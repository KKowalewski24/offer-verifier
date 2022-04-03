from __future__ import annotations

from typing import List, Tuple

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
            credible_reviews: List[ProductReview] = []
            for review in offer.reviews:
                if self._is_credible_review(review):
                    credible_reviews.append(review)

            offer.reviews = credible_reviews
            score = pd.Series([review.stars_number for review in offer.reviews]).mean()
            self.dataset.append((offer, score))

        return self


    def get_dataset(self) -> List[Tuple[Offer, float]]:
        return self.dataset


    def _is_credible_review(self, review: ProductReview) -> bool:
        polarity: float = TextBlob(self._prepare_text(review.text_content)).sentiment.polarity
        # TODO
        return False
