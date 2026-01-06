from typing import Optional
from sqlmodel import SQLModel
import datetime

class WineUpdate(SQLModel):
    name: Optional[str] = None
    producer: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None
    appellation: Optional[str] = None
    colour: Optional[str] = None
    vintage: Optional[int] = None
    notes: Optional[str] = None

    in_cellar: Optional[bool] = None
    has_been_tasted: Optional[bool] = None
    on_wishlist: Optional[bool] = None

    date_bought: Optional[datetime.date] = None
    price_bought: Optional[float] = None
    quantity: Optional[int] = None
