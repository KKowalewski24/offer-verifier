from abc import abstractmethod
from typing import List

from module.model.BaseItem import BaseItem


class AnalyzableItem(BaseItem):

    def __init__(self, id: str) -> None:
        super().__init__(id)


    @abstractmethod
    def get_feature_values(self) -> List:
        pass


    @abstractmethod
    def get_feature_names(self) -> List[str]:
        pass


    @abstractmethod
    def get_non_numeric_feature_names(self) -> List[str]:
        pass
