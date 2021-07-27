from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import calinski_harabasz_score, davies_bouldin_score, silhouette_score

from module.model.Offer import Offer
from module.model.Statistics import Statistics

RANDOM_STATE: int = 21
K_RANGE: range = range(2, 20)


class Clusterizer:

    def __init__(self, offers: List[Offer]) -> None:
        self.offers = offers


    def clusterize(self) -> Tuple[Tuple[List[Offer], List[Offer]], Statistics]:
        dataset: pd.DataFrame = self._prepare_dataset()

        # K is set to 2 in order to always get 2 clusters whether it is optimal or not
        k_param: int = 2
        k_means: KMeans = KMeans(
            n_clusters=k_param, random_state=RANDOM_STATE
        )
        cluster_labels: np.ndarray = k_means.fit_predict(dataset)

        # Combine offers and assigned cluster numbers - in theory number of
        # offers and array with cluster numbers should have equal length and it should be
        # in same order that is why it is merged
        combined_offers: List[Tuple[Offer, int]] = list(zip(self.offers, cluster_labels))
        return (
            (
                [combined_offer[0] for combined_offer in combined_offers if combined_offer[1] == 0],
                [combined_offer[0] for combined_offer in combined_offers if combined_offer[1] == 1]
            ),
            self._calculate_statistics(dataset, cluster_labels)
        )


    def _prepare_dataset(self) -> pd.DataFrame:
        # TODO
        pass


    def _calculate_statistics(self, dataset: pd.DataFrame, cluster_labels: np.ndarray) -> Statistics:
        return Statistics(
            round(silhouette_score(dataset, cluster_labels), 3),
            round(calinski_harabasz_score(dataset, cluster_labels), 3),
            round(davies_bouldin_score(dataset, cluster_labels), 3)
        )
