from typing import List

from nameof import nameof

from module.model.BaseItem import BaseItem
from module.model.ProductRating import ProductRating
from module.model.ProductReview import ProductReview
from module.model.Seller import Seller
from module.utils import to_string_class_formatter


class Offer(BaseItem):

    def __init__(self, id: str, title: str, price: float, image_url: str,
                 has_return_option: bool, description_length: int,
                 ratings: List[ProductRating], reviews: List[ProductReview],
                 seller: Seller) -> None:
        super().__init__(id)
        self.title = title
        self.price = price
        self.image_url = image_url
        self.has_return_option = has_return_option
        self.description_length = description_length
        self.ratings: List[ProductRating] = ratings
        self.reviews: List[ProductReview] = reviews
        self.seller = seller


    def __str__(self) -> str:
        return super().__str__() + to_string_class_formatter(
            [
                self.title, self.price, self.image_url, self.has_return_option,
                self.description_length, self.ratings, self.reviews, self.seller
            ],
            [
                nameof(self.title), nameof(self.price), nameof(self.image_url),
                nameof(self.has_return_option), nameof(self.description_length),
                nameof(self.ratings), nameof(self.reviews), nameof(self.seller)
            ],
            "\n"
        )
