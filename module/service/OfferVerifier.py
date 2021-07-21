from typing import List, Tuple

from module.model.Offer import Offer
from module.model.Statistics import Statistics
from module.service.request.RequestProvider import RequestProvider


class OfferVerifier:

    def __init__(self, search_phrase: str) -> None:
        self.request_provider: RequestProvider = RequestProvider(search_phrase)


    def verify(self) -> Tuple[Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]], Statistics]:
        # TODO
        pass
