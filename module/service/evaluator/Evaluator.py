from abc import ABC, abstractmethod
from typing import List, Tuple

import pandas as pd

from module.model.Offer import Offer
from module.model.Statistics import Statistics
from module.service.common.Logger import Logger


class Evaluator(ABC):
    RANDOM_STATE: int = 21


    def __init__(self, offers: List[Offer]) -> None:
        self.logger = Logger().get_logging_instance()
        self.offers = offers


    @abstractmethod
    def evaluate(self) -> Tuple[Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]], Statistics]:
        pass


    def _calculate_statistics(self, dataset: pd.DataFrame, execution_time: float) -> Statistics:
        # TODO ADD MORE STATISTICS
        return Statistics(
            dataset.shape[0],
            execution_time
        )