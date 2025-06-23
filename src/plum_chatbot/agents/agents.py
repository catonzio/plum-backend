from typing import Any
from uuid import UUID, uuid4

from fastapi import HTTPException
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.pregel import Pregel
from langgraph.types import Command

from plum_chatbot.agents.my_agent import RagAgent
from plum_chatbot.schemas.schema import Agent, AgentInfo, ChatMessage, UserInput
from plum_chatbot.utils.utils import langchain_to_chat_message, process_output

DEFAULT_AGENT = "rag"


agents: dict[str, Agent] = {
    # "chatbot": Agent(description="A simple chatbot.", graph=rag_agent),
    "rag": RagAgent(
        name="rag_agent",
        description="A RAG agent that retrieves information from a vector database.",
    )
    # "research-assistant": Agent(
    #     description="A research assistant with web search and calculator.",
    #     graph=research_assistant,
    # ),
    # "rag-assistant": Agent(
    #     description="A RAG assistant with access to information in a database.",
    #     graph=rag_assistant,
    # ),
    # "command-agent": Agent(description="A command agent.", graph=command_agent),
    # "bg-task-agent": Agent(description="A background task agent.", graph=bg_task_agent),
    # "langgraph-supervisor-agent": Agent(
    #     description="A langgraph supervisor agent", graph=langgraph_supervisor_agent
    # ),
    # "interrupt-agent": Agent(
    #     description="An agent the uses interrupts.", graph=interrupt_agent
    # ),
    # "knowledge-base-agent": Agent(
    #     description="A retrieval-augmented generation agent using Amazon Bedrock Knowledge Base",
    #     graph=kb_agent,
    # ),
}


def get_agent(agent_id: str) -> Pregel:
    return agents[agent_id].graph


def get_all_agent_info() -> list[AgentInfo]:
    return [
        AgentInfo(key=agent_id, description=agent.description)
        for agent_id, agent in agents.items()
    ]


async def _handle_input(
    user_input: UserInput, agent: Pregel
) -> tuple[dict[str, Any], UUID, UUID]:
    """
    Parse user input and handle any required interrupt resumption.
    Returns kwargs for agent invocation and the run_id.
    """
    run_id = uuid4()
    thread_id = user_input.thread_id or str(uuid4())
    user_id = user_input.user_id or str(uuid4())

    configurable = {
        "thread_id": thread_id,
        "model": user_input.model,
        "user_id": user_id,
    }

    if user_input.agent_config:
        if overlap := configurable.keys() & user_input.agent_config.keys():
            raise HTTPException(
                status_code=422,
                detail=f"agent_config contains reserved keys: {overlap}",
            )
        configurable.update(user_input.agent_config)

    config = RunnableConfig(
        configurable=configurable,
        run_id=run_id,
    )

    # Check for interrupts that need to be resumed
    state = await agent.aget_state(config=config)
    interrupted_tasks = [
        task for task in state.tasks if hasattr(task, "interrupts") and task.interrupts
    ]

    input: Command | dict[str, Any]
    if interrupted_tasks:
        # assume user input is response to resume agent execution from interrupt
        input = Command(resume=user_input.message)
    else:
        input = {"messages": [HumanMessage(content=user_input.message)]}

    kwargs = {
        "input": input,
        "config": config,
    }

    return kwargs, run_id, thread_id


async def invoke_chatbot(user_input: UserInput, agent_id: str) -> ChatMessage:
    agent: Pregel = get_agent(agent_id)
    kwargs, run_id, thread_id = await _handle_input(user_input, agent)
    response_events: list[tuple[str, Any]] = await agent.ainvoke(**kwargs, stream_mode=["updates", "values"])  # type: ignore # fmt: skip
    response_type, response = response_events[-1]
    if response_type == "values":
        # Normal response, the agent completed successfully
        output = process_output(response)
    elif response_type == "updates" and "__interrupt__" in response:
        # The last thing to occur was an interrupt
        # Return the value of the first interrupt as an AIMessage
        output = langchain_to_chat_message(
            AIMessage(content=response["__interrupt__"][0].value)
        )
    else:
        raise ValueError(f"Unexpected response type: {response_type}")

    output.run_id = str(run_id)
    output.thread_id = str(thread_id)
    return output
