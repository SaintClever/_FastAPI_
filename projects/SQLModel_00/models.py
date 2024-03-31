from sqlmodel import SQLModel, Field


class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    email: str = Field(max_length=100)
