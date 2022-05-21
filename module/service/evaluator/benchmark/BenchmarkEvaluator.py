from typing import Dict, List, Tuple

from module.model.Offer import Offer
from module.model.Statistics import Statistics
from module.service.evaluator.Evaluator import Evaluator
from module.service.evaluator.benchmark.BenchmarkFeatureExtractor import BenchmarkFeatureExtractor
from module.utils import display_and_log_error, display_and_log_info


class BenchmarkEvaluator(Evaluator):
    CREDIBILITY_THRESHOLD_PARAM_KEY: str = "credibility_threshold"


    def __init__(self, offers: List[Offer], params: Dict[str, float]) -> None:
        super().__init__(offers, params)
        self.are_required_params_exist(params)

        self.credibility_threshold = params[BenchmarkEvaluator.CREDIBILITY_THRESHOLD_PARAM_KEY]
        self.polarity_threshold = params[BenchmarkFeatureExtractor.POLARITY_THRESHOLD_PARAM_KEY]
        display_and_log_info(self.logger, "Extracting features and preparing dataset...")
        self.dataset: List[Tuple[Offer, float]] = (
            BenchmarkFeatureExtractor(self.offers, self.polarity_threshold)
                .calculate_score()
                .get_dataset()
        )
        display_and_log_info(self.logger, "Features extracted and dataset prepared")


    def evaluate(self) -> Tuple[Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]], Statistics]:
        credible_offers: Tuple[List[Offer], bool] = ([], True)
        not_credible_offers: Tuple[List[Offer], bool] = ([], False)

        for offer, score in self.dataset:
            if score > self.credibility_threshold:
                credible_offers[0].append(offer)
            else:
                not_credible_offers[0].append(offer)

        result = (credible_offers, not_credible_offers)
        offers_count: int = len(credible_offers[0]) + len(not_credible_offers[0])
        return result, Statistics(offers_count)


    def are_required_params_exist(self, params: Dict[str, float]) -> None:
        required_params_keys: List[str] = [
            BenchmarkEvaluator.CREDIBILITY_THRESHOLD_PARAM_KEY,
            BenchmarkFeatureExtractor.POLARITY_THRESHOLD_PARAM_KEY
        ]

        if not all(required_params_key in params.keys() for required_params_key in required_params_keys):
            display_and_log_error(
                self.logger,
                f"ERROR: Argument 'params' must contains following keys {required_params_keys} !!!"
            )
