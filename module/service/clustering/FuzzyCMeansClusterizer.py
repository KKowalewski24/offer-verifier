from module.service.clustering.MeansClusterizer import MeansClusterizer

from fcmeans import FCM
import pandas as pd


class FuzzyCMeansClusterizer(MeansClusterizer):

    def perform_means_clusterization(self, dataset: pd.DataFrame) -> None:
        # TODO
        # fcm = FCM(**params)
        # fcm.random_state = Clusterizer.RANDOM_STATE
        # fcm.fit(self.X)
        # self.y_pred = fcm.predict(self.X)
        pass
