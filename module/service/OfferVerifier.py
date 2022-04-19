import time
from typing import Callable, Dict, List, Tuple

from nameof import nameof

from module.constants import OFFERS_PATH, PICKLE_EXTENSION
from module.exception.EmptyDatasetException import EmptyDatasetException
from module.exception.WrongConstructorParamsException import WrongConstructorParamsException
from module.model.Offer import Offer
from module.model.Statistics import Statistics
from module.service.RequestProvider import RequestProvider
from module.service.common.Logger import Logger
from module.service.evaluator.Evaluator import Evaluator
from module.service.evaluator.clustering.KMeansEvaluator import KMeansEvaluator
from module.utils import display_and_log_error, display_and_log_info, display_and_log_warning, \
    get_filename, read_object_from_file, save_object_to_file


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


    def verify(self) -> Tuple[Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]], Statistics]:
        display_and_log_info(self.logger, "Downloading offers, Please wait ...")
        offers: List[Offer] = self.download_offers()
        display_and_log_info(self.logger, f"Downloading offers done! Offers count: {len(offers)}")

        if len(offers) == 0:
            raise EmptyDatasetException()

        display_and_log_info(self.logger, "Performing the analysis of the offers, Please wait ...")
        start_time = time.time()
        verified_offers, statistics = self.evaluator(offers, self.params).evaluate()
        end_time = time.time()
        statistics.execution_time = end_time - start_time
        display_and_log_info(self.logger, "Analysis of the offers done!")

        return verified_offers, statistics


    def download_offers(self) -> List[Offer]:
        offers: List[Offer] = (
            list(read_object_from_file(self.path_to_local_file))
            if self.path_to_local_file is not None
            else RequestProvider().get_offers(self.search_phrase)
        )

        if self.save_offers and self.path_to_local_file is None:
            save_object_to_file(get_filename(OFFERS_PATH + self.search_phrase, PICKLE_EXTENSION), offers)

        return offers


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
