from __future__ import annotations

from typing import List, Tuple

import numpy as np
import pandas as pd
from textblob import TextBlob

from module.constants import MIN_MAX_REVIEW_VALUE
from module.model.Offer import Offer
from module.model.ProductReview import ProductReview
from module.service.evaluator.FeatureExtractor import FeatureExtractor


class BenchmarkFeatureExtractor(FeatureExtractor):
    POLARITY_THRESHOLD_PARAM_KEY: str = "polarity_thrld"


    def __init__(self, offers: List[Offer], polarity_threshold: float) -> None:
        super().__init__(offers)
        self.dataset: List[Tuple[Offer, float]] = []
        self.polarity_threshold = polarity_threshold


    def calculate_score(self) -> BenchmarkFeatureExtractor:
        self._fix_not_valid_reviews()

        for offer in self.offers:
            normalized_stars_numbers = self._normalize_array(
                np.array([review.stars_number for review in offer.reviews]),
                MIN_MAX_REVIEW_VALUE[0], MIN_MAX_REVIEW_VALUE[1]
            )

            credible_reviews: List[ProductReview] = [
                review for stars_number, review in zip(normalized_stars_numbers, offer.reviews)
                if self._is_credible_review(stars_number, review.text_content)
            ]

            offer.reviews = credible_reviews
            score = pd.Series([review.stars_number for review in offer.reviews], dtype=float).mean()
            self.dataset.append((offer, score))

        return self


    def get_dataset(self) -> List[Tuple[Offer, float]]:
        return self.dataset


    def _is_credible_review(self, normalized_stars_number: int, text_content: str) -> bool:
        if text_content == "":
            return True

        polarity: float = TextBlob(self._prepare_text(text_content)).sentiment.polarity
        normalized_polarity: float = self._normalize_single_value_on_range(polarity, -1, 1)

        left_side = normalized_polarity - self.polarity_threshold
        right_side = normalized_polarity + self.polarity_threshold
        return left_side < normalized_stars_number < right_side
