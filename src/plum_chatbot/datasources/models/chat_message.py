from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from plum_chatbot.datasources.postgres_datasource import BaseTable


class Chat(BaseTable):
    __tablename__ = "chats"

    id = Column(UUID, primary_key=True, default=uuid4)
    user_id = Column(UUID, nullable=False)
    is_closed = Column(
        Boolean, default=False, nullable=False
    )  # 0 for open, 1 for closed
    created_at = Column(DateTime, default=datetime.now)

    @classmethod
    def from_tuple(cls, data: tuple[UUID, UUID, datetime]) -> "Chat":
        """
        Create a Chat instance from a tuple.

        :param data: A tuple containing the fields in the order:
                        (id, user_id, created_at)
        :return: An instance of Chat.
        """
        return cls(
            id=data[0],
            user_id=data[1],
            created_at=data[2],
        )


class ChatMessage(BaseTable):
    __tablename__ = "chat_messages"

    id = Column(UUID, primary_key=True, default=uuid4)
    chat_id = Column(UUID, ForeignKey("chats.id"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)

    chat = relationship("Chat", foreign_keys=[chat_id])
    feedbacks = relationship("Feedback", back_populates="message")

    @classmethod
    def from_tuple(cls, data: tuple[UUID, UUID, str, str, datetime]) -> "ChatMessage":
        """
        Create a ChatMessage instance from a tuple.

        :param data: A tuple containing the fields in the order:
                     (id, chat_id, question, answer, timestamp)
        :return: An instance of ChatMessage.
        """
        return cls(
            id=data[0],
            chat_id=data[1],
            question=data[2],
            answer=data[3],
            timestamp=data[4],
        )
