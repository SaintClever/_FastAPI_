from sqlmodel import SQLModel, Field
from typing import Optional

# Category class (and SQL table)
class Category(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str = Field(min_length=3, max_length=15, index=True, unique=True)
