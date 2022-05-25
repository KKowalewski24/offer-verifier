import webbrowser
from typing import List, Tuple

from module.constants import EBAY_ITEM_PATH, JSON_EXTENSION, OFFERS_PATH, RESULTS_DIRECTORY
from module.model.OffersWrapper import OffersWrapper
from module.service.RequestProvider import RequestProvider
from module.service.common.Logger import Logger
from module.utils import create_directory, display_and_log_info, get_filename, run_main, save_json_to_file

OFFERS_NAME_IDS: List[Tuple[str, List[str]]] = [
    (
        "amd ryzen 9 5950x 16-core",
        [
            "393714612880",
            "353429471457",
            "254772007426",
            "255316126188",
            "324951940577",
            "324480526970",
            "265460231242",
            "324480324523",
            "114831636773",
            "164930511413",
            "402806621472",
            "255003155940",
            "174789972980",
            "185278620718",
            "115396323255",
        ]
    ),
]

logger = Logger().get_logging_instance()


def main() -> None:
    create_directory(RESULTS_DIRECTORY)

    for offer_name, offer_ids in OFFERS_NAME_IDS:
        display_and_log_info(logger, f"Search phrase: {offer_name}")
        offers = RequestProvider().get_offers_by_ids(offer_ids)
        display_and_log_info(logger, f"Downloaded offers: {len(offers)}")
        save_json_to_file(
            get_filename(OFFERS_PATH + offer_name, JSON_EXTENSION),
            OffersWrapper(offers).__dict__
        )


def open_offers_in_browser() -> None:
    for offer_name, offer_ids in OFFERS_NAME_IDS:
        print(f"Offer name: {offer_name}")
        for offer_id in offer_ids:
            webbrowser.open(EBAY_ITEM_PATH + offer_id)


if __name__ == "__main__":
    # open_offers_in_browser()
    run_main(main)
