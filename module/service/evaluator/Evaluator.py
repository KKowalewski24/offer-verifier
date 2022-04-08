from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

from module.model.Offer import Offer
from module.model.Statistics import Statistics
from module.service.common.Logger import Logger


class Evaluator(ABC):
    RANDOM_STATE: int = 21


    def __init__(self, offers: List[Offer], params: Dict[str, float] = {}) -> None:
        self.logger = Logger().get_logging_instance()
        self.offers = offers
        self.params = params


    @abstractmethod
    def evaluate(self) -> Tuple[Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]], Statistics]:
        pass
