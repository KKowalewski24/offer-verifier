import numpy as np
import pandas as pd
from fcmeans import FCM

from module.service.evaluator.Clusterizer import Clusterizer
from module.service.evaluator.clustering.MeansClusterizer import MeansClusterizer


class FuzzyCMeansClusterizer(MeansClusterizer):

    def perform_means_clusterization(self, dataset: pd.DataFrame) -> None:
        fcm = FCM(n_clusters=MeansClusterizer.K_PARAM)
        fcm.random_state = Clusterizer.RANDOM_STATE
        fcm.fit(dataset.to_numpy())
        self.cluster_labels: np.ndarray = fcm.predict(dataset.to_numpy())
