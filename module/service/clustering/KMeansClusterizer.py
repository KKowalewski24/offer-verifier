import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

from module.service.clustering.Clusterizer import Clusterizer
from module.service.clustering.MeansClusterizer import MeansClusterizer


class KMeansClusterizer(MeansClusterizer):

    def perform_means_clusterization(self, dataset: pd.DataFrame) -> None:
        # K is set to 2 in order to always get 2 clusters whether it is optimal or not
        k_param: int = 2
        k_means: KMeans = KMeans(
            n_clusters=k_param, random_state=Clusterizer.RANDOM_STATE
        )
        self.cluster_labels: np.ndarray = k_means.fit_predict(dataset)
