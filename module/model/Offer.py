from typing import Dict

from nameof import nameof

from module.model.BaseItem import BaseItem
from module.model.Seller import Seller
from module.utils import to_string_class_formatter


class Offer(BaseItem):

    def __init__(self, id: str, title: str, price: float, image_url: str,
                 has_return_option: bool, description_length: int, reviews_number: int,
                 product_rating: float, ratings_number: int, seller: Seller) -> None:
        super().__init__(id)
        self.title = title
        self.price = price
        self.image_url = image_url
        self.has_return_option = has_return_option
        self.description_length = description_length
        self.reviews_number = reviews_number
        self.product_rating = product_rating
        self.ratings_number = ratings_number
        self.seller = seller


    def get_features_array(self) -> Dict:
        features: Dict = {
            "price": self.price,
            "has_return_option": self.has_return_option,
            "description_length": self.description_length,
            "reviews_number": self.reviews_number,
            "product_rating": self.product_rating,
            "ratings_number": self.ratings_number
        }

        features.update(self.seller.get_features_array())
        return features


    def __str__(self) -> str:
        return super().__str__() + to_string_class_formatter(
            [
                self.title, self.price, self.image_url, self.has_return_option,
                self.description_length, self.reviews_number, self.product_rating,
                self.ratings_number, self.seller
            ],
            [
                nameof(self.title), nameof(self.price), nameof(self.image_url),
                nameof(self.has_return_option), nameof(self.description_length),
                nameof(self.reviews_number), nameof(self.product_rating),
                nameof(self.ratings_number), nameof(self.seller)
            ],
            "\n"
        )
