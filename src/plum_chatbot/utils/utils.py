from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    ToolMessage,
)
from langchain_core.messages import (
    ChatMessage as LangchainChatMessage,
)

from plum_chatbot.schemas.schema import ChatMessage, ToolCall


def convert_message_content_to_string(content: str | list[str | dict]) -> str:
    if isinstance(content, str):
        return content
    text: list[str] = []
    for content_item in content:
        if isinstance(content_item, str):
            text.append(content_item)
            continue
        if content_item["type"] == "text":
            text.append(content_item["text"])
    return "".join(text)


def process_output(messages: list[BaseMessage]) -> ChatMessage:
    """Convert a list of LangChain messages to a list of ChatMessage."""
    message = langchain_to_chat_message(messages["messages"][-1])
    last_human_message_index = -1
    for i, m in enumerate(messages["messages"][::-1]):
        if isinstance(m, HumanMessage):
            last_human_message_index = i
            break
    last_human_message_index = len(messages["messages"]) - last_human_message_index - 1
    tool_calls = [
        lc_tool_to_tool_call(m)
        for m in messages["messages"][last_human_message_index:]
        if isinstance(m, ToolMessage)
    ]
    if tool_calls:
        message.tool_calls = tool_calls

    return message


def lc_tool_to_tool_call(tool: BaseMessage) -> dict:
    return ToolCall(
        name=tool.name,
        args=tool.status,
        id=tool.id,
        content=tool.content,
        type=tool.type if hasattr(tool, "type") else None,
    )


def langchain_to_chat_message(message: BaseMessage) -> ChatMessage:
    """Create a ChatMessage from a LangChain message."""
    match message:
        case HumanMessage():
            human_message = ChatMessage(
                type="human",
                content=convert_message_content_to_string(message.content),
            )
            return human_message
        case AIMessage():
            ai_message = ChatMessage(
                type="ai",
                content=convert_message_content_to_string(message.content),
            )
            if message.tool_calls:
                ai_message.tool_calls = message.tool_calls
            if message.response_metadata:
                ai_message.response_metadata = message.response_metadata
            return ai_message
        case ToolMessage():
            tool_message = ChatMessage(
                type="tool",
                content=convert_message_content_to_string(message.content),
                tool_call_id=message.tool_call_id,
            )
            return tool_message
        case LangchainChatMessage():
            if message.role == "custom":
                custom_message = ChatMessage(
                    type="custom",
                    content="",
                    custom_data=message.content[0],
                )
                return custom_message
            else:
                raise ValueError(f"Unsupported chat message role: {message.role}")
        case _:
            raise ValueError(f"Unsupported message type: {message.__class__.__name__}")
