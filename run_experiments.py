import glob
import os
from argparse import ArgumentParser, Namespace
from concurrent.futures.process import ProcessPoolExecutor
from typing import Any, Dict, List, Tuple

import matplotlib.pyplot as plt

from module.constants import PICKLE_EXTENSION, UTF_8
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
from module.utils import create_directory, get_filename, run_main

"""
"""

# VAR ------------------------------------------------------------------------ #
EXPERIMENTS_RESULTS_DIR: str = "experiment_results/"
DATASET_DIR: str = "dataset_snapshot/"
LATEX_IMAGE_FILENAME: str = "latex_images.txt"
ENABLE_PARALLEL: bool = False
GENERATE_PDF: bool = False
SAVE_CHARTS: bool = True

latex_generator: LatexGenerator = LatexGenerator(EXPERIMENTS_RESULTS_DIR)
pdf_generator: PdfGenerator = PdfGenerator()
logger = Logger().get_logging_instance()


# MAIN ----------------------------------------------------------------------- #
def main() -> None:
    args = prepare_args()
    create_directory(EXPERIMENTS_RESULTS_DIR)

    dataset_paths = glob.glob(DATASET_DIR + "*" + PICKLE_EXTENSION)
    evaluators_params: List[Tuple[Any, Dict[str, float]]] = [
        (KMeansEvaluator, {}),
        (FuzzyCMeansEvaluator, {}),
        (BenchmarkEvaluator, {
            BenchmarkEvaluator.CREDIBILITY_THRESHOLD_PARAM_KEY: 2.8,
            BenchmarkFeatureExtractor.POLARITY_THRESHOLD_PARAM_KEY: 0.2
        }),
        (BenchmarkEvaluator, {
            BenchmarkEvaluator.CREDIBILITY_THRESHOLD_PARAM_KEY: 3.2,
            BenchmarkFeatureExtractor.POLARITY_THRESHOLD_PARAM_KEY: 0.4
        })
    ]

    for dataset_path in dataset_paths:
        dataset_name: str = str(os.path.basename(dataset_path).split(".")[0])
        if ENABLE_PARALLEL:
            run_parallel(dataset_path, evaluators_params)
        else:
            results: List[Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool], str]] = []
            for evaluator in evaluators_params:
                offer_verifier: OfferVerifier = OfferVerifier(
                    path_to_local_file=dataset_path, evaluator_params=evaluator
                )
                combined_offers, statistics = offer_verifier.verify()

                name, params = evaluator
                _display_result(combined_offers, statistics, name.__name__)
                results.append(
                    (*combined_offers, f"{name.__name__}\n {' '.join([str(params[x]) for x in params])}")
                )
            plot_results(results, dataset_name)


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


def plot_results(
        results: List[Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool], str]], dataset_name: str
) -> None:
    for result in results:
        first = result[0]
        second = result[1]
        evaluator_name = result[2]
        plt.bar(
            [get_bar_description(first[1], evaluator_name), get_bar_description(second[1], evaluator_name)],
            [len(first[0]), len(second[0])]
        )
    plt.xticks(rotation=90)
    plt.grid(axis="y")
    plt.margins(x=0)
    plt.tight_layout()
    show_and_save(f"{dataset_name}_results", SAVE_CHARTS)


def get_bar_description(is_verified: bool, evaluator_name: str) -> str:
    verified_offer_text: str = "Oferty wiarygodne\n "
    not_verified_offer_text: str = "Oferty niewiarygodne\n "
    return (
        f"{verified_offer_text} {evaluator_name}"
        if is_verified
        else f"{not_verified_offer_text} {evaluator_name}"
    )


def set_descriptions(title: str, x_label: str = "", y_label: str = "") -> None:
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)


def show_and_save(name: str, save: bool = False) -> None:
    if save:
        filename = get_filename(name)
        plt.savefig(EXPERIMENTS_RESULTS_DIR + filename)
        plt.close()
        with open(EXPERIMENTS_RESULTS_DIR + LATEX_IMAGE_FILENAME, "a", encoding=UTF_8) as file:
            file.write(f"{latex_generator.generate_chart_image(filename, False)}\n\n")
    plt.show()


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
