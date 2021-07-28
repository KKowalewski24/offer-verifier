from typing import Any, Dict, Tuple

from bs4 import BeautifulSoup, Tag

from module.constants import EBAY_USER_DETAILS_PATH, EBAY_USER_PATH, POSITIVE_FEEDBACK, \
    SELLER_BASIC_INFO
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
        return {
            "id": seller_id,
            "feedback_score": feedback_score,
            "feedback_percentage": feedback_percentage
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
