from typing import List

from module.model.BaseItem import BaseItem
from module.model.Seller import Seller
from module.utils import to_string_class_formatter


class Offer(BaseItem):

    def __init__(self, id: str, seller: Seller) -> None:
        super().__init__(id)
        # TODO
        self.seller = seller


    def get_features_array(self) -> List:
        return [] + self.seller.get_features_array()


    def __str__(self) -> str:
        return super().__str__() + to_string_class_formatter(
            [],
            [],
            "\n"
        )
