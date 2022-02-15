from typing import List

from module.service.OfferVerifier import OfferVerifier
from module.utils import run_main

SEARCH_PHRASES: List[str] = [
    "amd ryzen 9"
    "intel core i9"
    "kingston a400"
    "iphone 7 plus 128gb"
    "new balance 574 blue"
    "atomic redster"
    "tag heuer formula 1 chronograph"
    "tag heuer carrera chronograph"
    "tag heuer carrera automatic"
    "breitling chronograph automatic"
    "maono microphone"
    "lexar sd card"
    "kingston pendrive"
    "lexia"
    "apple macbook pro m1"
    "lord of the lost"
    "metallica s&m2"
    "rammstein shirt"
    "porsche 911 key fob"
    "porsche 911 rug"
]


def main() -> None:
    for search_phrase in SEARCH_PHRASES:
        print(f"Search phrase: {search_phrase}")
        offers = OfferVerifier(search_phrase=search_phrase, save_offers=True).download_offers()
        print(f"Downloaded offers: {len(offers)}")


if __name__ == "__main__":
    run_main(main)
