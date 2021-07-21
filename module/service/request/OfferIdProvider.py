from typing import List

from bs4 import BeautifulSoup

from module.constants import EBAY_SEARCH_PATH, ITEMS_PER_PAGE, PARAM_BRAND_NEW, PARAM_BUY_NOW, \
    PARAM_PAGE_NUMBER
from module.service.request.BaseProvider import BaseProvider


class OfferIdProvider(BaseProvider):

    def __init__(self, search_phrase: str) -> None:
        super().__init__()
        self.search_phrase = search_phrase


    def get_offers_id(self) -> List[str]:
        return []


    def _get_pages_number(self) -> str:
        soup: BeautifulSoup = self._get_beautiful_soup_instance("1")
        items_number: int = int(soup.find(text=" results for ").parent
                                .select("span")[0].get_text().replace(",", ""))
        pages_number: int = int(items_number / ITEMS_PER_PAGE[1])
        if items_number % ITEMS_PER_PAGE[1] != 0:
            pages_number += 1

        return str(pages_number)


    def _get_beautiful_soup_instance(self, page_number: str) -> BeautifulSoup:
        response = self.requests_session.get(self._create_url(page_number))
        return BeautifulSoup(response.content, "html.parser")


    def _create_url(self, page_number: str) -> str:
        return EBAY_SEARCH_PATH + self.search_phrase + PARAM_BRAND_NEW + \
               PARAM_BUY_NOW + ITEMS_PER_PAGE[0] + PARAM_PAGE_NUMBER + page_number
