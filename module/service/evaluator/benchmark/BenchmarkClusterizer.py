import time
from typing import List, Tuple

import pandas as pd

from module.model.Offer import Offer
from module.model.Statistics import Statistics
from module.service.evaluator.Clusterizer import Clusterizer


class BenchmarkClusterizer(Clusterizer):

    def __init__(self, offers: List[Offer]) -> None:
        super().__init__(offers)
        self.dataset: pd.DataFrame = pd.DataFrame({})


    def clusterize(self) -> Tuple[Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]], Statistics]:
        start_time = time.time()

        # TODO ADD REST OF IMPL
        result = ""

        end_time = time.time()
        execution_time = end_time - start_time

        return result, self._calculate_statistics(self.dataset, execution_time)
