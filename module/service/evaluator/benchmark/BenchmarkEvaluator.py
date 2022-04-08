import time
from typing import Dict, List, Tuple

from module.model.Offer import Offer
from module.model.Statistics import Statistics
from module.service.evaluator.Evaluator import Evaluator
from module.service.evaluator.benchmark.BenchmarkFeatureExtractor import BenchmarkFeatureExtractor


class BenchmarkEvaluator(Evaluator):
    CREDIBILITY_THRESHOLD_PARAM_KEY: str = "credibility_threshold"


    def __init__(self, offers: List[Offer], params: Dict[str, float] = {}) -> None:
        super().__init__(offers, params)
        self.credibility_threshold = params[BenchmarkEvaluator.CREDIBILITY_THRESHOLD_PARAM_KEY]
        self.polarity_threshold = params[BenchmarkFeatureExtractor.POLARITY_THRESHOLD_PARAM_KEY]
        self.dataset: List[Tuple[Offer, float]] = (
            BenchmarkFeatureExtractor(self.offers, self.polarity_threshold)
                .calculate_score()
                .get_dataset()
        )


    def evaluate(self) -> Tuple[Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]], Statistics]:
        start_time = time.time()

        credible_offers: Tuple[List[Offer], bool] = ([], True)
        not_credible_offers: Tuple[List[Offer], bool] = ([], False)

        for offer, score in self.dataset:
            if score > self.credibility_threshold:
                credible_offers[0].append(offer)
            else:
                not_credible_offers[0].append(offer)

        result = (credible_offers, not_credible_offers)

        end_time = time.time()
        execution_time = end_time - start_time

        offers_count: int = len(credible_offers[0]) + len(not_credible_offers[0])
        return result, Statistics(offers_count, execution_time)
