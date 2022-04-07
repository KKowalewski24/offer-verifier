from __future__ import annotations, annotations

from abc import ABC
from typing import List

import numpy as np
import pandas as pd
from langdetect import detect
from nltk import WordNetLemmatizer, word_tokenize
from nltk.corpus import stopwords
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder

from module.constants import LANGDETECT_ENGLISH
from module.model.Offer import Offer
from module.service.common.Logger import Logger
from module.utils import list_to_string


class FeatureExtractor(ABC):

    def __init__(self, offers: List[Offer]) -> None:
        super().__init__()
        self.logger = Logger().get_logging_instance()
        self.offers = offers
        self.stopwords = stopwords.words("english")


    def _normalize_array(self, items: np.ndarray) -> List:
        if items.size == 0:
            return list(items)
        return list((items - items.min()) / (items.max() - items.min()))


    def _normalize_single_value_on_range(self, value: float, range_begin: float, range_end: float) -> float:
        return (value - range_begin) / (range_end - range_begin)


    def _encode_columns(self, dataset: pd.DataFrame, column_names: List[str]) -> pd.DataFrame:
        label_encoder = LabelEncoder()
        for name in column_names:
            dataset[name] = label_encoder.fit_transform(dataset[name])

        return dataset


    def _normalize_columns(self, dataset: pd.DataFrame) -> pd.DataFrame:
        dataset = dataset.astype(float)
        return pd.DataFrame(
            data=preprocessing.normalize(dataset),
            columns=dataset.columns
        )


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
