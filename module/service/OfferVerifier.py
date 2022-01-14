import glob
from typing import List, Tuple

import numpy as np

from module.constants import OFFERS_PATH, PICKLE_EXTENSION, RESULTS_DIRECTORY
from module.exception.ChoosingCredibleOfferNotPossibleException import \
    ChoosingCredibleOfferNotPossibleException
from module.exception.VerificationImpossibleException import VerificationImpossibleException
from module.model.Offer import Offer
from module.model.Statistics import Statistics
from module.service.Logger import Logger
from module.service.RequestProvider import RequestProvider
from module.service.clustering.Clusterizer import Clusterizer
from module.service.clustering.KMeansClusterizer import KMeansClusterizer
from module.utils import display_and_log, get_filename, read_object_from_file, save_object_to_file


class OfferVerifier:

    def __init__(self, search_phrase: str, save_offers: bool) -> None:
        self.search_phrase = search_phrase
        self.save_offers = save_offers
        self.logger = Logger().get_logging_instance()
        self.request_provider: RequestProvider = RequestProvider(self.search_phrase)


    def verify(self) -> Tuple[Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]], Statistics]:
        display_and_log(self.logger, "Downloading offers, Please wait ...")
        # TODO Add True as param for using local file
        offers: List[Offer] = self.download_offers()

        display_and_log(self.logger, "Downloading offers done!")
        clusterizer: Clusterizer = KMeansClusterizer(offers)

        try:
            display_and_log(self.logger, "Performing the analysis of the offers, Please wait ...")
            combined_offers, statistics = clusterizer.clusterize()
            verified_offers = self._choose_list_with_more_credible_offers(combined_offers)
            display_and_log(self.logger, "Analysis of the offers done!")
        except ChoosingCredibleOfferNotPossibleException:
            raise VerificationImpossibleException

        return verified_offers, statistics


    def download_offers(self, read_from_file: bool = False) -> List[Offer]:
        offers: List[Offer] = []
        if read_from_file:
            offers = list(
                read_object_from_file(glob.glob(RESULTS_DIRECTORY + "*" + PICKLE_EXTENSION)[0])
            )
        else:
            offers = self.request_provider.get_offers()

        if self.save_offers and not read_from_file:
            save_object_to_file(
                get_filename(OFFERS_PATH + self.search_phrase, PICKLE_EXTENSION), offers)

        return offers


    def _choose_list_with_more_credible_offers(
            self, combined_offers: Tuple[List[Offer], List[Offer]]
    ) -> Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]]:
        first_list_offers, second_list_offers = combined_offers
        first_list_average_feedback_score: float = self._average_feedback_score(first_list_offers)
        second_list_average_feedback_score: float = self._average_feedback_score(second_list_offers)

        if first_list_average_feedback_score > second_list_average_feedback_score:
            result = (first_list_offers, True), (second_list_offers, False)
        elif first_list_average_feedback_score < second_list_average_feedback_score:
            result = (second_list_offers, True), (first_list_offers, False)
        else:
            raise ChoosingCredibleOfferNotPossibleException

        return result


    def _average_feedback_score(self, offers: List[Offer]) -> float:
        return round(np.sum([offer.seller.feedback_score for offer in offers]) / len(offers), 2)
