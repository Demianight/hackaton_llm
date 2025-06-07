from sqlmodel import Session

from db import engine
from message import Message


def create_message(message: Message) -> Message:
    message = Message(
        spam_score=message.spam_score,
        text=message.text,
        date=message.date,
        chat_id=10,
        chat_type=message.chat_type,
        user_id=message.user_id,
        user_username=message.user_username,
        user_first_name=message.user_first_name,
        user_last_name=message.user_last_name,
        reply_to_message_id=message.reply_to_message_id,
    )
    with Session(engine) as session:
        session.add(message)
        session.commit()
        session.refresh(message)
        return message
