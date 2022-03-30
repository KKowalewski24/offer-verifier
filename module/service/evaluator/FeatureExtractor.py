from __future__ import annotations, annotations

from abc import ABC
from typing import List

import pandas as pd
from langdetect import detect
from nltk import WordNetLemmatizer, word_tokenize
from nltk.corpus import stopwords

from module.constants import LANGDETECT_ENGLISH
from module.model.Offer import Offer
from module.service.common.Logger import Logger
from module.utils import list_to_string


class FeatureExtractor(ABC):

    def __init__(self, offers: List[Offer]) -> None:
        super().__init__()
        self.logger = Logger().get_logging_instance()
        self.offers = offers
        self.dataset: pd.DataFrame = pd.DataFrame()
        self.stopwords = stopwords.words("english")


    def get_dataset(self) -> pd.DataFrame:
        return self.dataset


    def prepare_text(self, text: str) -> str:
        return list_to_string([
            WordNetLemmatizer().lemmatize(x)
            for x in word_tokenize(text.casefold())
            if x.isalpha() and x not in self.stopwords
        ])


    def fix_not_valid_reviews(self) -> None:
        for offer in self.offers:
            for review in offer.reviews:
                if review.text_content != "" and not self.is_english_language(review.text_content):
                    review.text_content = ""


    def is_english_language(self, text: str) -> bool:
        return detect(text) == LANGDETECT_ENGLISH
