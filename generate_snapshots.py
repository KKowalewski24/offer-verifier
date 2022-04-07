from argparse import ArgumentParser, Namespace
from typing import List, Tuple

from module.constants import OFFERS_PATH, PICKLE_EXTENSION
from module.model.Offer import Offer
from module.service.RequestProvider import RequestProvider
from module.service.common.Logger import Logger
from module.utils import get_filename, run_main, save_object_to_file

"""
"""

# VAR ------------------------------------------------------------------------ #
logger = Logger().get_logging_instance()


# MAIN ----------------------------------------------------------------------- #
def main() -> None:
    logger.info("Start of generate_snapshots.py")
    args = prepare_args()

    offers_id: List[Tuple[str, str]] = [
        ("293882212178", "AMD Ryzen 9 5900X 12-core 24-thread Desktop Processor - 12 cores And 24 threads")
    ]

    for offer_id, offer_name in offers_id:
        offers: List[Offer] = RequestProvider().get_offer_splitted_into_snapshots(offer_id)
        save_object_to_file(get_filename(f"{OFFERS_PATH}{offer_id}-{offer_name}", PICKLE_EXTENSION), offers)


# DEF ------------------------------------------------------------------------ #
def prepare_args() -> Namespace:
    arg_parser = ArgumentParser()

    return arg_parser.parse_args()


# __MAIN__ ------------------------------------------------------------------- #
if __name__ == "__main__":
    run_main(main)
