from __future__ import annotations

from typing import List

import pandas as pd
from nameof import nameof
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder

from module.model.Offer import Offer


class FeatureExtractor:

    def __init__(self, offers: List[Offer]) -> None:
        super().__init__()
        self.offers = offers
        self.dataset: pd.DataFrame = pd.DataFrame()


    def insert_elementary_columns(self) -> FeatureExtractor:
        columns: List = [self._get_feature_values(offer) for offer in self.offers]
        column_names: List[str] = self._get_feature_names(self.offers[0])

        self.dataset = pd.DataFrame(columns, columns=column_names)
        return self


    def insert_extracted_features(self) -> FeatureExtractor:
        column_names: List[str] = [
            # "", "", "", "", ""
        ]

        columns: List = [

        ]

        for column_name, column in zip(column_names, columns):
            self.dataset[column_name] = column

        return self


    def prepare_dataset(self) -> pd.DataFrame:
        non_numeric_feature_names: List[str] = [
            nameof(self.offers[0].has_return_option),
            # nameof(self.offers[0].reviews[0].contains_images),
        ]

        label_encoder = LabelEncoder()
        for name in non_numeric_feature_names:
            self.dataset[name] = label_encoder.fit_transform(self.dataset[name])

        self.dataset = self.dataset.astype(float)
        return pd.DataFrame(
            data=preprocessing.normalize(self.dataset), columns=self.dataset.columns
        )


    def _get_feature_values(self, offer: Offer) -> List:
        return [
            offer.price,
            offer.has_return_option,
            offer.description_length,
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
