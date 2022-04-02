from typing import List, Tuple

from module.model.Offer import Offer
from module.service.evaluator.FeatureExtractor import FeatureExtractor


class BenchmarkFeatureExtractor(FeatureExtractor):

    def __init__(self, offers: List[Offer]) -> None:
        super().__init__(offers)
        self.dataset: List[Tuple[Offer, float]] = []


    def get_dataset(self) -> List[Tuple[Offer, float]]:
        return self.dataset


    def _get_sentiment_polarity(self) -> None:
        pass
