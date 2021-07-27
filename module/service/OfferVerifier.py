from typing import List, Tuple

from module.exception.ChoosingCredibleOfferNotPossibleException import \
    ChoosingCredibleOfferNotPossibleException
from module.exception.VerificationImpossibleException import VerificationImpossibleException
from module.model.Offer import Offer
from module.model.Statistics import Statistics
from module.service.Clusterizer import Clusterizer
from module.service.RequestProvider import RequestProvider


class OfferVerifier:

    def __init__(self, search_phrase: str) -> None:
        self.request_provider: RequestProvider = RequestProvider(search_phrase)


    def verify(self) -> Tuple[Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]], Statistics]:
        offers: List[Offer] = self.request_provider.get_offers()
        clusterizer: Clusterizer = Clusterizer(offers)
        try:
            combined_offers, statistics = clusterizer.clusterize()
            verified_offers = self._choose_list_with_more_credible_offers(combined_offers)
        except ChoosingCredibleOfferNotPossibleException:
            raise VerificationImpossibleException

        return verified_offers, statistics


    def _choose_list_with_more_credible_offers(
            self, combined_offers: Tuple[List[Offer], List[Offer]]
    ) -> Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]]:
        # TODO
        # first_list_offers, second_list_offers = combined_offers
        pass
