import time
from abc import abstractmethod
from typing import List, Tuple

import numpy as np
import pandas as pd

from module.exception.ChoosingCredibleOfferNotPossibleException import \
    ChoosingCredibleOfferNotPossibleException
from module.model.Offer import Offer
from module.model.Statistics import Statistics
from module.service.clustering.Clusterizer import Clusterizer
from module.utils import display_and_log_info


class MeansClusterizer(Clusterizer):
    # K is set to 2 in order to always get 2 clusters whether it is optimal or not
    K_PARAM: int = 2


    def clusterize(self) -> Tuple[Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]], Statistics]:
        start_time = time.time()

        display_and_log_info(self.logger, "Clustering started")
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
        first_list_offers, second_list_offers = combined_offers
        first_list_average_feedback_score: float = self._average_feedback_score(first_list_offers)
        second_list_average_feedback_score: float = self._average_feedback_score(second_list_offers)

        if first_list_average_feedback_score > second_list_average_feedback_score:
            result = (first_list_offers, True), (second_list_offers, False)
        elif first_list_average_feedback_score < second_list_average_feedback_score:
            result = (second_list_offers, True), (first_list_offers, False)
        else:
            raise ChoosingCredibleOfferNotPossibleException()

        return result


    def _average_feedback_score(self, offers: List[Offer]) -> float:
        return round(np.sum([offer.seller.feedback_score for offer in offers]) / len(offers), 2)
