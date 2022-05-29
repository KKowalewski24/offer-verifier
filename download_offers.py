import webbrowser
from typing import List, Tuple

from module.constants import EBAY_ITEM_PATH, JSON_EXTENSION, OFFERS_PATH, RESULTS_DIRECTORY
from module.model.OffersWrapper import OffersWrapper
from module.service.RequestProvider import RequestProvider
from module.service.common.Logger import Logger
from module.utils import create_directory, display_and_log_info, get_filename, run_main, save_json_to_file

OFFERS_NAME_IDS: List[Tuple[str, List[str]]] = [
    (
        "Logitech m330 silent plus wireless mouse",
        [
            "274397880702",
            "265057665735",
            "173866245760",
            "403260420231",
            "334450553087",
            "115359467945",
            "183914161172",
            "294954877695",
            "154748368545",
            "165486728404",
            "224521087043",
        ]
    ),
    (
        "Dell kb522",
        [
            "144424823851",
            "165324771635",
            "284765479736",
            "265036799585",
            "233473029652",
            "254391662544",
            "124264256696",
            "184679202498",
            "165288195030",
            "324689481396",
            "124866339735",
            "224140935197",
            "334374878752",
            "125285449664",
            "144128841494",
            "175282353903",
        ]
    ),
    (
        "Apple iPhone 11 128gb",
        [
            "265687803334",
            "304483134601",
            "384801268671",
            "294795784502",
            "304345175606",
            "304345175160",
            "125133076503",
            "403685713202",
            "274417996351",
            "403662737672",
            "403662737683",
            "154317230752",
            "354063668529",
            "284829561755",
            "275307057518",
            "234556890151",
            "224863529832",
            "363853411310",
            "403368693738",
            "374002605441",
            "203926615228",
            "383721905997",
        ]
    ),
    (
        "Logitech m185",
        [
            "303584559225",
            "313801832344",
            "154853011630",
            "331333475528",
            "184217751270",
            "384320429914",
            "284380193729",
            "154582775348",
            "185158786398",
            "334400568840",
            "384854818229",
            "274068832613",
            "192306639958",
            "192306637682",
            "192306637717",
            "184679208204",
            "184679186521",
        ],
    )
]

logger = Logger().get_logging_instance()


def main() -> None:
    create_directory(RESULTS_DIRECTORY)

    for offer_name, offer_ids in OFFERS_NAME_IDS:
        display_and_log_info(logger, f"Search phrase: {offer_name}")
        offers = RequestProvider().get_offers_by_ids(offer_ids)
        display_and_log_info(logger, f"Downloaded offers: {len(offers)}")
        save_json_to_file(
            get_filename(OFFERS_PATH + offer_name, JSON_EXTENSION),
            OffersWrapper(offers).__dict__
        )


def open_offers_in_browser() -> None:
    for offer_name, offer_ids in OFFERS_NAME_IDS:
        print(f"Offer name: {offer_name}")
        for offer_id in offer_ids:
            webbrowser.open(EBAY_ITEM_PATH + offer_id)


if __name__ == "__main__":
    # print(OfferIdProvider("")._create_url(1))
    # open_offers_in_browser()
    run_main(main)
