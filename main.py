from argparse import ArgumentParser, Namespace

from dotenv import load_dotenv

from module.constants import RESULTS_DIRECTORY
from module.interface.UserInterface import UserInterface
from module.service.Logger import Logger
from module.utils import create_directory, run_main

"""
"""


def main() -> None:
    logger = Logger().get_logging_instance()
    logger.info("Start program")
    load_dotenv()
    create_directory(RESULTS_DIRECTORY)

    args = prepare_args()
    search_phrase: str = args.phrase
    generate_pdf: bool = args.pdf
    logger.info("Search phrase: " + search_phrase)

    user_interface: UserInterface = UserInterface(search_phrase, generate_pdf)
    user_interface.display_result()


def prepare_args() -> Namespace:
    arg_parser = ArgumentParser()

    arg_parser.add_argument(
        "-p", "--phrase", required=True, type=str, help="Search phrase"
    )
    arg_parser.add_argument(
        "--pdf", default=False, action="store_true", help="Generate PDF report"
    )

    return arg_parser.parse_args()


if __name__ == "__main__":
    run_main(main)
