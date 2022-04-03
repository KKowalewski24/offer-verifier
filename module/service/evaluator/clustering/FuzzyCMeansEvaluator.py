import numpy as np
import pandas as pd
from fcmeans import FCM

from module.service.evaluator.Evaluator import Evaluator
from module.service.evaluator.clustering.MeansEvaluator import MeansEvaluator


class FuzzyCMeansEvaluator(MeansEvaluator):

    def perform_means_clusterization(self, dataset: pd.DataFrame) -> None:
        fcm = FCM(n_clusters=MeansEvaluator.K_PARAM)
        fcm.random_state = Evaluator.RANDOM_STATE
        fcm.fit(dataset.to_numpy())
        self.cluster_labels: np.ndarray = fcm.predict(dataset.to_numpy())
