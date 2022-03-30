import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

from module.service.evaluator.Evaluator import Evaluator
from module.service.evaluator.clustering.MeansEvaluator import MeansEvaluator


class KMeansEvaluator(MeansEvaluator):

    def perform_means_clusterization(self, dataset: pd.DataFrame) -> None:
        k_means: KMeans = KMeans(
            n_clusters=MeansEvaluator.K_PARAM, random_state=Evaluator.RANDOM_STATE
        )
        self.cluster_labels: np.ndarray = k_means.fit_predict(dataset)
