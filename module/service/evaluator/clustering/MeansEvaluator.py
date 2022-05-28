from abc import abstractmethod
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

from module.exception.ChoosingCredibleOfferNotPossibleException import \
    ChoosingCredibleOfferNotPossibleException
from module.model.Offer import Offer
from module.model.ProductReview import ProductReview
from module.model.Statistics import Statistics
from module.service.evaluator.Evaluator import Evaluator
from module.service.evaluator.clustering.MeansFeatureExtractor import MeansFeatureExtractor
from module.utils import display_and_log_info


class MeansEvaluator(Evaluator):
    # K is set to 2 in order to always get 2 clusters whether it is optimal or not
    K_PARAM: int = 2


    def __init__(self, offers: List[Offer], params: Dict[str, float]) -> None:
        super().__init__(offers, params)
        self.cluster_labels: np.ndarray = np.ndarray([])

        display_and_log_info(self.logger, "Extracting features and preparing dataset...")
        self.dataset: pd.DataFrame = (
            MeansFeatureExtractor(self.offers)
                .insert_elementary_columns()
                .normalize_dataset()
                .insert_extracted_features()
                .get_dataset()
        )
        display_and_log_info(self.logger, "Features extracted and dataset prepared")


    def evaluate(self) -> Tuple[Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]], Statistics]:
        display_and_log_info(self.logger, "Clustering started...")
        self.perform_means_clusterization(self.dataset)
        display_and_log_info(self.logger, "Clustering finished")

        result = self._choose_list_with_more_credible_offers(self._combine_offers())
        return result, Statistics(self.dataset.shape[0])


    @abstractmethod
    def perform_means_clusterization(self, dataset: pd.DataFrame) -> None:
        pass


    def _combine_offers(self) -> Tuple[List[Offer], List[Offer]]:
        # Combine offers and assigned cluster numbers - in theory number of
        # offers and array with cluster numbers should have equal length and it should be
        # in same order that is why it is merged
        combined_offers: List[Tuple[Offer, int]] = list(zip(self.offers, self.cluster_labels))
        return (
            [combined_offer[0] for combined_offer in combined_offers if combined_offer[1] == 0],
            [combined_offer[0] for combined_offer in combined_offers if combined_offer[1] == 1]
        )


    def _choose_list_with_more_credible_offers(
            self, combined_offers: Tuple[List[Offer], List[Offer]]
    ) -> Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]]:
        first_offers, second_offers = combined_offers
        first_average_stars_number: float = self._average_stars_number_for_offers_list(first_offers)
        second_average_stars_number: float = self._average_stars_number_for_offers_list(second_offers)
        display_and_log_info(self.logger, f"first_average_stars_number: {first_average_stars_number}")
        display_and_log_info(self.logger, f"second_average_stars_number: {second_average_stars_number}")

        if first_average_stars_number > second_average_stars_number:
            result = (first_offers, True), (second_offers, False)
        elif first_average_stars_number < second_average_stars_number:
            result = (second_offers, True), (first_offers, False)
        else:
            raise ChoosingCredibleOfferNotPossibleException(
                f"\nValue of first_average_stars_number: {first_average_stars_number}"
                f"\nValue of second_average_stars_number: {second_average_stars_number}"
            )

        return result


    def _average_stars_number_for_offers_list(self, offers: List[Offer]) -> float:
        reviews_mean = [self._calculate_reviews_mean(offer.reviews) for offer in offers]
        offers_mean = pd.Series(reviews_mean).dropna().tolist()
        offers_mean_sum = np.sum(offers_mean)
        offers_mean_len = len(offers_mean)
        return round(offers_mean_sum / offers_mean_len, 2)


    def _calculate_reviews_mean(self, reviews: List[ProductReview]) -> int:
        return pd.Series([review.stars_number for review in reviews], dtype=float).mean()
