from typing import Dict

from bs4 import BeautifulSoup

from module.constants import EBAY_ITEM_PATH, HTML_PARSER, SLASH_USR
from module.service.request.BaseProvider import BaseProvider
from module.utils import remove_new_line_items


class OfferDetailsProvider(BaseProvider):

    def __init__(self) -> None:
        super().__init__()


    def get_offer_details(self, offer_id: str) -> Dict[str, str]:
        soup: BeautifulSoup = self.get_beautiful_soup_instance(EBAY_ITEM_PATH + offer_id)

        return {
            "offer_id": offer_id,
            "seller_id": self._get_seller_id(soup)
        }


    def _get_seller_id(self, soup: BeautifulSoup) -> str:
        markup: str = str(remove_new_line_items(list(soup.find(id="RightSummaryPanel").children))[2])
        url: str = BeautifulSoup(markup, HTML_PARSER).find("a").get("href")
        return self.urlparse_path_replace(url, SLASH_USR)
