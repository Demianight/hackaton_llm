from sqlmodel import Session

from db import engine
from message import Message


def create_message(message: Message) -> Message:
    message.is_proccesed = False
    with Session(engine) as session:
        session.add(message)
        session.commit()
        session.refresh(message)
        return message
