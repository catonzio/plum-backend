import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from plum_chatbot.agents.agents import invoke_chatbot
from plum_chatbot.configs.settings import Settings
from plum_chatbot.datasources.models.chat_message import (
    Chat,
)
from plum_chatbot.datasources.models.chat_message import (
    ChatMessage as DBChatMessage,
)
from plum_chatbot.datasources.postgres_datasource import PostgresDatasource
from plum_chatbot.di_containers.datasources_containers import get_postgres_datasource
from plum_chatbot.schemas.schema import ChatMessage, UserInput

router = APIRouter(prefix="/agent", tags=["agent"])
logger = logging.getLogger(__name__)


@router.post("/{agent_id}/invoke")
@router.post("/invoke")
async def invoke(
    datasource: Annotated[PostgresDatasource, Depends(get_postgres_datasource)],
    user_input: UserInput,
    agent_id: str = Settings().DEFAULT_AGENT,
) -> ChatMessage:
    """
    Invoke an agent with user input to retrieve a final response.

    If agent_id is not provided, the default agent will be used.
    Use `chat_id` to persist and continue a multi-turn conversation. `run_id` kwarg
    is also attached to messages for recording feedback.
    Use `user_id` to persist and continue a conversation across multiple threads.
    """
    # NOTE: Currently this only returns the last message or interrupt.
    # In the case of an agent outputting multiple AIMessages (such as the background step
    # in interrupt-agent, or a tool step in research-assistant), it's omitted. Arguably,
    # you'd want to include it. You could update the API to return a list of ChatMessages
    # in that case.

    try:
        if (
            not user_input.chat_id
            or datasource.find(Chat, UUID(user_input.chat_id)) is None
        ):
            raise HTTPException(
                status_code=404, detail="Chat session not found or not provided."
            )
        answer: ChatMessage = await invoke_chatbot(user_input, agent_id)
        db_message: DBChatMessage = DBChatMessage(
            chat_id=answer.thread_id,
            question=user_input.message,
            answer=answer.content,
        )
        datasource.insert(db_message)
        answer.message_id = str(db_message.id)
        return answer
    except Exception as e:
        logger.error(f"An exception occurred: {e}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
