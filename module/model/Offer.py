from typing import List

from nameof import nameof

from module.model.AnalyzableItem import AnalyzableItem
from module.model.Seller import Seller
from module.utils import to_string_class_formatter


class Offer(AnalyzableItem):

    def __init__(self, id: str, title: str, price: float, image_url: str,
                 has_return_option: bool, description_length: int, product_reviews_number: int,
                 product_rating: float, product_ratings_number: int, seller: Seller) -> None:
        super().__init__(id)
        self.title = title
        self.price = price
        self.image_url = image_url
        self.has_return_option = has_return_option
        self.description_length = description_length
        self.product_reviews_number = product_reviews_number
        self.product_rating = product_rating
        self.product_ratings_number = product_ratings_number
        self.seller = seller


    def get_feature_names(self) -> List[str]:
        return [nameof(self.price), nameof(self.has_return_option), nameof(self.description_length),
                nameof(self.product_reviews_number), nameof(self.product_rating),
                nameof(self.product_ratings_number)] + self.seller.get_feature_names()


    def get_feature_values(self) -> List:
        return [self.price, self.has_return_option, self.description_length,
                self.product_reviews_number, self.product_rating,
                self.product_ratings_number] + self.seller.get_feature_values()


    def get_non_numeric_feature_names(self) -> List[str]:
        return [nameof(self.has_return_option)] + self.seller.get_non_numeric_feature_names()


    def __str__(self) -> str:
        return super().__str__() + to_string_class_formatter(
            [
                self.title, self.price, self.image_url, self.has_return_option,
                self.description_length, self.product_reviews_number, self.product_rating,
                self.product_ratings_number, self.seller
            ],
            [
                nameof(self.title), nameof(self.price), nameof(self.image_url),
                nameof(self.has_return_option), nameof(self.description_length),
                nameof(self.product_reviews_number), nameof(self.product_rating),
                nameof(self.product_ratings_number), nameof(self.seller)
            ],
            "\n"
        )
