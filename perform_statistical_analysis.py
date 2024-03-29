import glob
from argparse import ArgumentParser, Namespace
from typing import List, Tuple

import matplotlib.pyplot as plt
import pandas as pd

from module.constants import DATASET_SOURCE_DIRECTORY, JSON_EXTENSION, MIN_MAX_REVIEW_VALUE
from module.model.Offer import Offer
from module.model.OffersWrapper import OffersWrapper
from module.model.ProductReview import ProductReview
from module.model.Seller import Seller
from module.service.common.LatexGenerator import LatexGenerator
from module.service.common.Logger import Logger
from module.utils import create_directory, get_filename, read_json_from_file, run_main

"""
"""

# VAR ------------------------------------------------------------------------ #
DATASET_DIR: str = DATASET_SOURCE_DIRECTORY
ANALYSIS_RESULTS_DIR: str = "_analysis_results/"

logger = Logger().get_logging_instance()
latex_generator: LatexGenerator = LatexGenerator(ANALYSIS_RESULTS_DIR)
SAVE_CHARTS: bool = True


# MAIN ----------------------------------------------------------------------- #
def main() -> None:
    args = prepare_args()
    create_directory(ANALYSIS_RESULTS_DIR)

    dataset_paths = glob.glob(DATASET_DIR + "*" + JSON_EXTENSION)
    for dataset_path in dataset_paths:
        offers_wrapper: OffersWrapper = OffersWrapper.from_dict(read_json_from_file(dataset_path))
        df: pd.DataFrame = build_data_frame(offers_wrapper.offers)

        generate_table(
            offers_wrapper.dataset_name, len(offers_wrapper.offers),
            pd.Series(len(offer.reviews) for offer in offers_wrapper.offers).mode()[0],
            len([offer for offer in offers_wrapper.offers if offer.is_specified_as_credible is True]),
            len([offer for offer in offers_wrapper.offers if offer.is_specified_as_credible is False]),
        )
        draw_hists(df, offers_wrapper.dataset_name)
        # draw_charts(df, dataset_name)


def build_data_frame(offers: List[Offer]) -> pd.DataFrame:
    offers_sellers = [
        Fields.get_offer_values(offer)
        + Fields.get_seller_values(offer.seller)
        + [pd.Series([review.stars_number for review in offer.reviews], dtype=float).mean()]
        for offer in offers
    ]
    return pd.DataFrame(
        data=offers_sellers,
        columns=Fields.get_offer_names() + Fields.get_seller_names() + [Fields.REVIEW_MEAN_STARS_NUMBER]
    )


def generate_table(dataset_name: str, offers_number: int, reviews_number_mode: int,
                   credible_offers_number: int, not_credible_offers_number: int) -> None:
    info: pd.DataFrame = pd.DataFrame(
        columns=["Nazwa", "Wartość"],
        data=[
            ["Nazwa katalogowa", dataset_name],
            ["Liczba ofert", str(offers_number)],
            # ["Dominanta liczby recenzji w ofertach", str(reviews_number_mode)],
            ["Liczba ofert określona jako wiarygodna przez eksperta", str(credible_offers_number)],
            ["Liczba ofert określona jako niewiarygodna przez eksperta", str(not_credible_offers_number)],
        ]
    )
    latex_generator.generate_vertical_table_df(info, dataset_name)


def draw_hists(df: pd.DataFrame, dataset_name: str) -> None:
    fields_groups: List[List[str]] = [
        [
            Fields.OFFER_PRICE,
            Fields.OFFER_DESCRIPTION_LENGTH,
            Fields.SELLER_FEEDBACK_SCORE,
            Fields.SELLER_FEEDBACK_PERCENTAGE,
        ],
        [
            Fields.SELLER_YEAR_OF_JOINING,
            Fields.SELLER_POSITIVE_RATINGS_NUMBER,
            Fields.SELLER_NEUTRAL_RATINGS_NUMBER,
            Fields.SELLER_NEGATIVE_RATINGS_NUMBER,
        ],
        [
            Fields.SELLER_ACCURATE_DESCRIPTION,
            Fields.SELLER_REASONABLE_SHIPPING_COST,
            Fields.SELLER_SHIPPING_SPEED,
            Fields.SELLER_COMMUNICATION,
        ]
    ]
    for index, fields_group in enumerate(fields_groups):
        draw_hist_2x2(df, fields_group, dataset_name, index, SAVE_CHARTS)

    plt.hist(df[Fields.REVIEW_MEAN_STARS_NUMBER], range=MIN_MAX_REVIEW_VALUE, color="white", edgecolor="blue")
    set_descriptions(f"{dataset_name} {Fields.REVIEW_MEAN_STARS_NUMBER}", "Wartość", "Liczba ofert")
    show_and_save(f"{dataset_name}_{Fields.REVIEW_MEAN_STARS_NUMBER}", SAVE_CHARTS)


# def draw_charts(df: pd.DataFrame, dataset_name: str) -> None:
#     fields_groups: List[List[Tuple[str, str]]] = [
#         [
#             (Fields.OFFER_PRICE, Fields.OFFER_DESCRIPTION_LENGTH),
#             (Fields.REVIEW_MEAN_STARS_NUMBER, Fields.OFFER_DESCRIPTION_LENGTH),
#             (Fields.SELLER_FEEDBACK_SCORE, Fields.OFFER_DESCRIPTION_LENGTH),
#             (Fields.SELLER_ACCURATE_DESCRIPTION, Fields.OFFER_DESCRIPTION_LENGTH),
#         ],
#     ]
#     for index, fields_group in enumerate(fields_groups):
#         draw_plot_2x2(df, fields_group, dataset_name, index, SAVE_CHARTS)


def draw_hist_2x2(df: pd.DataFrame, field_names: List[str], dataset_name: str,
                  order_number: int, save: bool = False) -> None:
    fig, axs = prepare_subplots(2, 2)
    # Disable scientific notation - for 2d arrays
    for ax in axs:
        for a in ax:
            a.ticklabel_format(useOffset=False, style="plain")

    fig.suptitle(dataset_name)
    set_subplot_hist(df[field_names[0]], field_names[0], "Wartość", "Liczba ofert", axs, 0, 0)
    set_subplot_hist(df[field_names[1]], field_names[1], "Wartość", "Liczba ofert", axs, 0, 1)
    set_subplot_hist(df[field_names[2]], field_names[2], "Wartość", "Liczba ofert", axs, 1, 0)
    set_subplot_hist(df[field_names[3]], field_names[3], "Wartość", "Liczba ofert", axs, 1, 1)
    show_and_save(f"{dataset_name}_{order_number + 1}", save)


# def draw_plot_2x2(df: pd.DataFrame, field_names_x_y: List[Tuple[str, str]],
#                   dataset_name: str, order_number: int, save: bool = False) -> None:
#     fig, axs = prepare_subplots(2, 2)
#     # Disable scientific notation - for 2d arrays
#     for ax in axs:
#         for a in ax:
#             a.ticklabel_format(useOffset=False, style="plain")
#
#     fig.suptitle(dataset_name)
#     set_subplot_plot(
#         df[field_names_x_y[0][0]], df[field_names_x_y[0][1]],
#         field_names_x_y[0][0], field_names_x_y[0][1], axs, 0, 0
#     )
#     set_subplot_plot(
#         df[field_names_x_y[1][0]], df[field_names_x_y[1][1]],
#         field_names_x_y[1][0], field_names_x_y[1][1], axs, 0, 1
#     )
#     set_subplot_plot(
#         df[field_names_x_y[2][0]], df[field_names_x_y[2][1]],
#         field_names_x_y[2][0], field_names_x_y[2][1], axs, 1, 0
#     )
#     set_subplot_plot(
#         df[field_names_x_y[3][0]], df[field_names_x_y[3][1]],
#         field_names_x_y[3][0], field_names_x_y[3][1], axs, 1, 1
#     )
#     show_and_save(f"{dataset_name}_{order_number + 1}", save)


def set_subplot_hist(data: pd.Series, subtitle: str, x_label: str,
                     y_label: str, axs, row: int, column: int) -> None:
    axs[row, column].set_title(subtitle)
    axs[row, column].set_xlabel(x_label)
    axs[row, column].set_ylabel(y_label)
    axs[row, column].hist(data, color="white", edgecolor="blue")


# def set_subplot_plot(data_x_axis: pd.Series, data_y_axis: pd.Series, subtitle_x_axis: str,
#                      subtitle_y_axis: str, axs, row: int, column: int) -> None:
#     axs[row, column].set(xlabel=subtitle_x_axis, ylabel=subtitle_y_axis)
#     axs[row, column].plot(data_x_axis, data_y_axis)


# DEF ----------------------------------------------------------------------- #
def prepare_subplots(row: int, column: int) -> Tuple:
    fig, axs = plt.subplots(row, column)
    plt.subplots_adjust(hspace=0.5)
    plt.subplots_adjust(wspace=0.5)
    return fig, axs


def set_descriptions(title: str, x_label: str = "", y_label: str = "") -> None:
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)


def show_and_save(name: str, save: bool = False) -> None:
    if save:
        filename = get_filename(name)
        plt.savefig(ANALYSIS_RESULTS_DIR + filename)
        plt.close()
    plt.show()


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
    OFFER_IS_SPECIFIED_AS_CREDIBLE: str = "offer_is_specified_as_credible"

    SELLER_ID: str = "seller_id"
    SELLER_FEEDBACK_SCORE: str = "seller_feedback_score"
    SELLER_FEEDBACK_PERCENTAGE: str = "seller_feedback_percentage"
    SELLER_YEAR_OF_JOINING: str = "seller_year_of_joining"
    SELLER_POSITIVE_RATINGS_NUMBER: str = "seller_positive_ratings_number"
    SELLER_NEUTRAL_RATINGS_NUMBER: str = "seller_neutral_ratings_number"
    SELLER_NEGATIVE_RATINGS_NUMBER: str = "seller_negative_ratings_number"
    SELLER_ACCURATE_DESCRIPTION: str = "seller_accurate_description"
    SELLER_REASONABLE_SHIPPING_COST: str = "seller_reasonable_shipping_cost"
    SELLER_SHIPPING_SPEED: str = "seller_shipping_speed"
    SELLER_COMMUNICATION: str = "seller_communication"

    REVIEW_ID: str = "review_id"
    REVIEW_STARS_NUMBER: str = "review_stars_number"
    REVIEW_MEAN_STARS_NUMBER: str = "mean_review_stars_number"
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
            Fields.OFFER_IS_SPECIFIED_AS_CREDIBLE
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
            offer.is_specified_as_credible
        ]


    @staticmethod
    def get_seller_names() -> List[str]:
        return [
            Fields.SELLER_ID,
            Fields.SELLER_FEEDBACK_SCORE,
            Fields.SELLER_FEEDBACK_PERCENTAGE,
            Fields.SELLER_YEAR_OF_JOINING,
            Fields.SELLER_POSITIVE_RATINGS_NUMBER,
            Fields.SELLER_NEUTRAL_RATINGS_NUMBER,
            Fields.SELLER_NEGATIVE_RATINGS_NUMBER,
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
