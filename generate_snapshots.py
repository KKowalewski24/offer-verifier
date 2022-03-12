from argparse import ArgumentParser, Namespace
from typing import List

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

    offers_id: List[str] = [
        "294161433526"
    ]

    for offer_id in offers_id:
        offers: List[Offer] = RequestProvider().get_offer_splitted_into_snapshots(offer_id)
        save_object_to_file(get_filename(OFFERS_PATH + offer_id, PICKLE_EXTENSION), offers)
        offer: Offer = RequestProvider().get_offer(offer_id)
        print(offer)


# DEF ------------------------------------------------------------------------ #
def prepare_args() -> Namespace:
    arg_parser = ArgumentParser()

    return arg_parser.parse_args()


# __MAIN__ ------------------------------------------------------------------- #
if __name__ == "__main__":
    run_main(main)
