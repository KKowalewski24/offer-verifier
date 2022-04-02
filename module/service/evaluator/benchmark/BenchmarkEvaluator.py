import time
from typing import List, Tuple

from module.model.Offer import Offer
from module.model.Statistics import Statistics
from module.service.evaluator.Evaluator import Evaluator
from module.service.evaluator.benchmark.BenchmarkFeatureExtractor import BenchmarkFeatureExtractor


class BenchmarkEvaluator(Evaluator):
    CREDIBILITY_THRESHOLD: float = 2.8


    def __init__(self, offers: List[Offer]) -> None:
        super().__init__(offers)
        self.dataset: List[Tuple[Offer, float]] = (
            BenchmarkFeatureExtractor(self.offers)
                .calculate_score()
                .get_dataset()
        )


    def evaluate(self) -> Tuple[Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]], Statistics]:
        start_time = time.time()

        credible_offers: Tuple[List[Offer], bool] = ([], True)
        not_credible_offers: Tuple[List[Offer], bool] = ([], False)

        for offer, score in self.dataset:
            if score > BenchmarkEvaluator.CREDIBILITY_THRESHOLD:
                credible_offers[0].append(offer)
            else:
                not_credible_offers[0].append(offer)

        result = (credible_offers, not_credible_offers)

        end_time = time.time()
        execution_time = end_time - start_time

        offers_count: int = len(credible_offers[0]) + len(not_credible_offers[0])
        return result, Statistics(offers_count, execution_time)
