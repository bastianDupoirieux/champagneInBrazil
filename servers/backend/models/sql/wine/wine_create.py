from typing import Optional
import datetime
from sqlmodel import Field

from wine_base import WineBase

class WineCreate(WineBase):
    in_cellar: bool = Field(
        default = True,
        description="Value indicating if the wine has been bought and is in the cellar"
    )
    has_been_tasted: bool = Field(
        default = False,
        description="Value indicating if the wine has been drank already"
    )
    on_wishlist: bool = Field(
        default = False,
        description="Value indicating whether or not the wine is on the wishlist"
    )

    quantity: int = Field(
        default = 1,
        description="Quantity of bottles in the cellar"
    )

    date_bought: datetime.date = Field(
        default_factory=datetime.date.today,
        description="Date the wine has been bought on"
    )

    @classmethod
    def model_validate(cls, values):
        """
        Validates model based on the fact that at least one of the values of in_cellar, has_been_drunk or on_wishlist must be True
        :param values:
        :return:
        """
        in_cellar = values.get("in_cellar", False)
        has_been_drunk = values.get("has_been_drunk", False)
        on_wishlist = values.get("on_wishlist", False)

        if not (in_cellar or has_been_drunk or on_wishlist):
            raise ValueError(
                "At least one of 'in_cellar', 'has_been_drunk' or 'on_wishlist' must be True"
            )

        return values