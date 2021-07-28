from typing import Any, Dict, Tuple

from bs4 import BeautifulSoup, Tag

from module.constants import EBAY_ITEM_PATH, HTML_PARSER, OFFER_DESCRIPTION_ATTRIBUTES, \
    OFFER_IMAGE_ATTRIBUTES, OFFER_PRICE_ATTRIBUTES, OFFER_RATINGS_REVIEWS_ATTRIBUTES, \
    PRODUCT_RATINGS_KEYWORDS, RATINGS_CLASS_ATTRIBUTE, RETURNS_KEYWORD, RETURNS_NOT_ACCEPTED, \
    RETURNS_OPTION_ATTRIBUTES, RETURNS_OPTION_SPAN_ATTRIBUTES, RETURNS_OPTION_WHY_BUY_ATTRIBUTES, \
    REVIEWS_CLASS_ATTRIBUTE, SELLER_PANEL_ATTRIBUTES, SLASH_USR, TITLE_PANEL_ATTRIBUTES
from module.service.Logger import Logger
from module.service.request.BaseProvider import BaseProvider
from module.utils import normalize_text, remove_new_line_items, replace_many


class OfferDetailsProvider(BaseProvider):

    def __init__(self) -> None:
        super().__init__()
        self.logger: Logger = Logger()


    def get_offer_details(self, offer_id: str) -> Dict[str, Any]:
        soup, is_error_page = self.get_beautiful_soup_instance(EBAY_ITEM_PATH + offer_id)
        if is_error_page:
            self.logger.error("Error Page")
            return {}

        reviews_number, product_rating, ratings_number = self._get_ratings(soup)
        return {
            "id": offer_id,
            "title": self._get_title(soup),
            "price": self._get_price(soup),
            "image_url": self._get_image_url(soup),
            "has_return_option": self._get_return_option(soup),
            "description_length": self._get_description_length(soup),
            "product_reviews_number": reviews_number,
            "product_rating": product_rating,
            "product_ratings_number": ratings_number,
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


    def _get_description_length(self, soup: BeautifulSoup) -> str:
        description_url: str = soup.find(attrs=OFFER_DESCRIPTION_ATTRIBUTES).get("src")
        description_soap, is_error_page = self.get_beautiful_soup_instance(description_url)

        if not is_error_page and description_soap is not None and len(description_soap) != 0:
            return str(len(normalize_text(description_soap.get_text())))

        return str(0)


    def _get_ratings(self, soup: BeautifulSoup) -> Tuple[str, str, str]:
        ratings_reviews_div: Tag = soup.find(attrs=OFFER_RATINGS_REVIEWS_ATTRIBUTES)
        reviews_number: str = str(0)
        # If offer has no ratings, neutral value is returned - 3 is neutral
        product_rating: str = str(3)
        ratings_number: str = str(0)

        if ratings_reviews_div is not None and len(ratings_reviews_div) != 0:
            self.logger.info("ratings_reviews_div exists")
            reviews_number = str(len(ratings_reviews_div.select(REVIEWS_CLASS_ATTRIBUTE)))
            ratings_spans = ratings_reviews_div.select(RATINGS_CLASS_ATTRIBUTE)

            if ratings_spans is not None and len(ratings_spans) != 0:
                self.logger.info("ratings_spans exists")
                product_rating = normalize_text(ratings_spans[0].get_text()).replace(",", ".")
                ratings_number_text: str = normalize_text(ratings_spans[1].get_text())
                ratings_number = replace_many(ratings_number_text, PRODUCT_RATINGS_KEYWORDS)

        return reviews_number, product_rating, ratings_number


    def _get_seller_id(self, soup: BeautifulSoup) -> str:
        markup: str = str(
            remove_new_line_items(list(soup.find(attrs=SELLER_PANEL_ATTRIBUTES).children))[2]
        )
        url: str = BeautifulSoup(markup, HTML_PARSER).find("a").get("href")
        return self.urlparse_path_replace(url, SLASH_USR)
