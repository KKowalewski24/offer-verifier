from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from langdetect import detect
from nameof import nameof
from nltk import WordNetLemmatizer, word_tokenize
from nltk.corpus import stopwords
from nrclex import NRCLex
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder

from module.constants import LANGDETECT_ENGLISH
from module.model.Offer import Offer
from module.service.common.Logger import Logger
from module.utils import display_and_log_info, list_to_string, remove_dict_entry_by_key

'''
Order of calling method (fluent api) from MeansFeatureExtractor may be confusing, at first 
`insert_elementary_columns` should be called, then `normalize_dataset` and then `insert_extracted_features` 
because extracted features are already normalized. Final step is to get dataset by calling `get_dataset`. 
'''


class MeansFeatureExtractor:

    def __init__(self, offers: List[Offer]) -> None:
        super().__init__()
        self.logger = Logger().get_logging_instance()
        self.offers = offers
        self.dataset: pd.DataFrame = pd.DataFrame()
        self.stopwords = stopwords.words("english")


    def insert_elementary_columns(self) -> MeansFeatureExtractor:
        display_and_log_info(self.logger, f"Started insert_elementary_columns...")
        columns: List = [self._get_feature_values(offer) for offer in self.offers]
        column_names: List[str] = self._get_feature_names(self.offers[0])

        self.dataset = pd.DataFrame(columns, columns=column_names)

        display_and_log_info(self.logger, f"Finished insert_elementary_columns")
        return self


    def normalize_dataset(self) -> MeansFeatureExtractor:
        display_and_log_info(self.logger, f"Started normalize_dataset...")
        non_numeric_feature_names: List[str] = [nameof(self.offers[0].has_return_option)]

        label_encoder = LabelEncoder()
        for name in non_numeric_feature_names:
            self.dataset[name] = label_encoder.fit_transform(self.dataset[name])

        self.dataset = self.dataset.astype(float)
        self.dataset = pd.DataFrame(
            data=preprocessing.normalize(self.dataset),
            columns=self.dataset.columns
        )

        display_and_log_info(self.logger, f"Finished normalize_dataset")
        return self


    def insert_extracted_features(self) -> MeansFeatureExtractor:
        display_and_log_info(self.logger, f"Started insert_extracted_features...")
        self._fix_not_valid_reviews()

        emotions_column_names, emotions_columns = self._get_emotions_from_text_content()

        if len(emotions_columns) != len(emotions_column_names):
            raise Exception(
                f"{nameof(emotions_columns)} and {nameof(emotions_column_names)} must have equal size!"
            )

        for column_name, column in zip(emotions_column_names, emotions_columns):
            self.dataset[str(column_name)] = column

        display_and_log_info(self.logger, f"Finished insert_extracted_features")
        return self


    def get_dataset(self) -> pd.DataFrame:
        return self.dataset


    def _get_emotions_from_text_content(self) -> Tuple[List[str], List[List[float]]]:
        emotions_column_names: List[List[str]] = []
        emotions_columns: List[List[float]] = []

        for offer in self.offers:
            reviews_emotions: List[Dict] = [
                remove_dict_entry_by_key(
                    NRCLex(self._prepare_text(review.text_content)).affect_frequencies,
                    "anticip"
                )
                for review in offer.reviews
            ]

            if len(reviews_emotions) == 0:
                continue

            mean: pd.Series = pd.DataFrame(
                data=[emotions.values() for emotions in reviews_emotions],
                columns=reviews_emotions[0].keys()
            ).mean()

            emotions_column_names.append(mean.index.to_list())
            emotions_columns.append(mean.to_list())

        emotions_columns_ndarray = np.array(emotions_columns)
        rotated_emotions_columns = [
            list(emotions_columns_ndarray[:, index])
            for index in range(emotions_columns_ndarray.shape[1])
        ]

        return list(np.unique(emotions_column_names)), rotated_emotions_columns


    def _prepare_text(self, text: str) -> str:
        return list_to_string([
            WordNetLemmatizer().lemmatize(x)
            for x in word_tokenize(text.casefold())
            if x.isalpha() and x not in self.stopwords
        ])


    def _fix_not_valid_reviews(self) -> None:
        for offer in self.offers:
            for review in offer.reviews:
                if review.text_content != "" and not self._is_english_language(review.text_content):
                    review.text_content = ""


    def _is_english_language(self, text: str) -> bool:
        return detect(text) == LANGDETECT_ENGLISH


    def _get_feature_values(self, offer: Offer) -> List:
        return [
            offer.price,
            offer.has_return_option,
            offer.description_length,
            offer.seller.feedback_score,
            offer.seller.seller_feedback_percentage,
            offer.seller.year_of_joining,
            offer.seller.seller_positive_ratings_number,
            offer.seller.seller_neutral_ratings_number,
            offer.seller.seller_negative_ratings_number,
            offer.seller.accurate_description,
            offer.seller.reasonable_shipping_cost,
            offer.seller.shipping_speed,
            offer.seller.communication,
        ]


    def _get_feature_names(self, offer: Offer) -> List[str]:
        return [
            nameof(offer.price),
            nameof(offer.has_return_option),
            nameof(offer.description_length),
            nameof(offer.seller.feedback_score),
            nameof(offer.seller.seller_feedback_percentage),
            nameof(offer.seller.year_of_joining),
            nameof(offer.seller.seller_positive_ratings_number),
            nameof(offer.seller.seller_neutral_ratings_number),
            nameof(offer.seller.seller_negative_ratings_number),
            nameof(offer.seller.accurate_description),
            nameof(offer.seller.reasonable_shipping_cost),
            nameof(offer.seller.shipping_speed),
            nameof(offer.seller.communication),
        ]
