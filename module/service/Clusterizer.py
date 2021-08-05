from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import calinski_harabasz_score, davies_bouldin_score, silhouette_score
from sklearn.preprocessing import LabelEncoder

from module.model.Offer import Offer
from module.model.Statistics import Statistics
from module.service.Logger import Logger
from module.utils import display_and_log

RANDOM_STATE: int = 21


class Clusterizer:

    def __init__(self, offers: List[Offer]) -> None:
        self.logger = Logger().get_logging_instance()
        self.offers = offers
        self.feature_names: List[str] = []
        self.non_numeric_feature_names: List[str] = []

        if self.offers is not None and len(self.offers) != 0:
            self.feature_names = self.offers[0].get_feature_names()
            self.non_numeric_feature_names = self.offers[0].get_non_numeric_feature_names()


    def clusterize(self) -> Tuple[Tuple[List[Offer], List[Offer]], Statistics]:
        display_and_log(self.logger, "Preparing dataset")
        dataset: pd.DataFrame = self._prepare_dataset()
        display_and_log(self.logger, "Dataset prepared")

        # K is set to 2 in order to always get 2 clusters whether it is optimal or not
        k_param: int = 2
        display_and_log(self.logger, "Clustering started")
        k_means: KMeans = KMeans(
            n_clusters=k_param, random_state=RANDOM_STATE
        )
        cluster_labels: np.ndarray = k_means.fit_predict(dataset)
        display_and_log(self.logger, "Clustering finished")

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
        df: pd.DataFrame = pd.DataFrame(
            [offer.get_feature_values() for offer in self.offers],
            columns=self.feature_names
        )

        label_encoder = LabelEncoder()
        for name in self.non_numeric_feature_names:
            df[name] = label_encoder.fit_transform(df[name])

        return df


    def _calculate_statistics(self, dataset: pd.DataFrame, cluster_labels: np.ndarray) -> Statistics:
        return Statistics(
            round(silhouette_score(dataset, cluster_labels), 3),
            round(calinski_harabasz_score(dataset, cluster_labels), 3),
            round(davies_bouldin_score(dataset, cluster_labels), 3)
        )
