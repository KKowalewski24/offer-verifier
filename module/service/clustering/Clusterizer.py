from abc import abstractmethod
from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.metrics import calinski_harabasz_score, davies_bouldin_score, silhouette_score
from sklearn.preprocessing import LabelEncoder

from module.model.Offer import Offer
from module.model.Statistics import Statistics
from module.service.common.Logger import Logger


class Clusterizer:
    RANDOM_STATE: int = 21


    def __init__(self, offers: List[Offer]) -> None:
        self.logger = Logger().get_logging_instance()
        self.offers = offers
        self.cluster_labels: np.ndarray = np.ndarray([])


    @abstractmethod
    def clusterize(self) -> Tuple[Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]], Statistics]:
        pass


    def _prepare_dataset(self) -> pd.DataFrame:
        # df: pd.DataFrame = pd.DataFrame(
        #     [offer.get_feature_values() for offer in self.offers],
        #     columns=self.feature_names
        # )
        #
        # label_encoder = LabelEncoder()
        # for name in self.non_numeric_feature_names:
        #     df[name] = label_encoder.fit_transform(df[name])
        #
        # df = df.astype(float)
        # return pd.DataFrame(data=preprocessing.normalize(df), columns=df.columns)
        return pd.DataFrame()


    def _calculate_statistics(self, dataset: pd.DataFrame, execution_time: float) -> Statistics:
        # TODO ADD MORE STATISTICS
        return Statistics(
            dataset.shape[0],
            round(silhouette_score(dataset, self.cluster_labels), 3),
            round(calinski_harabasz_score(dataset, self.cluster_labels), 3),
            round(davies_bouldin_score(dataset, self.cluster_labels), 3),
            execution_time
        )
