from nameof import nameof

from module.model.BaseItem import BaseItem
from module.utils import to_string_class_formatter


class ProductRating(BaseItem):

    def __init__(self, id: str, stars_number: int) -> None:
        super().__init__(id)
        self.stars_number = stars_number


    def __str__(self) -> str:
        return to_string_class_formatter([self.stars_number], [nameof(self.stars_number)], "\n")
