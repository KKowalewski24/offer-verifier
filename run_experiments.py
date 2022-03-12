import glob
from argparse import ArgumentParser, Namespace

from module.constants import PICKLE_EXTENSION
from module.model.Statistics import Statistics
from module.service.common.LatexGenerator import LatexGenerator
from module.service.common.Logger import Logger
from module.service.OfferVerifier import OfferVerifier
from module.interface.PdfGenerator import PdfGenerator
from module.service.clustering.KMeansClusterizer import KMeansClusterizer
from module.utils import run_main

"""
"""

# VAR ------------------------------------------------------------------------ #
EXPERIMENTS_RESULTS_DIR: str = "experiment_results"
DATASET_DIR: str = "dataset_snapshot/"

latex_generator: LatexGenerator = LatexGenerator(EXPERIMENTS_RESULTS_DIR)
pdf_generator: PdfGenerator = PdfGenerator()
logger = Logger().get_logging_instance()


# MAIN ----------------------------------------------------------------------- #
def main() -> None:
    args = prepare_args()

    dataset_paths = glob.glob(DATASET_DIR + "*" + PICKLE_EXTENSION)
    arr = []
    for dataset_path in dataset_paths:
        offer_verifier: OfferVerifier = OfferVerifier(
            path_to_local_file=dataset_path, clusterizer=KMeansClusterizer
        )
        combined_offers, statistics = offer_verifier.verify()
        print(f"Is verified: {combined_offers[0][1]}, offers count: {len(combined_offers[0][0])}")
        print(f"Is verified: {combined_offers[1][1]}, offers count: {len(combined_offers[1][0])}")
        print()
        arr.append([len(combined_offers[0][0]), len(combined_offers[1][0])])
        pdf_generator.generate(combined_offers)
    print(arr)


# DEF ------------------------------------------------------------------------ #
def _display_statistics(statistics: Statistics) -> None:
    pass


def prepare_args() -> Namespace:
    arg_parser = ArgumentParser()

    return arg_parser.parse_args()


# __MAIN__ ------------------------------------------------------------------- #
if __name__ == "__main__":
    run_main(main)
