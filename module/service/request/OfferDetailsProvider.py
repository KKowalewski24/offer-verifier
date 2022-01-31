from typing import Any, Dict, Optional, Tuple

from bs4 import BeautifulSoup, Tag

from module.constants import EBAY_ITEM_PATH, HTML_PARSER, OFFER_DESCRIPTION_ATTRIBUTES, \
    OFFER_IMAGE_ATTRIBUTES, OFFER_PRICE_ATTRIBUTES, OFFER_RATINGS_REVIEWS_ATTRIBUTES, \
    PRODUCT_RATINGS_KEYWORDS, RATINGS_CLASS_ATTRIBUTE, RETURNS_KEYWORD, RETURNS_NOT_ACCEPTED, \
    RETURNS_OPTION_ATTRIBUTES, RETURNS_OPTION_SPAN_ATTRIBUTES, RETURNS_OPTION_WHY_BUY_ATTRIBUTES, \
    REVIEWS_CLASS_ATTRIBUTE, SELLER_PANEL_ATTRIBUTES, SLASH_USR, TITLE_PANEL_ATTRIBUTES
from module.service.request.BaseProvider import BaseProvider
from module.utils import is_valid_item, normalize_text, remove_new_line_items, replace_many


class OfferDetailsProvider(BaseProvider):

    def get_offer_details(self, offer_id: str) -> Dict[str, Any]:
        soup, is_error_page = self.get_beautiful_soup_instance_by_url(EBAY_ITEM_PATH + offer_id)
        if is_error_page:
            self.logger.error("Error Page")
            return {}

        reviews_number, product_rating, ratings_number = self._get_ratings(soup)
        offer_json: Dict[str, Any] = {
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

        if None in list(offer_json.values()):
            self.logger.error("Wrong offer structure")
            return {}

        return offer_json


    def _get_title(self, soup: BeautifulSoup) -> Optional[str]:
        title_div = soup.find(attrs=TITLE_PANEL_ATTRIBUTES)
        if is_valid_item(title_div):
            h1_element = title_div.find("h1")
            if is_valid_item(h1_element):
                return str(list(h1_element.children)[1])

        return None


    def _get_price(self, soup: BeautifulSoup) -> Optional[str]:
        price_div = soup.find(attrs=OFFER_PRICE_ATTRIBUTES)
        if is_valid_item(price_div):
            return str(price_div.get("content").replace(",", ""))

        return None


    def _get_image_url(self, soup: BeautifulSoup) -> Optional[str]:
        image_div = soup.find(attrs=OFFER_IMAGE_ATTRIBUTES)
        if is_valid_item(image_div):
            return str(image_div.get("src"))

        return None


    def _get_return_option(self, soup: BeautifulSoup) -> Optional[bool]:
        returns_div = soup.find(attrs=RETURNS_OPTION_ATTRIBUTES)
        other_returns_div = soup.find(attrs=RETURNS_OPTION_WHY_BUY_ATTRIBUTES)
        if not is_valid_item(returns_div) or not is_valid_item(other_returns_div):
            return None

        returns_phrase: str = (
            returns_div.find_parent().find(attrs=RETURNS_OPTION_SPAN_ATTRIBUTES).get_text(strip=True)
        )
        other_returns_phrase: str = str(other_returns_div.get_text())

        return returns_phrase != RETURNS_NOT_ACCEPTED or RETURNS_KEYWORD in other_returns_phrase


    def _get_description_length(self, soup: BeautifulSoup) -> str:
        description_url: str = soup.find(attrs=OFFER_DESCRIPTION_ATTRIBUTES).get("src")
        description_soap, is_error_page = self.get_beautiful_soup_instance_by_url(description_url)

        if not is_error_page and is_valid_item(description_soap):
            return str(len(normalize_text(description_soap.get_text())))

        return str(0)


    def _get_ratings(self, soup: BeautifulSoup) -> Tuple[str, str, str]:
        ratings_reviews_div: Tag = soup.find(attrs=OFFER_RATINGS_REVIEWS_ATTRIBUTES)
        reviews_number: str = str(0)
        # If offer has no ratings, neutral value is returned - 3 is neutral
        product_rating: str = str(3)
        ratings_number: str = str(0)

        if is_valid_item(ratings_reviews_div):
            reviews_number = str(len(ratings_reviews_div.select(REVIEWS_CLASS_ATTRIBUTE)))
            ratings_spans = ratings_reviews_div.select(RATINGS_CLASS_ATTRIBUTE)

            if is_valid_item(ratings_spans):
                product_rating = normalize_text(ratings_spans[0].get_text()).replace(",", ".")
                ratings_number_text: str = normalize_text(ratings_spans[1].get_text())
                ratings_number = replace_many(ratings_number_text, PRODUCT_RATINGS_KEYWORDS)
            else:
                self.logger.info("ratings_spans does not exist")
        else:
            self.logger.info("ratings_reviews_div does not exist")

        return reviews_number, product_rating, ratings_number


    def _get_seller_id(self, soup: BeautifulSoup) -> Optional[str]:
        seller_div = soup.find(attrs=SELLER_PANEL_ATTRIBUTES)
        if is_valid_item(seller_div):
            markup: str = str(remove_new_line_items(list(seller_div.children))[2])
            a_element = BeautifulSoup(markup, HTML_PARSER).find("a")
            if is_valid_item(a_element):
                return self.urlparse_path_replace(a_element.get("href"), SLASH_USR)

        return None
