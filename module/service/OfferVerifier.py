import time
from typing import Callable, Dict, List, Tuple

import numpy as np
from nameof import nameof
from sklearn.metrics import confusion_matrix

from module.constants import JSON_EXTENSION, OFFERS_PATH
from module.exception.EmptyDatasetException import EmptyDatasetException
from module.exception.WrongConstructorParamsException import WrongConstructorParamsException
from module.model.Offer import Offer
from module.model.OffersWrapper import OffersWrapper
from module.model.Statistics import Statistics
from module.service.RequestProvider import RequestProvider
from module.service.common.Logger import Logger
from module.service.evaluator.Evaluator import Evaluator
from module.service.evaluator.clustering.KMeansEvaluator import KMeansEvaluator
from module.utils import display_and_log_error, display_and_log_info, display_and_log_warning, \
    get_filename, read_json_from_file, save_json_to_file


class OfferVerifier:

    def __init__(
            self, search_phrase: str = None,
            path_to_local_file: str = None,
            save_offers: bool = False,
            evaluator_params: Tuple[
                Callable[[List[Offer], Dict[str, float]], Evaluator], Dict[str, float]
            ] = (KMeansEvaluator, {})
    ) -> None:
        self.logger = Logger().get_logging_instance()
        self.search_phrase = search_phrase
        self.path_to_local_file = path_to_local_file
        self.save_offers = save_offers
        self.evaluator: Callable[[List[Offer], Dict[str, float]], Evaluator] = evaluator_params[0]
        self.params: Dict[str, float] = evaluator_params[1]
        self._validate_init_params()


    def verify(self) -> Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]]:
        display_and_log_info(self.logger, "Downloading offers, Please wait ...")
        offers: List[Offer] = self.download_offers()
        display_and_log_info(self.logger, f"Downloading offers done! Offers count: {len(offers)}")

        if len(offers) == 0:
            raise EmptyDatasetException()

        display_and_log_info(self.logger, "Performing the analysis of the offers, Please wait ...")
        verified_offers, statistics = self.evaluator(offers, self.params).evaluate()
        display_and_log_info(self.logger, "Analysis of the offers done!")

        return verified_offers


    def verify_by_local_file(
            self
    ) -> Tuple[Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]], Statistics]:
        offers_wrapper: OffersWrapper = OffersWrapper.from_dict(
            read_json_from_file(self.path_to_local_file)
        )

        if len(offers_wrapper.offers) == 0:
            raise EmptyDatasetException()

        display_and_log_info(self.logger, "Performing the analysis of the offers, Please wait ...")
        start_time = time.time()
        verified_offers, statistics = self.evaluator(offers_wrapper.offers, self.params).evaluate()
        end_time = time.time()
        display_and_log_info(self.logger, "Analysis of the offers done!")

        statistics.execution_time = end_time - start_time
        statistics.dataset_name = offers_wrapper.dataset_name
        statistics.confusion_matrix = self._calculate_confusion_matrix(offers_wrapper.offers, verified_offers)

        return verified_offers, statistics


    def download_offers(self) -> List[Offer]:
        offers = RequestProvider().get_offers(self.search_phrase)

        if self.save_offers:
            save_json_to_file(
                get_filename(OFFERS_PATH + self.search_phrase, JSON_EXTENSION),
                OffersWrapper(offers).__dict__
            )

        return offers


    def _calculate_confusion_matrix(
            self, offers: List[Offer],
            verified_offers: Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]]
    ) -> np.ndarray:
        mapped_offers: List[Tuple] = [(offer.id, offer.is_specified_as_credible) for offer in offers]
        mapped_evaluated_offers: List[Tuple] = (
                [(offer.id, verified_offers[0][1]) for offer in verified_offers[0][0]]
                + [(offer.id, verified_offers[1][1]) for offer in verified_offers[1][0]]
        )
        mapped_evaluated_offers_dict: Dict = {
            eval_offer[0]: (eval_offer[0], eval_offer[1])
            for eval_offer in mapped_evaluated_offers
        }

        y_true = [mapped_offer[1] for mapped_offer in mapped_offers]
        y_pred = [mapped_evaluated_offers_dict[x[0]][1] for x in mapped_offers]

        return confusion_matrix(y_true, y_pred, labels=[False, True])


    def _validate_init_params(self) -> None:
        # Both NOT activated
        if self.search_phrase is None and self.path_to_local_file is None:
            message: str = (f"{nameof(self.search_phrase)} must be provided or "
                            f"{nameof(self.path_to_local_file)} cannot be None")
            display_and_log_error(self.logger, message)
            raise WrongConstructorParamsException(message)

        # Both activated
        if self.search_phrase is not None and self.path_to_local_file is not None:
            message: str = (f"Data from local file has higher priority and downloading by passed"
                            f"{nameof(self.search_phrase)} will not be done")
            display_and_log_warning(self.logger, message)

        if self.save_offers and self.path_to_local_file is not None:
            message: str = f"Local file cannot be saved ones again"
            display_and_log_error(self.logger, message)
            raise WrongConstructorParamsException(message)
