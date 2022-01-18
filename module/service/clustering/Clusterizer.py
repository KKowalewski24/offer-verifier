from abc import abstractmethod
from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.metrics import calinski_harabasz_score, davies_bouldin_score, silhouette_score
from sklearn.preprocessing import LabelEncoder

from module.model.Offer import Offer
from module.model.Statistics import Statistics
from module.service.Logger import Logger


class Clusterizer:
    RANDOM_STATE: int = 21


    def __init__(self, offers: List[Offer]) -> None:
        self.logger = Logger().get_logging_instance()
        self.offers = offers
        self.cluster_labels: np.ndarray = np.ndarray([])
        self.feature_names: List[str] = []
        self.non_numeric_feature_names: List[str] = []

        if self.offers is not None and len(self.offers) != 0:
            self.feature_names = self.offers[0].get_feature_names()
            self.non_numeric_feature_names = self.offers[0].get_non_numeric_feature_names()


    @abstractmethod
    def clusterize(self) -> Tuple[Tuple[List[Offer], List[Offer]], Statistics]:
        pass


    def _combine_offers(
            self, dataset: pd.DataFrame
    ) -> Tuple[Tuple[List[Offer], List[Offer]], Statistics]:
        # Combine offers and assigned cluster numbers - in theory number of
        # offers and array with cluster numbers should have equal length and it should be
        # in same order that is why it is merged
        combined_offers: List[Tuple[Offer, int]] = list(zip(self.offers, self.cluster_labels))
        return (
            (
                [combined_offer[0] for combined_offer in combined_offers if combined_offer[1] == 0],
                [combined_offer[0] for combined_offer in combined_offers if combined_offer[1] == 1]
            ),
            self._calculate_statistics(dataset)
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


    def _calculate_statistics(self, dataset: pd.DataFrame) -> Statistics:
        return Statistics(
            dataset.shape[0],
            round(silhouette_score(dataset, self.cluster_labels), 3),
            round(calinski_harabasz_score(dataset, self.cluster_labels), 3),
            round(davies_bouldin_score(dataset, self.cluster_labels), 3)
        )
