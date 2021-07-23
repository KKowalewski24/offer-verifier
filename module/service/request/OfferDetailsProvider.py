from typing import Any, Dict

from bs4 import BeautifulSoup

from module.constants import EBAY_ITEM_PATH, HTML_PARSER, LEFT_PANEL_ATTRIBUTE, \
    OFFERS_IMAGE_ATTRIBUTES, OFFERS_PRICE_ATTRIBUTES, RIGHT_PANEL_ATTRIBUTE, SLASH_USR
from module.service.request.BaseProvider import BaseProvider
from module.utils import remove_new_line_items


class OfferDetailsProvider(BaseProvider):

    def __init__(self) -> None:
        super().__init__()


    def get_offer_details(self, offer_id: str) -> Dict[str, Any]:
        soup: BeautifulSoup = self.get_beautiful_soup_instance(EBAY_ITEM_PATH + offer_id)

        return {
            "offer_id": offer_id,
            "offer_title": self._get_title(soup),
            "offer_price": self._get_price(soup),
            "offer_image_url": self._get_image_url(soup),
            "seller": {
                "seller_id": self._get_seller_id(soup)
            }
        }


    def _get_title(self, soup: BeautifulSoup) -> str:
        return str(list(soup.find(id=LEFT_PANEL_ATTRIBUTE).find("h1").children)[1])


    def _get_price(self, soup: BeautifulSoup) -> str:
        return str(soup.find(attrs=OFFERS_PRICE_ATTRIBUTES).get("content"))


    def _get_image_url(self, soup: BeautifulSoup) -> str:
        return str(soup.find(attrs=OFFERS_IMAGE_ATTRIBUTES).get("src"))


    def _get_seller_id(self, soup: BeautifulSoup) -> str:
        markup: str = str(
            remove_new_line_items(list(soup.find(id=RIGHT_PANEL_ATTRIBUTE).children))[2]
        )
        url: str = BeautifulSoup(markup, HTML_PARSER).find("a").get("href")
        return self.urlparse_path_replace(url, SLASH_USR)
