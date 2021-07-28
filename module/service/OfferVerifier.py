from typing import List, Tuple

from module.constants import OFFERS_PATH, PICKLE_EXTENSION
from module.exception.ChoosingCredibleOfferNotPossibleException import \
    ChoosingCredibleOfferNotPossibleException
from module.exception.VerificationImpossibleException import VerificationImpossibleException
from module.model.Offer import Offer
from module.model.Statistics import Statistics
from module.service.Clusterizer import Clusterizer
from module.service.RequestProvider import RequestProvider
from module.utils import get_filename, save_object_to_file


class OfferVerifier:

    def __init__(self, search_phrase: str, save_offers: bool) -> None:
        self.search_phrase = search_phrase
        self.save_offers = save_offers
        self.request_provider: RequestProvider = RequestProvider(self.search_phrase)


    def verify(self) -> Tuple[Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]], Statistics]:
        print("Downloading offers, Please wait ...")
        offers: List[Offer] = self.request_provider.get_offers()
        if self.save_offers:
            save_object_to_file(
                get_filename(OFFERS_PATH + self.search_phrase, PICKLE_EXTENSION), offers)

        print("Downloading offers done!")
        clusterizer: Clusterizer = Clusterizer(offers)
        try:
            print("Performing the analysis of the offers, Please wait ...")
            combined_offers, statistics = clusterizer.clusterize()
            verified_offers = self._choose_list_with_more_credible_offers(combined_offers)
            print("Analysis of the offers done!")
        except ChoosingCredibleOfferNotPossibleException:
            raise VerificationImpossibleException

        return verified_offers, statistics


    def _choose_list_with_more_credible_offers(
            self, combined_offers: Tuple[List[Offer], List[Offer]]
    ) -> Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]]:
        # TODO
        # first_list_offers, second_list_offers = combined_offers
        pass
