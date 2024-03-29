from typing import List

from bs4 import Tag

from module.constants import EBAY_SEARCH_PATH, ITEMS_NUMBER_PHRASE, ITEMS_PER_PAGE, LIST_VIEW, \
    OFFERS_ID_A_HREF_ATTRIBUTES, OFFERS_ID_RELATED_OFFERS_SEPARATOR_ATTRIBUTES, PARAM_BRAND_NEW, \
    PARAM_BUY_NOW, PARAM_PAGE_NUMBER, SCH_PAGE, SLASH_ITM
from module.exception.ArraysLengthNotEqualException import ArraysLengthNotEqualException
from module.service.request.BaseProvider import BaseProvider
from module.utils import remove_duplicates, remove_none_items


class OfferIdProvider(BaseProvider):

    def __init__(self, search_phrase: str) -> None:
        super().__init__()
        self.search_phrase = search_phrase


    def get_offers_id(self) -> List[str]:
        offers_id: List[str] = []
        for page_number in self._get_pages_range():
            offers_id.extend(self._get_offers_id_for_single_page(page_number))

        return remove_duplicates(offers_id)


    def _get_offers_id_for_single_page(self, page_number: int) -> List[str]:
        soup, is_error_page = self.get_beautiful_soup_instance_by_url(self._create_url(page_number))
        if is_error_page:
            self.logger.error("Error Page")
            return []

        ul = soup.find(attrs=OFFERS_ID_A_HREF_ATTRIBUTES).find("ul")
        list_items = self._remove_related_offers(ul).select("li")
        a_hrefs = remove_none_items([list_item.find("a") for list_item in list_items])

        offers_id = [
            self.urlparse_path_replace(a_href.get("href"), SLASH_ITM)
            for a_href in a_hrefs
        ]

        # Removing redundant SCH_PAGE - somehow select("li") returns also div with this URL
        return [offer_id for offer_id in offers_id if offer_id != SCH_PAGE]


    def _remove_related_offers(self, tag: Tag) -> Tag:
        separator_div = tag.find(attrs=OFFERS_ID_RELATED_OFFERS_SEPARATOR_ATTRIBUTES)
        if separator_div is None:
            return tag

        hashed_children = [hash(child) for child in tag.children]
        if len(list(tag.children)) != len(hashed_children):
            raise ArraysLengthNotEqualException()

        separator_index = hashed_children.index(hash(separator_div))
        content = str(list(tag.children)[:separator_index])
        return self.get_beautiful_soup_instance_by_content(content)


    def _get_pages_range(self) -> range:
        soup, is_error_page = self.get_beautiful_soup_instance_by_url(self._create_url(1))
        if is_error_page:
            self.logger.error("Error Page")
            return range(0)

        items_number: int = int(
            soup.find(text=ITEMS_NUMBER_PHRASE)
                .find_parent()
                .select("span")[0]
                .get_text()
                .replace(",", "")
        )

        return self.calculate_page_ranges(items_number, ITEMS_PER_PAGE[1])


    def _create_url(self, page_number: int) -> str:
        return (EBAY_SEARCH_PATH + self.search_phrase + PARAM_BRAND_NEW + PARAM_BUY_NOW
                + LIST_VIEW + ITEMS_PER_PAGE[0] + PARAM_PAGE_NUMBER + str(page_number))
