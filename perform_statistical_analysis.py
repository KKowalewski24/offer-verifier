import glob
from argparse import ArgumentParser, Namespace

from module.constants import PICKLE_EXTENSION
from module.service.common.Logger import Logger
from module.utils import run_main

"""
"""

# VAR ------------------------------------------------------------------------ #
ANALYSIS_RESULTS_DIR: str = "analysis_results"
DATASET_DIR: str = "dataset_snapshot/"

logger = Logger().get_logging_instance()


# MAIN ----------------------------------------------------------------------- #
def main() -> None:
    args = prepare_args()
    dataset_paths = glob.glob(DATASET_DIR + "*" + PICKLE_EXTENSION)
    # TODO


# DEF ------------------------------------------------------------------------ #

def prepare_args() -> Namespace:
    arg_parser = ArgumentParser()

    return arg_parser.parse_args()


# __MAIN__ ------------------------------------------------------------------- #
if __name__ == "__main__":
    run_main(main)
