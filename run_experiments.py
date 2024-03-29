import glob
from argparse import ArgumentParser, Namespace
from typing import Any, Dict, List, Tuple

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay

from module.constants import DATASET_SOURCE_DIRECTORY, JSON_EXTENSION
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
DATASET_DIR: str = DATASET_SOURCE_DIRECTORY
EXPERIMENTS_RESULTS_DIR: str = "_experiment_results/"
LATEX_IMAGE_FILENAME: str = "latex_images.txt"
NEW_LINE: str = "\n"
SAVE_CHARTS: bool = True

latex_generator: LatexGenerator = LatexGenerator(EXPERIMENTS_RESULTS_DIR)
logger = Logger().get_logging_instance()

evaluators_params: List[Tuple[Any, Dict[str, float]]] = [
    (KMeansEvaluator, {}),
    (FuzzyCMeansEvaluator, {}),
    (BenchmarkEvaluator, {
        BenchmarkEvaluator.CREDIBILITY_THRESHOLD_PARAM_KEY: 3.4,
        BenchmarkFeatureExtractor.POLARITY_THRESHOLD_PARAM_KEY: 0.6
    }),
    (BenchmarkEvaluator, {
        BenchmarkEvaluator.CREDIBILITY_THRESHOLD_PARAM_KEY: 4.2,
        BenchmarkFeatureExtractor.POLARITY_THRESHOLD_PARAM_KEY: 0.2
    })
]


# MAIN ----------------------------------------------------------------------- #
def main() -> None:
    args = prepare_args()
    create_directory(EXPERIMENTS_RESULTS_DIR)
    dataset_paths = glob.glob(DATASET_DIR + "*" + JSON_EXTENSION)

    for dataset_path in dataset_paths:
        offers_results: List[Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool], str]] = []
        execution_time_results: List[Tuple[float, str]] = []

        for evaluator_params in evaluators_params:
            offer_verifier: OfferVerifier = OfferVerifier(
                path_to_local_file=dataset_path, evaluator_params=evaluator_params
            )
            combined_offers, statistics = offer_verifier.verify_by_local_file()

            evaluator_name, params = evaluator_params
            formatted_params = (
                f"{evaluator_name.__name__}\n {' '.join([f'{x}={params[x]}{NEW_LINE}' for x in params])}"
            )
            offers_results.append((*combined_offers, formatted_params))
            execution_time_results.append((statistics.execution_time, formatted_params))

            # display_combined_offers(combined_offers)
            display_result(combined_offers, statistics, evaluator_name.__name__)
            generate_table(combined_offers, statistics, evaluator_name.__name__)
            plot_confusion_matrix(statistics, formatted_params, evaluator_name)

        plot_offers_results(offers_results, statistics.dataset_name)
        plot_execution_time(execution_time_results, statistics.dataset_name)


# DEF ------------------------------------------------------------------------ #
def display_result(
        combined_offers: Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]],
        statistics: Statistics, evaluator_name: str
) -> None:
    message: str = "\n--------------------------------------------------\n"
    message += f"{statistics.dataset_name}\n"
    message += f"{evaluator_name}\n"
    message += f"Liczba wszystkich ofert: {statistics.offers_count}\n"
    message += f"Czas wykonania: {round(statistics.execution_time, 3)} sek\n"
    for combined_offer in combined_offers:
        message += (
            f"Liczba ofert określona jako "
            f"{'wiarygodne' if combined_offer[1] else 'niewiarogodne'}: "
            f"{len(combined_offer[0])}\n"
        )
    message += "--------------------------------------------------\n"
    print(message)


def generate_table(
        combined_offers: Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]],
        statistics: Statistics, evaluator_name: str
) -> None:
    if combined_offers[0][1] == True:
        credible_offers = combined_offers[0][0]
        not_credible_offers = combined_offers[1][0]
    else:
        not_credible_offers = combined_offers[0][0]
        credible_offers = combined_offers[1][0]

    info: pd.DataFrame = pd.DataFrame(
        columns=["Nazwa", "Wartość"],
        data=[
            ["Nazwa zbioru", statistics.dataset_name],
            ["Nazwa algorytmu", evaluator_name],
            ["Liczba wszystkich ofert", statistics.offers_count],
            ["Czas wykonania (s)", f"{round(statistics.execution_time, 3)}"],
            ["Liczba ofert określona jako wiarygodne", str(len(credible_offers))],
            ["Liczba ofert określona jako niewiarogodne", str(len(not_credible_offers))],
        ]
    )
    latex_generator.generate_vertical_table_df(info, statistics.dataset_name)


def plot_confusion_matrix(statistics: Statistics, formatted_params: str, evaluator_name: str) -> None:
    cmd = ConfusionMatrixDisplay(confusion_matrix=statistics.confusion_matrix, display_labels=[True, False])
    cmd.plot(colorbar=False, cmap="binary")
    set_descriptions(f"Macierz pomyłek{NEW_LINE} {formatted_params.replace(NEW_LINE, ' ')}")
    show_and_save(f"{statistics.dataset_name}_{evaluator_name.__name__}", SAVE_CHARTS)


def plot_offers_results(
        offer_results: List[Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool], str]],
        dataset_name: str
) -> None:
    plt.figure(figsize=(7, 5))
    index: int = 0
    for result in offer_results:
        first = result[0]
        second = result[1]
        evaluator_name = result[2]

        plt.bar(get_bar_description(first[1], evaluator_name), len(first[0]), width=0.3)
        plt.text(index, len(first[0]), len(first[0]), color="blue", fontweight="bold", ha="center")
        plt.bar(get_bar_description(second[1], evaluator_name), len(second[0]), width=0.3)
        plt.text(index + 1, len(second[0]), len(second[0]), color="blue", fontweight="bold", ha="center")
        index += 2

    plt.xticks(rotation=90)
    plt.grid(axis="y")
    plt.margins(x=0)
    plt.tight_layout(pad=3)
    set_descriptions("", "Algorytm oceniający wiarygodność (Evaluator)", "Liczba ofert")
    show_and_save(f"{dataset_name}_offer_results", SAVE_CHARTS)


def plot_execution_time(execution_time_results: List[Tuple[float, str]], dataset_name: str) -> None:
    # plt.figure(figsize=(6, 5))
    for index, result in enumerate(execution_time_results):
        execution_time = round(result[0], 3)
        evaluator_name = result[1]
        plt.bar(evaluator_name, execution_time, width=0.1)
        plt.text(index, execution_time, f"{execution_time}s", color="blue", fontweight="bold", ha="center")

    plt.xticks(rotation=90)
    plt.grid(axis="y")
    plt.margins(x=0)
    plt.tight_layout(pad=3)
    set_descriptions(
        "Czas w sekundach (s)", "Algorytm oceniający wiarygodność (Evaluator)", "Czasy wykonania algorytmów"
    )
    show_and_save(f"{dataset_name}_time_results", SAVE_CHARTS)


def get_bar_description(is_credible: bool, evaluator_name: str) -> str:
    credible_offer_text: str = "Oferty wiarygodne\n "
    not_credible_offer_text: str = "Oferty niewiarygodne\n "
    return (
        f"{credible_offer_text} {evaluator_name}"
        if is_credible
        else f"{not_credible_offer_text} {evaluator_name}"
    )


def display_combined_offers(
        combined_offers: Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]]
) -> None:
    for i in range(len(combined_offers)):
        print(combined_offers[i][1])
        for combined_offer in combined_offers[i][0]:
            print(combined_offer.id, end=", ")
        print("--------------------------------------")


def set_descriptions(title: str, x_label: str = "", y_label: str = "") -> None:
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)


def show_and_save(name: str, save: bool = False) -> None:
    if save:
        filename = get_filename(name)
        plt.savefig(EXPERIMENTS_RESULTS_DIR + filename)
        plt.close()
    plt.show()


def prepare_args() -> Namespace:
    arg_parser = ArgumentParser()

    return arg_parser.parse_args()


# __MAIN__ ------------------------------------------------------------------- #
if __name__ == "__main__":
    run_main(main)
