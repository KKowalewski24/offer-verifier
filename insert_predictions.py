import glob
from argparse import ArgumentParser, Namespace

from module.constants import DATASET_SOURCE_DIRECTORY, JSON_EXTENSION
from module.model.OffersWrapper import OffersWrapper
from module.service.OfferVerifier import OfferVerifier
from module.service.evaluator.clustering.KMeansEvaluator import KMeansEvaluator
from module.utils import read_json_from_file, run_main, save_json_to_file

"""
"""

# VAR ------------------------------------------------------------------------ #
DATASET_DIR: str = DATASET_SOURCE_DIRECTORY


# MAIN ----------------------------------------------------------------------- #
def main() -> None:
    args = prepare_args()
    dataset_paths = glob.glob(DATASET_DIR + "*" + JSON_EXTENSION)

    for dataset_path in dataset_paths:
        offer_verifier: OfferVerifier = OfferVerifier(
            path_to_local_file=dataset_path, evaluator_params=(KMeansEvaluator, {})
        )

        combined_offers, _ = offer_verifier.verify_by_local_file()
        offers_wrapper: OffersWrapper = OffersWrapper.from_dict(read_json_from_file(dataset_path))

        for i in range(len(combined_offers)):
            for offer in combined_offers[0][0]:
                offer_from_file = [x for x in offers_wrapper.offers if x.id == offer.id][0]
                offer_from_file.is_specified_as_credible = offer.is_specified_as_credible

        save_json_to_file(
            f"{dataset_path.replace(JSON_EXTENSION, '')}-evaluated{JSON_EXTENSION}", offers_wrapper.__dict__
        )


# DEF ------------------------------------------------------------------------ #
def prepare_args() -> Namespace:
    arg_parser = ArgumentParser()

    return arg_parser.parse_args()


# __MAIN__ ------------------------------------------------------------------- #
if __name__ == "__main__":
    run_main(main)
