import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from plum_chatbot.datasources.models.feedback import (
    Feedback,  # noqa: F401 - needed for SQLAlchemy table creation
)
from plum_chatbot.datasources.postgres_datasource import PostgresDatasource
from plum_chatbot.di_containers.datasources_containers import get_postgres_datasource
from plum_chatbot.webserver.dtos.feedback_dto import NewFeedbackInput, NewFeedbackOutput

router = APIRouter(prefix="/feedbacks", tags=["feedbacks"])
logger = logging.getLogger(__name__)


@router.post("/new")
async def new_feedback(
    datasource: Annotated[PostgresDatasource, Depends(get_postgres_datasource)],
    feedback_input: NewFeedbackInput,
) -> NewFeedbackOutput:
    """
    Start a new feedback session with the agent.
    """
    try:
        feedbacks: list[Feedback] = datasource.all(
            Feedback, condition=f"message_id = '{feedback_input.message_id}'"
        )
        if feedbacks:
            for feedback in feedbacks:
                datasource.delete(feedback)
        datasource.insert(
            Feedback(
                message_id=feedback_input.message_id,
                is_positive=feedback_input.is_positive,
                description=feedback_input.description,
            )
        )
        return NewFeedbackOutput(
            feedback_id=UUID("847c6285-8fc9-4560-a83f-4e6285809254"),
            message="Feedback submitted successfully.",
        )
    except Exception as e:
        logger.error(f"An exception occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
