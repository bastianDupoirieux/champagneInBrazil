from typing import Optional
import uuid
from sqlmodel import Field, Column, JSON, SQLModel, Relationship
from models.sql.fact_wine import FactWine

class Wine(SQLModel, table=True):
    __tablename__ = "wine"

    id: uuid.UUID = Field(primary_key=True, default=uuid.uuid4)
    name: str = Field(description="Name of the wine")
    producer: str = Field(description="Name of the producer")
    region: Optional[str] = Field(description="Production region of the wine")
    country: Optional[str] = Field(description="Country of production of the wine")
    appellation: Optional[str] = Field(description="Appellation of the wine")
    colour: str = Field(description="Colour of the wine, red, white, rosé, orange, sparkling")
    vintage: Optional[int] = Field(description="Vintage of wine production")
    grape_varieties: Optional[list[str]] = Field(description="List of grape varieties the wine is made of")
    notes: Optional[str] = Field(description="Notes of the wine", default=None)
    in_cellar: Optional[bool] = Field(description="Value indicating if the wine has been bought and is in the cellar")
    has_been_drunk: Optional[bool] = Field(description="Value indicating if the wine has been drank already")

    facts: list["FactWine"] = Relationship(back_populates="fact_wine")

    def get_wine(self):
        return Wine(
            id = uuid.uuid4(),
            name = self.name,
            producer = self.producer,
            region = self.region,
            country = self.country,
            appellation = self.appellation,
            colour = self.colour,
            vintage = self.vintage,
            grape_varieties = self.grape_varieties,
            notes = self.notes,
            in_cellar = self.in_cellar,
            has_been_drunk = self.has_been_drunk,
        )
