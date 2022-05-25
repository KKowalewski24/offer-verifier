from typing import List, Tuple

from module.constants import JSON_EXTENSION, OFFERS_PATH
from module.model.OffersWrapper import OffersWrapper
from module.service.RequestProvider import RequestProvider
from module.service.common.Logger import Logger
from module.utils import display_and_log_info, get_filename, run_main, save_json_to_file

OFFERS_NAME_IDS: List[Tuple[str, List[str]]] = [
    ("", [""])
]

logger = Logger().get_logging_instance()


def main() -> None:
    for offer_name, offer_ids in OFFERS_NAME_IDS:
        display_and_log_info(logger, f"Search phrase: {offer_name}")
        offers = RequestProvider().get_offers_by_ids(offer_ids)
        display_and_log_info(logger, f"Downloaded offers: {len(offers)}")
        save_json_to_file(
            get_filename(OFFERS_PATH + offer_name, JSON_EXTENSION),
            OffersWrapper(offers).__dict__
        )


if __name__ == "__main__":
    run_main(main)
