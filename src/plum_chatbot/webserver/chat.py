import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from plum_chatbot.datasources.models.chat_message import Chat
from plum_chatbot.datasources.postgres_datasource import PostgresDatasource
from plum_chatbot.di_containers.datasources_containers import get_postgres_datasource
from plum_chatbot.schemas.schema import ChatMessage
from plum_chatbot.webserver.dtos.chat_dto import (
    CloseChatOutput,
    DeleteChatOutput,
    NewChatInput,
    NewChatOutput,
)

router = APIRouter(prefix="/chat", tags=["chat"])
logger = logging.getLogger(__name__)


@router.post("/new")
async def new_chat(
    datasource: Annotated[PostgresDatasource, Depends(get_postgres_datasource)],
    chat_input: NewChatInput,
) -> NewChatOutput:
    """
    Start a new chat session with the agent.
    """
    try:
        chat: Chat = Chat(
            user_id=chat_input.user_id,
        )
        datasource.insert(chat)
        return NewChatOutput(
            chat_id=UUID(str(chat.id)),
            message=ChatMessage(
                type="ai",
                content="Ciao! Io sono PlumChatbot, come posso esserti utile?",
            ),
        )
    except Exception as e:
        logger.error(f"An exception occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@router.get("/{chat_id}/close")
async def close_chat(
    datasource: Annotated[PostgresDatasource, Depends(get_postgres_datasource)],
    chat_id: UUID,
) -> CloseChatOutput:
    """
    Close an existing chat session.
    """
    try:
        chat = datasource.find(Chat, chat_id)
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")

        datasource.update(chat, is_closed=True)
        return CloseChatOutput(
            success=True, message="Chat session closed successfully."
        )
    except Exception as e:
        logger.error(f"An exception occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@router.delete("/{chat_id}")
async def delete_chat(
    datasource: Annotated[PostgresDatasource, Depends(get_postgres_datasource)],
    chat_id: UUID,
) -> DeleteChatOutput:
    """
    Delete an existing chat session.
    """
    try:
        chat = datasource.find(Chat, chat_id)
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")

        datasource.delete(chat)
        return DeleteChatOutput(
            success=True, message="Chat session deleted successfully."
        )
    except Exception as e:
        logger.error(f"An exception occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
