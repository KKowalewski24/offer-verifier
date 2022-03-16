from typing import Any, Dict, List, Optional, Tuple

from bs4 import BeautifulSoup, Tag

from module.constants import EBAY_ITEM_PATH, HTML_PARSER, OFFER_DESCRIPTION_ATTRIBUTES, \
    OFFER_IMAGE_ATTRIBUTES, OFFER_PRICE_ATTRIBUTES, OFFER_RATINGS_REVIEWS_ATTRIBUTES, RATINGS_HISTOGRAM, \
    RETURNS_NEGATION, RETURNS_NOT_ACCEPTED, RETURNS_OPTION_ATTRIBUTES, REVIEWS_CLASS_ATTRIBUTE, REVIEWS_COUNT, \
    REVIEWS_HEADER, REVIEW_ITEMS_PER_PAGE, REVIEW_NEGATIVE_VOTE, REVIEW_PARAM_PAGE_NUMBER, \
    REVIEW_POSITIVE_VOTE, SELLER_PANEL_ATTRIBUTES, SLASH_USR, TITLE_PANEL_ATTRIBUTES
from module.service.request.BaseProvider import BaseProvider
from module.utils import flat_map_list, is_valid_item, normalize_text, remove_new_line_items


class OfferDetailsProvider(BaseProvider):

    def get_offer_details(self, offer_id: str) -> Dict[str, Any]:
        soup, is_error_page = self.get_beautiful_soup_instance_by_url(EBAY_ITEM_PATH + offer_id)
        if is_error_page:
            self.logger.error("Error Page")
            return {}

        ratings, reviews = self._get_ratings_reviews(soup)
        offer_json: Dict[str, Any] = {
            "id": offer_id,
            "title": self._get_title(soup),
            "price": self._get_price(soup),
            "image_url": self._get_image_url(soup),
            "has_return_option": self._get_return_option(soup),
            "description_length": self._get_description_length(soup),
            "ratings": ratings,
            "reviews": reviews,
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
                return h1_element.get_text(strip=True)

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
        if not is_valid_item(returns_div):
            return None

        returns_phrase: str = (
            returns_div.find("a").find_parent().find_all("span")[0].get_text(strip=True)
        )

        return returns_phrase != RETURNS_NOT_ACCEPTED or RETURNS_NEGATION not in returns_phrase


    def _get_description_length(self, soup: BeautifulSoup) -> str:
        description_url: str = soup.find(attrs=OFFER_DESCRIPTION_ATTRIBUTES).get("src")
        description_soap, is_error_page = self.get_beautiful_soup_instance_by_url(description_url)

        if not is_error_page and is_valid_item(description_soap):
            return str(len(normalize_text(description_soap.get_text())))

        return str(0)


    def _get_seller_id(self, soup: BeautifulSoup) -> Optional[str]:
        seller_div = soup.find(attrs=SELLER_PANEL_ATTRIBUTES)
        if is_valid_item(seller_div):
            markup: str = str(remove_new_line_items(list(seller_div.children))[2])
            a_element = BeautifulSoup(markup, HTML_PARSER).find("a")
            if is_valid_item(a_element):
                return self.urlparse_path_replace(a_element.get("href"), SLASH_USR)

        return None


    def _get_ratings_reviews(self, soup: BeautifulSoup) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
        ratings_reviews_div: Tag = soup.find(attrs=OFFER_RATINGS_REVIEWS_ATTRIBUTES)
        ratings: List[Dict[str, str]] = []
        reviews: List[Dict[str, str]] = []

        if is_valid_item(ratings_reviews_div):
            reviews_header = ratings_reviews_div.find(attrs=REVIEWS_HEADER).find("div")
            if is_valid_item(reviews_header):
                a_element = reviews_header.find("a")
                ratings = self.__get_ratings(ratings_reviews_div)
                reviews = (
                    self.__get_reviews_when_many(str(a_element.get("href")))
                    if a_element is not None
                    else self.__get_reviews_when_few(ratings_reviews_div)
                )

                # Removing stars_number from ratings in order to disjoint this two sets - originally
                # website aggregate stars_number from ratings and reviews that is why it needs to be removed
                for stars_number in [review["stars_number"] for review in reviews]:
                    ratings.remove({"stars_number": str(stars_number)})
            else:
                self.logger.info("reviews_header does not exist")
        else:
            self.logger.info("ratings_reviews_div does not exist")

        return ratings, reviews


    def __get_ratings(self, ratings_reviews_div: Tag) -> List[Dict[str, str]]:
        ratings: List[Dict[str, str]] = []

        for rating_div in ratings_reviews_div.find(attrs=RATINGS_HISTOGRAM).find_all("li"):
            div_elements = rating_div.div.find_all("div")
            star_value = div_elements[0].find("p").get_text(strip=True)
            star_count = int(div_elements[1].find("span").get_text(strip=True))
            for _ in range(star_count):
                ratings.append({"stars_number": str(star_value)})

        return ratings


    def __get_reviews_when_few(self, ratings_reviews_div: Tag) -> List[Dict[str, str]]:
        return [
            self.__extract_data_from_reviews_when_few(review_div)
            for review_div in ratings_reviews_div.select(REVIEWS_CLASS_ATTRIBUTE)
        ]


    def __extract_data_from_reviews_when_few(self, review_div: Tag) -> Dict[str, str]:
        stars: int = int(float(review_div.div.div.get("aria-label").split()[0]))

        p_elements: str = review_div.find_all("div")[2].find_all("p")
        text_content: str = (f"{normalize_text(p_elements[0].get_text(strip=True))}."
                             f" {normalize_text(p_elements[1].get_text(strip=True))}")
        positive_votes = review_div.find(attrs=REVIEW_POSITIVE_VOTE).get_text(strip=True)
        negative_votes = review_div.find(attrs=REVIEW_NEGATIVE_VOTE).get_text(strip=True)

        contains_images: bool = len(review_div.find_all("img")) > 0

        return {
            "stars_number": str(stars),
            "text_content": text_content,
            "positive_votes_number": positive_votes,
            "negative_votes_number": negative_votes,
            "contains_images": contains_images
        }


    def __get_reviews_when_many(self, all_reviews_url: str) -> List[Dict[str, str]]:
        soup, is_error_page = self.get_beautiful_soup_instance_by_url(all_reviews_url)
        if is_error_page:
            self.logger.error("Error Page")
            return [{}]

        items_number: int = int(soup.find(attrs=REVIEWS_COUNT).get_text(strip=True).split()[0])
        reviews: List[List[Dict[str, str]]] = []

        for page_number in self.calculate_page_ranges(items_number, REVIEW_ITEMS_PER_PAGE):
            soup, is_error_page = self.get_beautiful_soup_instance_by_url(
                f"{all_reviews_url}{REVIEW_PARAM_PAGE_NUMBER}{page_number}"
            )
            if is_error_page:
                self.logger.error("Error Page")
                return [{}]

            reviews.append([
                self.__extract_data_from_reviews_when_many(review_div)
                for review_div in soup.select(REVIEWS_CLASS_ATTRIBUTE)[:-1]
            ])

        return flat_map_list(reviews)


    def __extract_data_from_reviews_when_many(self, review_div: Tag) -> Dict[str, str]:
        stars: int = int(float(review_div.div.div.get("title").split()[0]))

        review_section: str = review_div.find_all("div")[2]
        text_content: str = (f"{normalize_text(review_section.find('h3').get_text(strip=True))}."
                             f" {normalize_text(review_section.find('p').get_text(strip=True))}")
        positive_votes = review_div.find(attrs=REVIEW_POSITIVE_VOTE).get_text(strip=True)
        negative_votes = review_div.find(attrs=REVIEW_NEGATIVE_VOTE).get_text(strip=True)

        contains_images: bool = len(review_div.find_all("img")) > 0

        return {
            "stars_number": str(stars),
            "text_content": text_content,
            "positive_votes_number": positive_votes,
            "negative_votes_number": negative_votes,
            "contains_images": contains_images
        }
