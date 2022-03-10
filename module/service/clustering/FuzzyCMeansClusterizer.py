from module.service.clustering.MeansClusterizer import MeansClusterizer

from fcmeans import FCM
import pandas as pd


class FuzzyCMeansClusterizer(MeansClusterizer):
    RANDOM_STATE_VALUE = 21


    def perform_means_clusterization(self, dataset: pd.DataFrame) -> None:
        # TODO
        # fcm = FCM(**params)
        # fcm.random_state = FuzzyCMeansClusterizer.RANDOM_STATE_VALUE
        # fcm.fit(self.X)
        # self.y_pred = fcm.predict(self.X)
        pass
