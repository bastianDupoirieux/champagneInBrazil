import uuid
from sqlmodel import Field

from wine_base import WineBase

class Wine(WineBase, table=True):
    __tablename__ = "wine"

    id: uuid.UUID = Field(
        primary_key=True,
        default_factory=uuid.uuid4,
        index=True,
    )
