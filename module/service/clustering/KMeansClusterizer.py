from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

from module.model.Offer import Offer
from module.model.Statistics import Statistics
from module.service.clustering.Clusterizer import Clusterizer
from module.utils import display_and_log_info


class KMeansClusterizer(Clusterizer):

    def clusterize(self) -> Tuple[Tuple[List[Offer], List[Offer]], Statistics]:
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

        return self._combine_offers(dataset)
