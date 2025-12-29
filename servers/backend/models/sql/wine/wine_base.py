from typing import Optional
import datetime
from sqlmodel import SQLModel, Field

class WineBase(SQLModel):
    name: str = Field(description="Name of the wine")
    producer: str = Field(description="Name of the producer")
    region: Optional[str] = Field(
        default = None,
        description="Production region of the wine"
    )
    country: Optional[str] = Field(
        default = None,
        description="Country of production of the wine"
    )
    appellation: Optional[str] = Field(
        default = None,
        description="Appellation of the wine"
    )
    colour: str = Field(
        default = None,
        description="Colour of the wine, red, white, rosé, orange, sparkling"
    )
    vintage: Optional[int] = Field(
        default = None,
        description="Vintage of wine production"
    )
    notes: Optional[str] = Field(
        default = None,
        description="Notes of the wine"
    )
    in_cellar: Optional[bool] = Field(
        default = None,
        description="Value indicating if the wine has been bought and is in the cellar"
    )
    has_been_drunk: Optional[bool] = Field(
        default = None,
        description="Value indicating if the wine has been drank already"
    )
    on_wishlist: Optional[bool] = Field(
        default = None,
        description="Value indicating whether or not the wine is on the wishlist"
    )
    date_bought: Optional[datetime.date] = Field(
        default = None,
        description="Date the wine has been bought on"
    )
    price_bought: Optional[float] = Field(
        default = None,
        description="Price the wine has been bought at"
    )
    quantity: Optional[int] = Field(
        default = None,
        description="Quantity of bottles in the cellar"
    )
