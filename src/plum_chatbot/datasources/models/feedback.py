from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from plum_chatbot.datasources.postgres_datasource import BaseTable


class Feedback(BaseTable):
    __tablename__ = "feedbacks"

    id = Column(UUID, primary_key=True, default=uuid4)
    message_id = Column(UUID, ForeignKey("chat_messages.id"), nullable=False)
    is_positive = Column(Boolean, nullable=False)
    description = Column(Text, nullable=True, default="")
    timestamp = Column(DateTime, default=datetime.now)

    # Relationship: one feedback belongs to one chat message
    # The 'message_id' refers to the 'id' column in the ChatMessage table
    message = relationship("ChatMessage", back_populates="feedbacks")
