import glob
import os
from argparse import ArgumentParser, Namespace
from typing import List, Tuple

import matplotlib.pyplot as plt
import pandas as pd

from module.constants import MIN_MAX_REVIEW_VALUE, PICKLE_EXTENSION, UTF_8
from module.model.Offer import Offer
from module.model.ProductReview import ProductReview
from module.model.Seller import Seller
from module.service.common.LatexGenerator import LatexGenerator
from module.service.common.Logger import Logger
from module.utils import create_directory, get_filename, read_object_from_file, run_main

"""
"""

# VAR ------------------------------------------------------------------------ #
ANALYSIS_RESULTS_DIR: str = "analysis_results/"
DATASET_DIR: str = "dataset_snapshot/"
LATEX_IMAGE_FILENAME: str = "latex_images.txt"

logger = Logger().get_logging_instance()
latex_generator: LatexGenerator = LatexGenerator(ANALYSIS_RESULTS_DIR)
SAVE_CHARTS: bool = True


# MAIN ----------------------------------------------------------------------- #
def main() -> None:
    args = prepare_args()
    create_directory(ANALYSIS_RESULTS_DIR)

    dataset_paths = glob.glob(DATASET_DIR + "*" + PICKLE_EXTENSION)
    for dataset_path in dataset_paths:
        dataset_name: str = str(os.path.basename(dataset_path).split(".")[0])
        offers: List[Offer] = list(read_object_from_file(dataset_path))
        df: pd.DataFrame = build_data_frame(offers)

        draw_hists(df, dataset_name)
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

    plt.hist(df[Fields.REVIEW_MEAN_STARS_NUMBER], range=MIN_MAX_REVIEW_VALUE)
    set_descriptions(f"{dataset_name} {Fields.REVIEW_MEAN_STARS_NUMBER}")
    show_and_save(f"{dataset_name}_{Fields.REVIEW_MEAN_STARS_NUMBER}", SAVE_CHARTS)


def draw_charts(df: pd.DataFrame, dataset_name: str) -> None:
    fields_groups: List[List[Tuple[str, str]]] = [
        [
            (Fields.OFFER_PRICE, Fields.OFFER_DESCRIPTION_LENGTH),
            (Fields.REVIEW_MEAN_STARS_NUMBER, Fields.OFFER_DESCRIPTION_LENGTH),
            (Fields.SELLER_FEEDBACK_SCORE, Fields.OFFER_DESCRIPTION_LENGTH),
            (Fields.SELLER_ACCURATE_DESCRIPTION, Fields.OFFER_DESCRIPTION_LENGTH),
        ],
    ]
    for index, fields_group in enumerate(fields_groups):
        draw_plot_2x2(df, fields_group, dataset_name, index, SAVE_CHARTS)


def draw_hist_2x2(df: pd.DataFrame, field_names: List[str], dataset_name: str,
                  order_number: int, save: bool = False) -> None:
    fig, axs = prepare_subplots(2, 2)
    # Disable scientific notation - for 2d arrays
    for ax in axs:
        for a in ax:
            a.ticklabel_format(useOffset=False, style="plain")

    fig.suptitle(dataset_name)
    set_subplot_hist(df[field_names[0]], field_names[0], axs, 0, 0)
    set_subplot_hist(df[field_names[1]], field_names[1], axs, 0, 1)
    set_subplot_hist(df[field_names[2]], field_names[2], axs, 1, 0)
    set_subplot_hist(df[field_names[3]], field_names[3], axs, 1, 1)
    show_and_save(f"{dataset_name}_{order_number + 1}", save)


def draw_plot_2x2(df: pd.DataFrame, field_names_x_y: List[Tuple[str, str]],
                  dataset_name: str, order_number: int, save: bool = False) -> None:
    fig, axs = prepare_subplots(2, 2)
    # Disable scientific notation - for 2d arrays
    for ax in axs:
        for a in ax:
            a.ticklabel_format(useOffset=False, style="plain")

    fig.suptitle(dataset_name)
    set_subplot_plot(
        df[field_names_x_y[0][0]], df[field_names_x_y[0][1]],
        field_names_x_y[0][0], field_names_x_y[0][1], axs, 0, 0
    )
    set_subplot_plot(
        df[field_names_x_y[1][0]], df[field_names_x_y[1][1]],
        field_names_x_y[1][0], field_names_x_y[1][1], axs, 0, 1
    )
    set_subplot_plot(
        df[field_names_x_y[2][0]], df[field_names_x_y[2][1]],
        field_names_x_y[2][0], field_names_x_y[2][1], axs, 1, 0
    )
    set_subplot_plot(
        df[field_names_x_y[3][0]], df[field_names_x_y[3][1]],
        field_names_x_y[3][0], field_names_x_y[3][1], axs, 1, 1
    )
    show_and_save(f"{dataset_name}_{order_number + 1}", save)


def set_subplot_hist(data: pd.Series, subtitle: str, axs, row: int, column: int) -> None:
    axs[row, column].set_title(subtitle)
    axs[row, column].hist(data, edgecolor="black")


def set_subplot_plot(data_x_axis: pd.Series, data_y_axis: pd.Series, subtitle_x_axis: str,
                     subtitle_y_axis: str, axs, row: int, column: int) -> None:
    axs[row, column].set(xlabel=subtitle_x_axis, ylabel=subtitle_y_axis)
    axs[row, column].plot(data_x_axis, data_y_axis)


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
        with open(ANALYSIS_RESULTS_DIR + LATEX_IMAGE_FILENAME, "a", encoding=UTF_8) as file:
            file.write(f"{latex_generator.generate_chart_image(filename, False)}\n\n")
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
