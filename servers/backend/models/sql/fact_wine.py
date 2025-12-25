from typing import Optional
import uuid
from sqlalchemy import ForeignKey
from sqlmodel import Field, Column, JSON, SQLModel, Relationship
import datetime

from models.sql.wine import Wine

class FactWine(SQLModel, table=True):
    __tablename__ = "fact_wine"
    id: uuid.UUID = Field(primary_key=True, default=uuid.uuid4)
    wine_id: uuid.UUID = Field(foreign_key="wine.id")
    fact: str = Field(description="Definition of the fact, can be date drank, date bought, price bought, quantity")
    value: datetime.date | float | int = Field(description="Value corresponding to the fact")

    fact_wine: Wine | None = Relationship(back_populates="facts")
