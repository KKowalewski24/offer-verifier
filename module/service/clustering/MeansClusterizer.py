import time
from abc import abstractmethod
from typing import List, Tuple

import numpy as np
import pandas as pd

from module.exception.ChoosingCredibleOfferNotPossibleException import \
    ChoosingCredibleOfferNotPossibleException
from module.model.Offer import Offer
from module.model.ProductReview import ProductReview
from module.model.Statistics import Statistics
from module.service.clustering.Clusterizer import Clusterizer
from module.service.clustering.FeatureExtractor import FeatureExtractor
from module.utils import display_and_log_info


class MeansClusterizer(Clusterizer):
    # K is set to 2 in order to always get 2 clusters whether it is optimal or not
    K_PARAM: int = 2


    def __init__(self, offers: List[Offer]) -> None:
        super().__init__(offers)

        display_and_log_info(self.logger, "Extracting features and preparing dataset...")
        self.dataset: pd.DataFrame = (
            FeatureExtractor(self.offers)
                .insert_elementary_columns()
                .normalize_dataset()
                .insert_extracted_features()
                .get_dataset()
        )
        display_and_log_info(self.logger, "Features extracted and dataset prepared")


    def clusterize(self) -> Tuple[Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]], Statistics]:
        start_time = time.time()

        display_and_log_info(self.logger, "Clustering started...")
        self.perform_means_clusterization(self.dataset)
        display_and_log_info(self.logger, "Clustering finished")

        result = self._choose_list_with_more_credible_offers(self._combine_offers())

        end_time = time.time()
        execution_time = end_time - start_time

        return result, self._calculate_statistics(self.dataset, execution_time)


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

        if first_average_stars_number > second_average_stars_number:
            result = (first_offers, True), (second_offers, False)
        elif first_average_stars_number < second_average_stars_number:
            result = (second_offers, True), (first_offers, False)
        else:
            raise ChoosingCredibleOfferNotPossibleException()

        return result


    def _average_stars_number_for_offers_list(self, offers: List[Offer]) -> float:
        offers_mean_sum = np.sum([self._calculate_reviews_mean(offer.reviews) for offer in offers])
        return round(offers_mean_sum / len(offers), 2)


    def _calculate_reviews_mean(self, reviews: List[ProductReview]) -> int:
        return pd.Series([review.stars_number for review in reviews]).mean()
