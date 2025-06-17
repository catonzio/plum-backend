from plum_chatbot.agents.tools.vector_db import query_vector_db
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from plum_chatbot.schemas.schema import Agent


class RagAgent(Agent):
    def __init__(self, name: str = "rag_agent", description: str = ""):
        super().__init__(name=name, description=description)
        self.prompt = (
            "You are an assistant for helping users using the Plum software, therefore you should always refer to the official documentation when providing answers."
            "You will be provided with a question and you may need to retrieve information from the documentation."
            # "Use the 3 following pieces of retrieved context to answer the question."
            "If you don't know the answer, say that you don't know."
            "Use three sentences maximum and keep the answer concise."
            "If you can answer directly without retrieving, do so."
            "If you need to retrieve, use the tools provided to you."
            "If you retrieve, use the retrieved content to answer the question."
            "The software is for italian users, so you should always answer in italian, unless the user specifies otherwise."
            "All the retrieved content will be in italian."
        )
        # Initialize the RAG agent
        self._initialize_rag_agent()

    def _initialize_rag_agent(self):
        self.llm = init_chat_model(
            "llama3.2", # qwen3:8b
            model_provider="ollama",
            base_url="host.docker.internal",
            temperature=0.5,
        )

        self.tools = [query_vector_db]

        self.graph = create_react_agent(
            self.llm,
            self.tools,
            checkpointer=MemorySaver(),
            prompt=self.prompt,
        )


if __name__ == "__main__":
    config = {"configurable": {"thread_id": "def234555"}}

    input_message = "come cambio la mail?"

    # for event in rag_agent.stream(
    #     {"messages": [{"role": "user", "content": input_message}]},
    #     stream_mode="values",
    #     config=config,
    # ):
    #     event["messages"][-1].pretty_print()
