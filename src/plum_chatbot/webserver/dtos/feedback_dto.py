from uuid import UUID

from pydantic import BaseModel, Field


class NewFeedbackInput(BaseModel):
    message_id: UUID
    is_positive: bool = Field(
        description="Indicates whether the feedback is positive or negative.",
        examples=[True, False],
    )
    description: str | None = Field(
        description="Optional description of the feedback.",
        default=None,
        examples=["The response was helpful and accurate."],
    )


class NewFeedbackOutput(BaseModel):
    """
    Represents the output of a new feedback session.
    """

    feedback_id: UUID = Field(
        description="Unique identifier for the feedback session.",
        examples=["847c6285-8fc9-4560-a83f-4e6285809254"],
    )
    message: str = Field(
        description="Message indicating the status of the feedback submission.",
        examples=["Feedback submitted successfully."],
    )
