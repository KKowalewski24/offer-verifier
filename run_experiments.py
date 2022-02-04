import glob
from argparse import ArgumentParser, Namespace

from module.constants import PICKLE_EXTENSION
from module.service.LatexGenerator import LatexGenerator
from module.service.Logger import Logger
from module.service.OfferVerifier import OfferVerifier
from module.service.PdfGenerator import PdfGenerator
from module.service.clustering.KMeansClusterizer import KMeansClusterizer
from module.utils import run_main

EXPERIMENTS_RESULTS_DIR: str = "experiment_results"
DATASET_DIR: str = "dataset_snapshot/"

latex_generator: LatexGenerator = LatexGenerator(EXPERIMENTS_RESULTS_DIR)
pdf_generator: PdfGenerator = PdfGenerator()
logger = Logger().get_logging_instance()


def main() -> None:
    args = prepare_args()

    dataset_paths = glob.glob(DATASET_DIR + "*" + PICKLE_EXTENSION)
    for dataset_path in dataset_paths:
        offer_verifier: OfferVerifier = OfferVerifier(
            path_to_local_file=dataset_path, clusterizer=KMeansClusterizer
        )
        combined_offers, statistics = offer_verifier.verify()


# def _display_statistics(statistics: Statistics) -> None:
#     print("\n\nNumber of offers :", statistics.offers_number)
#     print("Silhouette score:", statistics.silhouette_score)
#     print("Calinski Harabasz score:", statistics.calinski_harabasz_score)
#     print("Davies Bouldin score:", statistics.davies_bouldin_score)
#     latex_table_row: str = latex_generator.get_table_body(
#         [[search_phrase] + statistics.to_list()]
#     )
#     print(latex_table_row)
#     save_to_file(STATISTICS_PATH, latex_table_row + "\n", "a")


def prepare_args() -> Namespace:
    arg_parser = ArgumentParser()

    return arg_parser.parse_args()


if __name__ == "__main__":
    run_main(main)
