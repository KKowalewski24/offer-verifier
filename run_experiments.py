import glob
from argparse import ArgumentParser, Namespace
from concurrent.futures.process import ProcessPoolExecutor
from typing import Any, Dict, List, Tuple

from module.constants import PICKLE_EXTENSION
from module.interface.PdfGenerator import PdfGenerator
from module.model.Offer import Offer
from module.model.Statistics import Statistics
from module.service.OfferVerifier import OfferVerifier
from module.service.common.LatexGenerator import LatexGenerator
from module.service.common.Logger import Logger
from module.service.evaluator.benchmark.BenchmarkEvaluator import BenchmarkEvaluator
from module.service.evaluator.benchmark.BenchmarkFeatureExtractor import BenchmarkFeatureExtractor
from module.service.evaluator.clustering.FuzzyCMeansEvaluator import FuzzyCMeansEvaluator
from module.service.evaluator.clustering.KMeansEvaluator import KMeansEvaluator
from module.utils import run_main

"""
"""

# VAR ------------------------------------------------------------------------ #
ENABLE_PARALLEL: bool = False
GENERATE_PDF: bool = False
EXPERIMENTS_RESULTS_DIR: str = "experiment_results"
DATASET_DIR: str = "dataset_snapshot/"

latex_generator: LatexGenerator = LatexGenerator(EXPERIMENTS_RESULTS_DIR)
pdf_generator: PdfGenerator = PdfGenerator()
logger = Logger().get_logging_instance()


# MAIN ----------------------------------------------------------------------- #
def main() -> None:
    args = prepare_args()

    dataset_paths = glob.glob(DATASET_DIR + "*" + PICKLE_EXTENSION)
    evaluators_params: List[Tuple[Any, Dict[str, float]]] = [
        (KMeansEvaluator, {}),
        (FuzzyCMeansEvaluator, {}),
        (BenchmarkEvaluator, {
            BenchmarkEvaluator.CREDIBILITY_THRESHOLD_PARAM_KEY: 2.8,
            BenchmarkFeatureExtractor.POLARITY_THRESHOLD_PARAM_KEY: 0.2
        })
    ]
    for dataset_path in dataset_paths:
        if ENABLE_PARALLEL:
            run_parallel(dataset_path, evaluators_params)
        else:
            result = []
            for evaluator in evaluators_params:
                offer_verifier: OfferVerifier = OfferVerifier(
                    path_to_local_file=dataset_path, evaluator_params=evaluator
                )
                combined_offers, statistics = offer_verifier.verify()

                _display_result(combined_offers, statistics, evaluator[0].__name__)
                result.append([len(combined_offers[0][0]), len(combined_offers[1][0])])
            print(result)


# DEF ------------------------------------------------------------------------ #
def _display_result(
        combined_offers: Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]],
        statistics: Statistics, evaluator_name: str
) -> None:
    message: str = "\n--------------------------------------------------\n"
    message += f"{evaluator_name}\n"
    message += f"Liczba wszystkich ofert {statistics.offers_count}\n"
    message += f"Czas wykonania {round(statistics.execution_time, 3)} sek\n"
    for combined_offer in combined_offers:
        message += (
            f"Liczba ofert określona jako "
            f"{'wiarygodne' if combined_offer[1] else 'niewiarogodne'}: "
            f"{len(combined_offer[0])}\n"
        )
    message += "--------------------------------------------------\n"
    print(message)

    if GENERATE_PDF:
        pdf_generator.generate(combined_offers)


def run_single_thread(evaluator: Tuple[Any, Dict[str, float]], dataset_path: str) -> Any:
    offer_verifier: OfferVerifier = OfferVerifier(
        path_to_local_file=dataset_path, evaluator_params=evaluator
    )

    combined_offers, statistics = offer_verifier.verify()
    _display_result(combined_offers, statistics, evaluator[0].__name__)


def run_parallel(dataset_path: str, evaluators_params: List[Tuple[Any, Dict[str, float]]]) -> None:
    evaluators_len = len(evaluators_params)
    with ProcessPoolExecutor() as executor:
        executor.map(
            run_single_thread,
            evaluators_params,
            [dataset_path] * evaluators_len
        )


def prepare_args() -> Namespace:
    arg_parser = ArgumentParser()

    return arg_parser.parse_args()


# __MAIN__ ------------------------------------------------------------------- #
if __name__ == "__main__":
    run_main(main)
