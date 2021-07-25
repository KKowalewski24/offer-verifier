from typing import List

from module.model.BaseItem import BaseItem
from module.utils import to_string_class_formatter


class Seller(BaseItem):

    def __init__(self, id: str) -> None:
        super().__init__(id)
        # TODO


    def get_features_array(self) -> List:
        return []


    def __str__(self) -> str:
        return super().__str__() + to_string_class_formatter(
            [],
            [],
            "\n"
        )
