import uuid
import datetime
from sqlmodel import SQLModel
from typing import Optional

class WineRead(SQLModel):
    id: uuid.UUID

    name: str
    producer: str
    region: Optional[str]
    country: Optional[str]
    appellation: Optional[str]
    colour: str
    vintage: Optional[int]
    notes: Optional[str]
    in_cellar: Optional[bool]
    has_been_tasted: Optional[bool]
    on_wishlist: Optional[bool]
    date_bought: Optional[datetime.date]
    price_bought: Optional[float]
    quantity: Optional[int]
