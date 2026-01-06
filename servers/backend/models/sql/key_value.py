import uuid
from sqlmodel import Field, Column, JSON, SQLModel

class KeyValueModel(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    key: str = Field(index=True)
    value: dict = Field(sa_column=Column(JSON))
