from argparse import ArgumentParser, Namespace

from module.model.Offer import Offer
from module.service.RequestProvider import RequestProvider
from module.utils import run_main

"""
"""


# VAR ------------------------------------------------------------------------ #

# MAIN ----------------------------------------------------------------------- #
def main() -> None:
    args = prepare_args()
    offer_id: str = ""
    offer: Offer = RequestProvider().get_offer(offer_id)


# DEF ------------------------------------------------------------------------ #
def prepare_args() -> Namespace:
    arg_parser = ArgumentParser()

    return arg_parser.parse_args()


# __MAIN__ ------------------------------------------------------------------- #
if __name__ == "__main__":
    run_main(main)
