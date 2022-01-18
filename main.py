from argparse import ArgumentParser, Namespace

from dotenv import load_dotenv

from module.constants import RESULTS_DIRECTORY
from module.interface.UserInterface import UserInterface
from module.service.Logger import Logger
from module.service.OfferVerifier import OfferVerifier
from module.utils import create_directory, display_and_log_info, run_main

"""
"""


def main() -> None:
    logger = Logger().get_logging_instance()
    logger.info("Start program")
    load_dotenv()
    create_directory(RESULTS_DIRECTORY)

    args = prepare_args()
    search_phrase: str = args.phrase
    save_offers: bool = args.offers
    generate_pdf: bool = args.pdf
    generate_statistics: bool = args.statistics
    only_dataset: bool = args.dataset
    logger.info("Search phrase: " + search_phrase)

    if not only_dataset:
        user_interface: UserInterface = UserInterface(
            search_phrase, save_offers, generate_pdf, generate_statistics
        )
        user_interface.display_result()
    else:
        offer_verifier: OfferVerifier = OfferVerifier(search_phrase, save_offers)
        display_and_log_info(logger, str(len(offer_verifier.download_offers())))


def prepare_args() -> Namespace:
    arg_parser = ArgumentParser()

    arg_parser.add_argument(
        "-p", "--phrase", required=True, type=str, help="Search phrase"
    )
    arg_parser.add_argument(
        "-so", "--offers", default=False, action="store_true", help="Save downloaded offers to file"
    )
    arg_parser.add_argument(
        "--pdf", default=False, action="store_true", help="Generate PDF report"
    )
    arg_parser.add_argument(
        "-s", "--statistics", default=False, action="store_true",
        help="Generate clustering statistics"
    )
    arg_parser.add_argument(
        "-ds", "--dataset", default=False, action="store_true",
        help="Only create and save dataset - for development and research!!!"
    )

    return arg_parser.parse_args()


if __name__ == "__main__":
    run_main(main)
