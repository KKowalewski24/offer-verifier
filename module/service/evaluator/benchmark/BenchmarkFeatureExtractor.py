from __future__ import annotations

from typing import List, Tuple

import numpy as np
import pandas as pd
from textblob import TextBlob

from module.model.Offer import Offer
from module.model.ProductReview import ProductReview
from module.service.evaluator.FeatureExtractor import FeatureExtractor


class BenchmarkFeatureExtractor(FeatureExtractor):

    def __init__(self, offers: List[Offer]) -> None:
        super().__init__(offers)
        self.dataset: List[Tuple[Offer, float]] = []


    def calculate_score(self) -> BenchmarkFeatureExtractor:
        self._fix_not_valid_reviews()

        for offer in self.offers:
            normalized_stars_numbers = self._normalize_array(
                np.array([review.stars_number for review in offer.reviews])
            )

            credible_reviews: List[ProductReview] = [
                review for stars_number, review in zip(normalized_stars_numbers, offer.reviews)
                if self._is_credible_review(stars_number, review.text_content)
            ]

            offer.reviews = credible_reviews
            score = pd.Series([review.stars_number for review in offer.reviews]).mean()
            self.dataset.append((offer, score))

        return self


    def get_dataset(self) -> List[Tuple[Offer, float]]:
        return self.dataset


    def _is_credible_review(self, normalized_stars_number: int, text_content: str) -> bool:
        if text_content == "":
            return True

        polarity: float = TextBlob(self._prepare_text(text_content)).sentiment.polarity
        normalized_polarity: float = self._normalize_single_value_on_range(polarity, -1, 1)

        if normalized_polarity - 0.2 < normalized_stars_number < normalized_polarity + 0.2:
            return True
        return False
