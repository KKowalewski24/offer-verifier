from typing import Any, Dict

from bs4 import BeautifulSoup

from module.constants import EBAY_ITEM_PATH, HTML_PARSER, OFFER_DESCRIPTION_ATTRIBUTES, \
    OFFER_IMAGE_ATTRIBUTES, OFFER_PRICE_ATTRIBUTES, RETURNS_KEYWORD, RETURNS_NOT_ACCEPTED, \
    RETURNS_OPTION_ATTRIBUTES, RETURNS_OPTION_SPAN_ATTRIBUTES, RETURNS_OPTION_WHY_BUY_ATTRIBUTES, \
    SELLER_PANEL_ATTRIBUTES, SLASH_USR, TITLE_PANEL_ATTRIBUTES
from module.service.request.BaseProvider import BaseProvider
from module.utils import normalize_text, remove_new_line_items


class OfferDetailsProvider(BaseProvider):

    def __init__(self) -> None:
        super().__init__()


    def get_offer_details(self, offer_id: str) -> Dict[str, Any]:
        soup: BeautifulSoup = self.get_beautiful_soup_instance(EBAY_ITEM_PATH + offer_id)

        return {
            "id": offer_id,
            "title": self._get_title(soup),
            "price": self._get_price(soup),
            "image_url": self._get_image_url(soup),
            "has_return_option": self._get_return_option(soup),
            "description_length": self._get_description_length(soup),
            "seller": {
                "id": self._get_seller_id(soup)
            }
        }


    def _get_title(self, soup: BeautifulSoup) -> str:
        return str(list(soup.find(attrs=TITLE_PANEL_ATTRIBUTES).find("h1").children)[1])


    def _get_price(self, soup: BeautifulSoup) -> str:
        return str(soup.find(attrs=OFFER_PRICE_ATTRIBUTES).get("content"))


    def _get_image_url(self, soup: BeautifulSoup) -> str:
        return str(soup.find(attrs=OFFER_IMAGE_ATTRIBUTES).get("src"))


    def _get_return_option(self, soup: BeautifulSoup) -> bool:
        returns_phrase: str = (
            soup.find(attrs=RETURNS_OPTION_ATTRIBUTES)
                .find_parent()
                .find(attrs=RETURNS_OPTION_SPAN_ATTRIBUTES)
                .get_text(strip=True)
        )
        other_returns_phrase: str = str(soup.find(attrs=RETURNS_OPTION_WHY_BUY_ATTRIBUTES).get_text())

        return returns_phrase != RETURNS_NOT_ACCEPTED or RETURNS_KEYWORD in other_returns_phrase


    def _get_description_length(self, soup: BeautifulSoup) -> int:
        description_url: str = soup.find(attrs=OFFER_DESCRIPTION_ATTRIBUTES).get("src")
        description_soap: BeautifulSoup = self.get_beautiful_soup_instance(description_url)

        if description_soap is not None and len(description_soap) != 0:
            return len(normalize_text(description_soap.get_text()))

        return 0


    def _get_seller_id(self, soup: BeautifulSoup) -> str:
        markup: str = str(
            remove_new_line_items(list(soup.find(attrs=SELLER_PANEL_ATTRIBUTES).children))[2]
        )
        url: str = BeautifulSoup(markup, HTML_PARSER).find("a").get("href")
        return self.urlparse_path_replace(url, SLASH_USR)
