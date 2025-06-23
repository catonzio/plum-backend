from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, Column, DateTime, Integer, Text

from plum_chatbot.datasources.postgres_datasource import BaseTable


class ChatMessage(BaseTable):
    __tablename__ = "chat_messages"

    id = Column(UUID, primary_key=True, default=uuid4)
    chat_id = Column(UUID)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    positive_feedback = Column(Integer, default=None, nullable=True)
    timestamp = Column(DateTime, default=datetime.now)

    @classmethod
    def from_tuple(
        cls, data: tuple[UUID, UUID, str, str, int, datetime]
    ) -> "ChatMessage":
        """
        Create a ChatMessage instance from a tuple.

        :param data: A tuple containing the fields in the order:
                     (id, chat_id, question, answer, positive_feedback, timestamp)
        :return: An instance of ChatMessage.
        """
        return cls(
            id=data[0],
            chat_id=data[1],
            question=data[2],
            answer=data[3],
            positive_feedback=data[4],
            timestamp=data[5],
        )
