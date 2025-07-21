from uuid import UUID

from pydantic import BaseModel, Field

from plum_chatbot.schemas.schema import ChatMessage


class NewChatInput(BaseModel):
    """
    Represents the input for creating a new chat session.
    """

    user_id: UUID = Field(
        description="User ID to persist and continue a conversation across multiple threads.",
        examples=["847c6285-8fc9-4560-a83f-4e6285809254"],
    )


class NewChatOutput(BaseModel):
    """
    Represents the output of a new chat session.
    """

    chat_id: UUID = Field(
        description="Unique identifier for the chat session.",
        examples=["847c6285-8fc9-4560-a83f-4e6285809254"],
    )
    message: ChatMessage = Field(
        description="Message indicating the status of the chat session.",
        examples=["Ciao! Io sono PlumChatbot, come posso esserti utile?"],
    )


class BaseOutput(BaseModel):
    """
    Base output model for chat operations.
    This can be extended for specific outputs like closing or deleting a chat.
    """

    success: bool = Field(
        description="Indicates whether the operation was successful.",
        default=True,
        examples=[True],
    )
    message: str = Field(
        description="Message indicating the status of the operation.",
        examples=["Chat session closed successfully."],
    )


class CloseChatOutput(BaseOutput): ...


class DeleteChatOutput(BaseOutput): ...
