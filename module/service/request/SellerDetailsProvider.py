from typing import Any, Dict, Tuple

from bs4 import BeautifulSoup, ResultSet, Tag

from module.constants import DETAILED_CONTENT_EXTRA_WORD, DETAILED_SELLER_RATINGS_ATTRIBUTES, \
    DETAILED_SELLER_STARS_FOUR_ATTRIBUTES, DETAILED_SELLER_STARS_ONE_ATTRIBUTES, \
    DETAILED_SELLER_STARS_THREE_ATTRIBUTES, DETAILED_SELLER_STARS_TWO_ATTRIBUTES, \
    EBAY_USER_DETAILS_PATH, EBAY_USER_PATH, FEEDBACK_OVERALL_RATINGS_ATTRIBUTES, POSITIVE_FEEDBACK, \
    SELLER_BASIC_INFO_ATTRIBUTES, SELLER_MEMBER_INFO_ATTRIBUTES
from module.service.Logger import Logger
from module.service.request.BaseProvider import BaseProvider
from module.utils import normalize_text, replace_many


class SellerDetailsProvider(BaseProvider):

    def __init__(self) -> None:
        super().__init__()
        self.logger: Logger = Logger()


    def get_seller_details(self, seller_id: str) -> Dict[str, Any]:
        basic_soup, is_error_page = self.get_beautiful_soup_instance(EBAY_USER_PATH + seller_id)
        details_soup, is_error_details_page = self.get_beautiful_soup_instance(
            EBAY_USER_DETAILS_PATH + seller_id
        )

        if is_error_page or is_error_details_page:
            self.logger.error("Error Page")
            return {}

        feedback_score, feedback_percentage = self._get_basic_stats(basic_soup)
        positive_ratings, neutral_ratings, negative_ratings = self._get_feedback_ratings(details_soup)
        (accurate_description, reasonable_shipping_cost,
         shipping_speed, communication) = self._get_detailed_ratings(details_soup)

        return {
            "id": seller_id,
            "seller_feedback_score": feedback_score,
            "seller_feedback_percentage": feedback_percentage,
            "year_of_joining": self._get_year_of_joining(basic_soup),
            "seller_positive_ratings_number": positive_ratings,
            "seller_neutral_ratings_number": neutral_ratings,
            "seller_negative_ratings_number": negative_ratings,
            "accurate_description": accurate_description,
            "reasonable_shipping_cost": reasonable_shipping_cost,
            "shipping_speed": shipping_speed,
            "communication": communication,
        }


    def _get_basic_stats(self, soup: BeautifulSoup) -> Tuple[str, str]:
        stats_div = soup.find(attrs=SELLER_BASIC_INFO_ATTRIBUTES)
        feedback_score: str = str(0)
        feedback_percentage: str = str(0)

        if stats_div is not None and len(stats_div) != 0:
            self.logger.info("stats_div exists")
            a_href = stats_div.select("div")[0].select("span")[0].select("a")
            if a_href is not None and len(a_href) > 1:
                feedback_score_span: Tag = a_href[1]
                feedback_score = feedback_score_span.find(text=True, recursive=False).strip()

            feedback_percent_text: str = stats_div.select("div")[1].get_text()
            if feedback_percent_text != "":
                feedback_percentage = (normalize_text(feedback_percent_text)
                                       .replace(POSITIVE_FEEDBACK, ""))

        return feedback_score, feedback_percentage


    def _get_year_of_joining(self, soup: BeautifulSoup) -> str:
        member_info_spans = soup.find(
            attrs=SELLER_MEMBER_INFO_ATTRIBUTES
        ).find_all("span", recursive=False)

        date_text: str = member_info_spans[4].find_all("span")[1].get_text()
        comma_separator = ", "
        return date_text[date_text.index(comma_separator) + len(comma_separator):]


    def _get_feedback_ratings(self, soup: BeautifulSoup) -> Tuple[str, str, str]:
        ratings_section = soup.find(attrs=FEEDBACK_OVERALL_RATINGS_ATTRIBUTES)
        positive_ratings: str = str(0)
        neutral_ratings: str = str(0)
        negative_ratings: str = str(0)

        if ratings_section is not None and len(ratings_section) != 0:
            self.logger.info("ratings_section exists")
            table_rows = ratings_section.find("table").find("tbody").select("tr")
            positive_ratings = self.__get_feedback_td_content(table_rows[0])
            neutral_ratings = self.__get_feedback_td_content(table_rows[1])
            negative_ratings = self.__get_feedback_td_content(table_rows[2])

        return positive_ratings, neutral_ratings, negative_ratings


    def __get_feedback_td_content(self, table_rows: ResultSet) -> str:
        return table_rows.select("td")[2].get_text()


    def _get_detailed_ratings(self, soup: BeautifulSoup) -> Tuple[str, str, str, str]:
        ratings_section = soup.find(attrs=DETAILED_SELLER_RATINGS_ATTRIBUTES)
        # If seller has no ratings in selected category, neutral value is returned - 3 is neutral
        accurate_description: str = str(3)
        reasonable_shipping_cost: str = str(3)
        shipping_speed: str = str(3)
        communication: str = str(3)

        if ratings_section is not None and len(ratings_section) != 0:
            self.logger.info("ratings_section exists")
            accurate_description = self.__get_detailed_content(
                ratings_section, DETAILED_SELLER_STARS_ONE_ATTRIBUTES
            )
            reasonable_shipping_cost = self.__get_detailed_content(
                ratings_section, DETAILED_SELLER_STARS_TWO_ATTRIBUTES
            )
            shipping_speed = self.__get_detailed_content(
                ratings_section, DETAILED_SELLER_STARS_THREE_ATTRIBUTES
            )
            communication = self.__get_detailed_content(
                ratings_section, DETAILED_SELLER_STARS_FOUR_ATTRIBUTES
            )

        return accurate_description, reasonable_shipping_cost, shipping_speed, communication


    def __get_detailed_content(self, ratings_section: Tag, attributes: Dict[str, str]) -> str:
        stars_span: Tag = ratings_section.find(attrs=attributes)
        if stars_span is not None and len(stars_span) != 0:
            self.logger.info("stars_span exists")
            return replace_many(stars_span.find("span").get("style"), DETAILED_CONTENT_EXTRA_WORD)

        return str(3)
