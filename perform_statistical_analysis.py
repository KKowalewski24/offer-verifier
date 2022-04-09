import glob
from argparse import ArgumentParser, Namespace
from typing import List

import pandas as pd

from module.constants import PICKLE_EXTENSION
from module.model.Offer import Offer
from module.model.ProductReview import ProductReview
from module.model.Seller import Seller
from module.service.common.Logger import Logger
from module.utils import read_object_from_file, run_main

"""
"""

# VAR ------------------------------------------------------------------------ #
ANALYSIS_RESULTS_DIR: str = "analysis_results"
DATASET_DIR: str = "dataset_snapshot/"

logger = Logger().get_logging_instance()


# DEF ----------------------------------------------------------------------- #
def main() -> None:
    args = prepare_args()
    dataset_paths = glob.glob(DATASET_DIR + "*" + PICKLE_EXTENSION)
    for dataset_path in dataset_paths:
        offers: List[Offer] = list(read_object_from_file(dataset_path))

        offers_seller = [
            Fields.get_offer_values(offer) + Fields.get_seller_values(offer.seller)
            for offer in offers
        ]
        df_offers_seller: pd.DataFrame = pd.DataFrame(
            data=offers_seller,
            columns=Fields.get_offer_names() + Fields.get_seller_names()
        )


def prepare_args() -> Namespace:
    arg_parser = ArgumentParser()

    return arg_parser.parse_args()


class Fields:
    OFFER_ID: str = "offer_id"
    OFFER_TITLE: str = "offer_title"
    OFFER_PRICE: str = "offer_price"
    OFFER_IMAGE_URL: str = "offer_image_url"
    OFFER_HAS_RETURN_OPTION: str = "offer_has_return_option"
    OFFER_DESCRIPTION_LENGTH: str = "offer_description_length"

    SELLER_ID: str = "seller_id"
    SELLER_FEEDBACK_SCORE: str = "seller_feedback_score"
    SELLER_SELLER_FEEDBACK_PERCENTAGE: str = "seller_seller_feedback_percentage"
    SELLER_YEAR_OF_JOINING: str = "seller_year_of_joining"
    SELLER_SELLER_POSITIVE_RATINGS_NUMBER: str = "seller_seller_positive_ratings_number"
    SELLER_SELLER_NEUTRAL_RATINGS_NUMBER: str = "seller_seller_neutral_ratings_number"
    SELLER_SELLER_NEGATIVE_RATINGS_NUMBER: str = "seller_seller_negative_ratings_number"
    SELLER_ACCURATE_DESCRIPTION: str = "seller_accurate_description"
    SELLER_REASONABLE_SHIPPING_COST: str = "seller_reasonable_shipping_cost"
    SELLER_SHIPPING_SPEED: str = "seller_shipping_speed"
    SELLER_COMMUNICATION: str = "seller_communication"

    REVIEW_ID: str = "review_id"
    REVIEW_STARS_NUMBER: str = "review_stars_number"
    REVIEW_TEXT_CONTENT: str = "review_text_content"
    REVIEW_POSITIVE_VOTES_NUMBER: str = "review_positive_votes_number"
    REVIEW_NEGATIVE_VOTES_NUMBER: str = "review_negative_votes_number"
    REVIEW_CONTAINS_IMAGES: str = "review_contains_images"


    @staticmethod
    def get_offer_names() -> List[str]:
        return [
            Fields.OFFER_ID,
            Fields.OFFER_TITLE,
            Fields.OFFER_PRICE,
            Fields.OFFER_IMAGE_URL,
            Fields.OFFER_HAS_RETURN_OPTION,
            Fields.OFFER_DESCRIPTION_LENGTH,
        ]


    @staticmethod
    def get_offer_values(offer: Offer) -> List:
        return [
            offer.id,
            offer.title,
            offer.price,
            offer.image_url,
            offer.has_return_option,
            offer.description_length,
        ]


    @staticmethod
    def get_seller_names() -> List[str]:
        return [
            Fields.SELLER_ID,
            Fields.SELLER_FEEDBACK_SCORE,
            Fields.SELLER_SELLER_FEEDBACK_PERCENTAGE,
            Fields.SELLER_YEAR_OF_JOINING,
            Fields.SELLER_SELLER_POSITIVE_RATINGS_NUMBER,
            Fields.SELLER_SELLER_NEUTRAL_RATINGS_NUMBER,
            Fields.SELLER_SELLER_NEGATIVE_RATINGS_NUMBER,
            Fields.SELLER_ACCURATE_DESCRIPTION,
            Fields.SELLER_REASONABLE_SHIPPING_COST,
            Fields.SELLER_SHIPPING_SPEED,
            Fields.SELLER_COMMUNICATION,
        ]


    @staticmethod
    def get_seller_values(seller: Seller) -> List:
        return [
            seller.id,
            seller.feedback_score,
            seller.seller_feedback_percentage,
            seller.year_of_joining,
            seller.seller_positive_ratings_number,
            seller.seller_neutral_ratings_number,
            seller.seller_negative_ratings_number,
            seller.accurate_description,
            seller.reasonable_shipping_cost,
            seller.shipping_speed,
            seller.communication,
        ]


    @staticmethod
    def get_review_names() -> List[str]:
        return [
            Fields.REVIEW_ID,
            Fields.REVIEW_STARS_NUMBER,
            Fields.REVIEW_TEXT_CONTENT,
            Fields.REVIEW_POSITIVE_VOTES_NUMBER,
            Fields.REVIEW_NEGATIVE_VOTES_NUMBER,
            Fields.REVIEW_CONTAINS_IMAGES,
        ]


    @staticmethod
    def get_review_values(review: ProductReview) -> List:
        return [
            review.id,
            review.stars_number,
            review.text_content,
            review.positive_votes_number,
            review.negative_votes_number,
            review.contains_images,
        ]


# __MAIN__ ------------------------------------------------------------------- #
if __name__ == "__main__":
    run_main(main)
