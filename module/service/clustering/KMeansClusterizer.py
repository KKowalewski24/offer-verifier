from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

from module.exception.ChoosingCredibleOfferNotPossibleException import \
    ChoosingCredibleOfferNotPossibleException
from module.model.Offer import Offer
from module.model.Statistics import Statistics
from module.service.clustering.Clusterizer import Clusterizer
from module.utils import display_and_log_info


class KMeansClusterizer(Clusterizer):

    def clusterize(self) -> Tuple[Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]], Statistics]:
        display_and_log_info(self.logger, "Preparing dataset")
        dataset: pd.DataFrame = self._prepare_dataset()
        display_and_log_info(self.logger, "Dataset prepared")

        # K is set to 2 in order to always get 2 clusters whether it is optimal or not
        k_param: int = 2
        display_and_log_info(self.logger, "Clustering started")
        k_means: KMeans = KMeans(
            n_clusters=k_param, random_state=Clusterizer.RANDOM_STATE
        )
        self.cluster_labels: np.ndarray = k_means.fit_predict(dataset)
        display_and_log_info(self.logger, "Clustering finished")

        return (
            self._choose_list_with_more_credible_offers(self._combine_offers()),
            self._calculate_statistics(dataset)
        )


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
