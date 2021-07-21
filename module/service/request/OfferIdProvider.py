from typing import List

from bs4 import BeautifulSoup
from requests.utils import urlparse

from module.constants import EBAY_SEARCH_PATH, ITEMS_PER_PAGE, ITM, OFFERS_ID_A_HREF_ATTRIBUTES, \
    PARAM_BRAND_NEW, PARAM_BUY_NOW, PARAM_PAGE_NUMBER
from module.service.request.BaseProvider import BaseProvider
from module.utils import remove_duplicates


class OfferIdProvider(BaseProvider):

    def __init__(self, search_phrase: str) -> None:
        super().__init__()
        self.search_phrase = search_phrase


    def get_offers_id(self) -> List[str]:
        offers_id: List[str] = []
        for page_number in range(self._get_pages_number()):
            offers_id.extend(self._get_offers_id_for_single_page(page_number))

        return remove_duplicates(offers_id)


    def _get_offers_id_for_single_page(self, page_number: int) -> List[str]:
        soup: BeautifulSoup = self._get_beautiful_soup_instance(page_number)
        return [
            urlparse(a_href.get("href")).path.replace("/" + ITM, "")
            for a_href in soup.find_all("a", attrs=OFFERS_ID_A_HREF_ATTRIBUTES)
        ]


    def _get_pages_number(self) -> int:
        soup: BeautifulSoup = self._get_beautiful_soup_instance(1)
        items_number: int = int(
            soup.find(text=" results for ").find_parent()
                .select("span")[0].get_text().replace(",", "")
        )

        pages_number: int = int(items_number / ITEMS_PER_PAGE[1])
        if items_number % ITEMS_PER_PAGE[1] != 0:
            pages_number += 1

        return pages_number


    def _get_beautiful_soup_instance(self, page_number: int) -> BeautifulSoup:
        response = self.requests_session.get(self._create_url(page_number))
        return BeautifulSoup(response.content, "html.parser")


    def _create_url(self, page_number: int) -> str:
        return EBAY_SEARCH_PATH + self.search_phrase + PARAM_BRAND_NEW + \
               PARAM_BUY_NOW + ITEMS_PER_PAGE[0] + PARAM_PAGE_NUMBER + str(page_number)
