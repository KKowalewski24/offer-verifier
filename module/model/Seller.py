from nameof import nameof

from module.model.BaseItem import BaseItem
from module.utils import to_string_class_formatter


class Seller(BaseItem):

    def __init__(self, id: str, feedback_score: float, seller_feedback_percentage: float,
                 year_of_joining: int, seller_positive_ratings_number: int,
                 seller_neutral_ratings_number: int, seller_negative_ratings_number: int,
                 accurate_description: float, reasonable_shipping_cost: float,
                 shipping_speed: float, communication: float) -> None:
        super().__init__(id)
        self.feedback_score = feedback_score
        self.seller_feedback_percentage = seller_feedback_percentage
        self.year_of_joining = year_of_joining
        self.seller_positive_ratings_number = seller_positive_ratings_number
        self.seller_neutral_ratings_number = seller_neutral_ratings_number
        self.seller_negative_ratings_number = seller_negative_ratings_number
        self.accurate_description = accurate_description
        self.reasonable_shipping_cost = reasonable_shipping_cost
        self.shipping_speed = shipping_speed
        self.communication = communication


    def __str__(self) -> str:
        return super().__str__() + to_string_class_formatter(
            [
                self.feedback_score, self.seller_feedback_percentage, self.year_of_joining,
                self.seller_positive_ratings_number, self.seller_neutral_ratings_number,
                self.seller_negative_ratings_number, self.accurate_description,
                self.reasonable_shipping_cost, self.shipping_speed, self.communication
            ],
            [
                nameof(self.feedback_score), nameof(self.seller_feedback_percentage),
                nameof(self.year_of_joining), nameof(self.seller_positive_ratings_number),
                nameof(self.seller_neutral_ratings_number),
                nameof(self.seller_negative_ratings_number), nameof(self.accurate_description),
                nameof(self.reasonable_shipping_cost), nameof(self.shipping_speed),
                nameof(self.communication)
            ],
            "\n"
        )
