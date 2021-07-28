from typing import List

from module.model.AnalyzableItem import AnalyzableItem
from module.utils import to_string_class_formatter


class Seller(AnalyzableItem):

    def __init__(self, id: str) -> None:
        super().__init__(id)
        # TODO


    def get_feature_names(self) -> List[str]:
        return []


    def get_feature_values(self) -> List:
        return []


    def get_non_numeric_feature_names(self) -> List[str]:
        return []


    def __str__(self) -> str:
        return super().__str__() + to_string_class_formatter(
            [],
            [],
            "\n"
        )
