from __future__ import annotations, annotations

from typing import Dict, List

from nameof import nameof

from module.model.Offer import Offer
from module.utils import to_string_class_formatter


class OffersWrapper:
    OFFERS_KEY: str = "offers"
    DATASET_NAME_KEY: str = "dataset_name"


    def __init__(self, offers: List[Offer], dataset_name: str = "") -> None:
        self.offers = offers
        self.dataset_name = dataset_name


    def __str__(self) -> str:
        return super().__str__() + to_string_class_formatter(
            [self.offers, self.dataset_name],
            [nameof(self.offers), nameof(self.dataset_name)],
            "\n"
        )


    @staticmethod
    def from_dict(json_data: Dict) -> OffersWrapper:
        return OffersWrapper(
            [Offer.from_dict(json_offer) for json_offer in json_data[OffersWrapper.OFFERS_KEY]],
            json_data[OffersWrapper.DATASET_NAME_KEY]
        )
