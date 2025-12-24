from sqlmodel import SQLModel, Field
import uuid

class WineStatus(SQLModel, table=True):
    __tablename__ = "wine_status"
    id: uuid.UUID = Field(default = uuid.uuid4, primary_key=True)
    wine_id: uuid.UUID = Field(foreign_key="wines.id")
    part_of_Cellar: bool = Field(default = True)
    wine_has_been_drank: bool = Field(default = False)
