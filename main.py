import subprocess
import sys
from argparse import ArgumentParser, Namespace

from dotenv import load_dotenv

from module.constants import RESULTS_DIRECTORY
from module.interface.UserInterface import UserInterface
from module.service.Logger import Logger
from module.utils import create_directory

"""
"""


# MAIN ----------------------------------------------------------------------- #
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
    logger.info("Search phrase: " + search_phrase)

    user_interface: UserInterface = UserInterface(
        search_phrase, save_offers, generate_pdf, generate_statistics
    )
    user_interface.display_result()


# DEF ------------------------------------------------------------------------ #
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

    return arg_parser.parse_args()


# UTIL ----------------------------------------------------------------------- #
def check_types_check_style() -> None:
    subprocess.call(["mypy", "."])
    subprocess.call(["flake8", "."])


def compile_to_pyc() -> None:
    subprocess.call(["python", "-m", "compileall", "."])


def check_if_exists_in_args(arg: str) -> bool:
    return arg in sys.argv


# __MAIN__ ------------------------------------------------------------------- #
if __name__ == "__main__":
    if check_if_exists_in_args("--type"):
        check_types_check_style()
    elif check_if_exists_in_args("--build"):
        compile_to_pyc()
    else:
        main()
