from typing import Optional
import uuid
import datetime

from sqlmodel import Field, Column, JSON, SQLModel, Relationship

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
    date_bought: Optional[datetime.date] = Field(description="Date the wine has been bought on", default = datetime.date.today())
    price_bought: Optional[float] = Field(description="Price the wine has been bought at")
    quantity: Optional[int] = Field(description="Quantity of bottles in the cellar", default=1)



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
            date_bought = self.date_bought,
            price_bought = self.price_bought,
            quantity = self.quantity,
        )
