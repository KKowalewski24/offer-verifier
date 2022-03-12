from nameof import nameof

from module.model.ProductRating import ProductRating
from module.utils import to_string_class_formatter


class ProductReview(ProductRating):

    def __init__(self, id: str, stars_number: int, positive_votes_number: int,
                 negative_votes_number: int, contains_images: bool) -> None:
        super().__init__(id, stars_number)
        self.positive_votes_number = positive_votes_number
        self.negative_votes_number = negative_votes_number
        self.contains_images = contains_images


    def __str__(self) -> str:
        return super().__str__() + to_string_class_formatter(
            [
                self.positive_votes_number, self.negative_votes_number, self.contains_images
            ],
            [
                nameof(self.positive_votes_number), nameof(self.negative_votes_number),
                nameof(self.contains_images)
            ],
            "\n"
        )
