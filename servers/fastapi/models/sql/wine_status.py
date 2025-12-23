from sqlmodel import SQLModel, Field
import uuid

class WineStatus(SQLModel, table=True):
    __tablename__ = "wine_status"
    id: uuid.UUID = Field(default = uuid.uuid4, primary_key=True)
    wine_id: uuid.UUID = Field(foreign_key="wines.id")
    status_expired: bool = Field(default = False)
