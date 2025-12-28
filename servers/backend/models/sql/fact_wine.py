from typing import Optional
import uuid
from sqlalchemy import ForeignKey
from sqlmodel import Field, Column, JSON, SQLModel, Relationship
import datetime

from models.sql.wine import Wine

class DimWine(SQLModel, table=True):
    __tablename__ = "fact_wine"
    id: uuid.UUID = Field(primary_key=True, default=uuid.uuid4)
    wine_id: uuid.UUID = Field(foreign_key="wine.id")
    date_bought: Optional[datetime.date] = Field(description = "Date the wine was bought at", default=datetime.date.today())
    price_bought: Optional[float] = Field(description="Price the wine was bought at")
    quantity: int = Field(description="Quantity of bottles in the cellar", default = 1)

    fact_wine: Wine | None = Relationship(back_populates="facts")
