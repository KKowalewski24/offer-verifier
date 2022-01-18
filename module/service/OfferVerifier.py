from typing import Any, Callable, List, Tuple
from nameof import nameof
import numpy as np

from module.constants import OFFERS_PATH, PICKLE_EXTENSION
from module.exception.ChoosingCredibleOfferNotPossibleException import \
    ChoosingCredibleOfferNotPossibleException
from module.exception.VerificationImpossibleException import VerificationImpossibleException
from module.exception.WrongConstructorParams import WrongConstructorParams
from module.model.Offer import Offer
from module.model.Statistics import Statistics
from module.service.Logger import Logger
from module.service.RequestProvider import RequestProvider
from module.service.clustering.Clusterizer import Clusterizer
from module.service.clustering.KMeansClusterizer import KMeansClusterizer
from module.utils import display_and_log_error, display_and_log_info, display_and_log_warning, \
    get_filename, read_object_from_file, save_object_to_file


class OfferVerifier:

    def __init__(self, search_phrase: str = None,
                 path_to_local_file: str = None,
                 save_offers: bool = False,
                 clusterizer: Callable[[List[Offer]], Clusterizer] = KMeansClusterizer) -> None:
        self.logger = Logger().get_logging_instance()
        self.clusterizer: Callable[[Any], Clusterizer] = clusterizer
        self.search_phrase = search_phrase
        self.save_offers = save_offers
        self.path_to_local_file = path_to_local_file
        self._validate_init_params()


    def verify(self) -> Tuple[Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]], Statistics]:
        display_and_log_info(self.logger, "Downloading offers, Please wait ...")
        offers: List[Offer] = self.download_offers()
        display_and_log_info(self.logger, "Downloading offers done!")

        try:
            display_and_log_info(
                self.logger, "Performing the analysis of the offers, Please wait ..."
            )
            combined_offers, statistics = self.clusterizer(offers).clusterize()
            verified_offers = self._choose_list_with_more_credible_offers(combined_offers)
            display_and_log_info(self.logger, "Analysis of the offers done!")
        except ChoosingCredibleOfferNotPossibleException:
            raise VerificationImpossibleException()

        return verified_offers, statistics


    def download_offers(self) -> List[Offer]:
        offers: List[Offer] = (
            list(read_object_from_file(self.path_to_local_file))
            if self.path_to_local_file is not None
            else RequestProvider(self.search_phrase).get_offers()
        )

        if self.save_offers and self.path_to_local_file is None:
            save_object_to_file(
                get_filename(OFFERS_PATH + self.search_phrase, PICKLE_EXTENSION), offers
            )

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
            raise ChoosingCredibleOfferNotPossibleException()

        return result


    def _average_feedback_score(self, offers: List[Offer]) -> float:
        return round(np.sum([offer.seller.feedback_score for offer in offers]) / len(offers), 2)


    def _validate_init_params(self) -> None:
        # Both NOT activated
        if self.search_phrase is None and self.path_to_local_file is None:
            message: str = (f"{nameof(self.search_phrase)} must be provided or "
                            f"{nameof(self.path_to_local_file)} cannot be None")
            display_and_log_error(self.logger, message)
            raise WrongConstructorParams(message)

        # Both activated
        if self.search_phrase is not None and self.path_to_local_file is not None:
            message: str = (f"Data from local file has higher priority and downloading by passed"
                            f"{nameof(self.search_phrase)} will not be done")
            display_and_log_warning(self.logger, message)

        if self.save_offers and self.path_to_local_file is not None:
            message: str = f"Local file cannot be saved ones again"
            display_and_log_error(self.logger, message)
            raise WrongConstructorParams(message)
