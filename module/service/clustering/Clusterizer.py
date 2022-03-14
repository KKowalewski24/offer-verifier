from abc import abstractmethod
from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.metrics import calinski_harabasz_score, davies_bouldin_score, silhouette_score

from module.model.Offer import Offer
from module.model.Statistics import Statistics
from module.service.clustering.FeatureExtractor import FeatureExtractor
from module.service.common.Logger import Logger
from module.utils import display_and_log_info


class Clusterizer:
    RANDOM_STATE: int = 21


    def __init__(self, offers: List[Offer]) -> None:
        self.logger = Logger().get_logging_instance()
        self.offers = offers
        self.cluster_labels: np.ndarray = np.ndarray([])

        display_and_log_info(self.logger, "Extracting features and preparing dataset")
        self.dataset: pd.DataFrame = FeatureExtractor(self.offers).extract().prepare_dataset()
        display_and_log_info(self.logger, "Features extracted and dataset prepared")


    @abstractmethod
    def clusterize(self) -> Tuple[Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]], Statistics]:
        pass


    def _calculate_statistics(self, dataset: pd.DataFrame, execution_time: float) -> Statistics:
        # TODO ADD MORE STATISTICS
        return Statistics(
            dataset.shape[0],
            round(silhouette_score(dataset, self.cluster_labels), 3),
            round(calinski_harabasz_score(dataset, self.cluster_labels), 3),
            round(davies_bouldin_score(dataset, self.cluster_labels), 3),
            execution_time
        )
