import glob
from argparse import ArgumentParser, Namespace
from typing import List

from module.constants import PICKLE_EXTENSION
from module.interface.PdfGenerator import PdfGenerator
from module.model.Statistics import Statistics
from module.service.OfferVerifier import OfferVerifier
from module.service.RequestProvider import RequestProvider
from module.service.clustering.BenchmarkClusterizer import BenchmarkClusterizer
from module.service.clustering.FeatureExtractor import FeatureExtractor
from module.service.clustering.FuzzyCMeansClusterizer import FuzzyCMeansClusterizer
from module.service.clustering.KMeansClusterizer import KMeansClusterizer
from module.service.common.LatexGenerator import LatexGenerator
from module.service.common.Logger import Logger

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
    clusterizers: List = [KMeansClusterizer, FuzzyCMeansClusterizer, BenchmarkClusterizer]

    for clusterizer in clusterizers:
        result = []
        for dataset_path in dataset_paths:
            offer_verifier: OfferVerifier = OfferVerifier(
                path_to_local_file=dataset_path, clusterizer=clusterizer
            )
            combined_offers, statistics = offer_verifier.verify()

            print(f"Is verified: {combined_offers[0][1]}, offers count: {len(combined_offers[0][0])}")
            print(f"Is verified: {combined_offers[1][1]}, offers count: {len(combined_offers[1][0])}")
            print()
            result.append([len(combined_offers[0][0]), len(combined_offers[1][0])])
            pdf_generator.generate(combined_offers)
        print(result)


# DEF ------------------------------------------------------------------------ #
def _display_statistics(statistics: Statistics) -> None:
    pass


def prepare_args() -> Namespace:
    arg_parser = ArgumentParser()

    return arg_parser.parse_args()


# __MAIN__ ------------------------------------------------------------------- #
if __name__ == "__main__":
    # run_main(main)
    offer = RequestProvider().get_offer("294161433526")
    df = (
        FeatureExtractor([offer, offer])
            .insert_elementary_columns()
            .insert_extracted_features()
            .normalize_dataset()
            .get_dataset()
    )
    df.to_csv("abc.csv")
    print(df.to_numpy())
