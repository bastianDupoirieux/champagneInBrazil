from typing import Optional
import uuid
from sqlalchemy import ForeignKey
from sqlmodel import Field, Column, JSON, SQLModel

class Wines(SQLModel, table=True):
    __tablename__ = "wines"

    id: uuid.UUID = Field(primary_key=True, default=uuid.uuid4)
    name: str = Field(description="Name of the wine")
    producer: str = Field(description="Name of the producer")
    region: Optional[str] = Field(description="Production region of the wine")
    country: Optional[str] = Field(description="Country of production of the wine")
    appellation: Optional[str] = Field(description="Appellation of the wine")
    colour: str = Field(description="Colour of the wine, red, white, rosé, orange")
    vintage: Optional[int] = Field(description="Vintage of wine production")
    grape_varieties: Optional[list[str]] = Field(description="List of grape varieties the wine is made of")
    notes: Optional[str] = Field(description="Notes of the wine", default=None)

