import time
from typing import List, Tuple

import pandas as pd

from module.model.Offer import Offer
from module.model.Statistics import Statistics
from module.service.clustering.Clusterizer import Clusterizer
from module.utils import display_and_log_info


class BenchmarkClusterizer(Clusterizer):

    def clusterize(self) -> Tuple[Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]], Statistics]:
        start_time = time.time()

        display_and_log_info(self.logger, "Preparing dataset")
        dataset: pd.DataFrame = self._prepare_dataset()
        display_and_log_info(self.logger, "Dataset prepared")

        # TODO ADD REST OF IMPL
        result = ""

        end_time = time.time()
        execution_time = end_time - start_time

        return result, self._calculate_statistics(dataset, execution_time)
