from typing import Any, Dict, Tuple

from bs4 import BeautifulSoup, ResultSet, Tag

from module.constants import EBAY_USER_DETAILS_PATH, EBAY_USER_PATH, \
    FEEDBACK_OVERALL_RATINGS_CLASS_ATTRIBUTE, POSITIVE_FEEDBACK, SELLER_BASIC_INFO, SELLER_MEMBER_INFO
from module.service.Logger import Logger
from module.service.request.BaseProvider import BaseProvider
from module.utils import normalize_text


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
        self._get_detailed_ratings(details_soup)

        return {
            "id": seller_id,
            "feedback_score": feedback_score,
            "feedback_percentage": feedback_percentage,
            "year_of_joining": self._get_year_of_joining(basic_soup),
            "positive_ratings": positive_ratings,
            "neutral_ratings": neutral_ratings,
            "negative_ratings": negative_ratings
        }


    def _get_basic_stats(self, soup: BeautifulSoup) -> Tuple[str, str]:
        stats_div = soup.find(attrs=SELLER_BASIC_INFO)
        feedback_score: str = str(0)
        feedback_percentage: str = str(0)

        if stats_div is not None and len(stats_div) != 0:
            feedback_score_span: Tag = stats_div.select("div")[0].select("span")[0].select("a")[1]
            feedback_score = feedback_score_span.find(text=True, recursive=False).strip()

            feedback_percent_text: str = stats_div.select("div")[1].get_text()
            feedback_percentage = normalize_text(feedback_percent_text).replace(POSITIVE_FEEDBACK, "")

        return feedback_score, feedback_percentage


    def _get_year_of_joining(self, soup: BeautifulSoup) -> str:
        member_info_spans = soup.find(attrs=SELLER_MEMBER_INFO).find_all("span", recursive=False)
        date_text: str = member_info_spans[4].find_all("span")[1].get_text()
        comma_separator = ", "
        return date_text[date_text.index(comma_separator) + len(comma_separator):]


    def _get_feedback_ratings(self, soup: BeautifulSoup) -> Tuple[str, str, str]:
        ratings_section = soup.find(attrs=FEEDBACK_OVERALL_RATINGS_CLASS_ATTRIBUTE)
        positive_ratings: str = str(0)
        neutral_ratings: str = str(0)
        negative_ratings: str = str(0)

        if ratings_section is not None and len(ratings_section) != 0:
            table_rows = ratings_section.find("table").find("tbody").select("tr")
            positive_ratings = self.__get_td_content(table_rows[0])
            neutral_ratings = self.__get_td_content(table_rows[1])
            negative_ratings = self.__get_td_content(table_rows[2])

        return positive_ratings, neutral_ratings, negative_ratings


    def __get_td_content(self, table_rows: ResultSet) -> str:
        return table_rows.select("td")[2].get_text()


    def _get_detailed_ratings(self, soup: BeautifulSoup) -> str:
        return ""
