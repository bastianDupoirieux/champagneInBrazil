from typing import Optional
import uuid
from sqlalchemy import ForeignKey
from sqlmodel import Field, Column, JSON, SQLModel
import datetime

class fact_wine(SQLModel, table=True):
    __tablename__ = "fact_wine"
    id: uuid.UUID = Field(primary_key=True, default=uuid.uuid4)
    wine_id: uuid.UUID = Field(foreign_key="wines.id")
    date_bought: Optional[datetime.date] = Field(default = datetime.date.today())
    price_bought: Optional[float] = None
    quantity: int = Field(default = 1)
