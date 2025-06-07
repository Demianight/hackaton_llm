from sqlmodel import Field, SQLModel, Column, BigInteger


class Message(SQLModel, table=True):
    message_id: int = Field(primary_key=True, sa_column=Column(BigInteger()))

    chat_id: int | None = Field(sa_column=Column(BigInteger()))
    user_id: int | None = Field(sa_column=Column(BigInteger()))
    reply_to_message_id: int | None = Field(sa_column=Column(BigInteger()))

    date: int
    chat_type: str | None = None
    user_username: str | None = None
    user_first_name: str | None = None
    user_last_name: str | None = None
    text: str | None = None

    spam_score: float
