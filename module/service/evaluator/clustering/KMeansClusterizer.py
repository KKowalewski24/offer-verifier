import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

from module.service.evaluator.Clusterizer import Clusterizer
from module.service.evaluator.clustering.MeansClusterizer import MeansClusterizer


class KMeansClusterizer(MeansClusterizer):

    def perform_means_clusterization(self, dataset: pd.DataFrame) -> None:
        k_means: KMeans = KMeans(
            n_clusters=MeansClusterizer.K_PARAM, random_state=Clusterizer.RANDOM_STATE
        )
        self.cluster_labels: np.ndarray = k_means.fit_predict(dataset)
