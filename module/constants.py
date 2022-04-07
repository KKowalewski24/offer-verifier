from typing import Dict, List, Tuple

# ----------------------------------------------------------------------- #
HTML_PARSER: str = "html.parser"
LOGS_FILENAME: str = "app.log"

HTTP_OK: int = 200
UTF_8: str = "UTF-8"

OFFER_REPORT_FILENAME: Tuple[str, str] = (
    "credible_offer_report", "not_credible_offer_report"
)
PDF_MAX_LINE_LENGTH: int = 85
RESULTS_DIRECTORY: str = "results/"
STATISTICS_PATH: str = RESULTS_DIRECTORY + "statistics.txt"
OFFERS_PATH: str = RESULTS_DIRECTORY + "offers-"
CURRENCY_US_DOLLAR: str = "US $"
PICKLE_EXTENSION: str = ".pickle"
PDF_EXTENSION: str = ".pdf"
LANGDETECT_ENGLISH = "en"
MIN_MAX_REVIEW_VALUE: Tuple[float, float] = (1.0, 5.0)
AFFECT_FREQUENCIES_KEY: List[str] = [
    "fear", "anger", "anticip", "trust", "surprise",
    "positive", "negative", "sadness", "disgust", "joy"
]

# ----------------------------------------------------------------------- #
SLASH: str = "/"
PARAM_QUERY = "sch/i.html?_nkw="
PARAM_BRAND_NEW: str = "&LH_ItemCondition=1000"
PARAM_BUY_NOW: str = "&LH_BIN=1"
LIST_VIEW: str = "&_dmd=2"
ITEMS_PER_PAGE: Tuple[str, int] = ("&_ipg=240", 240)
PARAM_PAGE_NUMBER: str = "&_pgn="
REVIEW_ITEMS_PER_PAGE: int = 10
REVIEW_PARAM_PAGE_NUMBER: str = "&pgn="

ITM: str = "itm/"
SLASH_ITM: str = SLASH + ITM
USR: str = "usr/"
SLASH_USR: str = SLASH + USR
FEEDBACK_PROFILE: str = "fdbk/feedback_profile/"
SCH_PAGE: str = "/sch/i.html"

EBAY_BASE_PATH: str = "https://www.ebay.com/"
EBAY_SEARCH_PATH: str = EBAY_BASE_PATH + PARAM_QUERY
EBAY_ITEM_PATH: str = EBAY_BASE_PATH + ITM
EBAY_USER_PATH: str = EBAY_BASE_PATH + USR
EBAY_USER_DETAILS_PATH: str = EBAY_BASE_PATH + FEEDBACK_PROFILE

# ----------------------------------------------------------------------- #
REQUEST_HEADER: Dict[str, str] = {
    'authority': 'www.ebay.pl',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'pl-PL,pl;q=0.9',
}

OFFERS_ID_A_HREF_ATTRIBUTES: Dict[str, str] = {
    "id": "srp-river-results"
}

OFFERS_ID_RELATED_OFFERS_SEPARATOR_ATTRIBUTES: Dict[str, str] = {
    "class": "srp-river-answer srp-river-answer--REWRITE_START"
}

TITLE_PANEL_ATTRIBUTES: Dict[str, str] = {
    "id": "LeftSummaryPanel"
}

OFFER_PRICE_ATTRIBUTES: Dict[str, str] = {
    "itemprop": "price"
}

OFFER_IMAGE_ATTRIBUTES: Dict[str, str] = {
    "id": "icImg",
    "itemprop": "image"
}

RETURNS_OPTION_ATTRIBUTES: Dict[str, str] = {
    "data-testid": "x-returns-minview"
}

RETURNS_OPTION_SPAN_ATTRIBUTES: Dict[str, str] = {
    "id": "vi-ret-accrd-txt"
}

OFFER_DESCRIPTION_ATTRIBUTES: Dict[str, str] = {
    "id": "desc_ifr"
}

OFFER_RATINGS_REVIEWS_ATTRIBUTES: Dict[str, str] = {
    "id": "rwid"
}

RATINGS_HISTOGRAM: Dict[str, str] = {
    "class": "reviews-histogram"
}

REVIEWS_CLASS_ATTRIBUTE: str = ".reviews > div"

REVIEWS_HEADER: Dict[str, str] = {
    "class": "reviews-right"
}

REVIEWS_COUNT: Dict[str, str] = {
    "class": "p-rvw-count"
}

REVIEWS_IMAGES: Dict[str, str] = {
    "class": "reviews-images"
}

REVIEW_VOTE: Dict[str, str] = {
    "name": "vote"
}

REVIEW_POSITIVE_VOTE: Dict[str, str] = {
    "class": "positive-h-c"
}

REVIEW_NEGATIVE_VOTE: Dict[str, str] = {
    "class": "negative-h-c"
}

SELLER_PANEL_ATTRIBUTES: Dict[str, str] = {
    "id": "RightSummaryPanel"
}

SELLER_BASIC_INFO_ATTRIBUTES: Dict[str, str] = {
    "id": "user_info"
}

SELLER_MEMBER_INFO_ATTRIBUTES: Dict[str, str] = {
    "id": "member_info"
}

FEEDBACK_OVERALL_RATINGS_ATTRIBUTES: Dict[str, str] = {
    "class": "overall-rating-summary"
}

DETAILED_SELLER_RATINGS_ATTRIBUTES: Dict[str, str] = {
    "class": "dsr-summary"
}

DETAILED_SELLER_STARS_ONE_ATTRIBUTES: Dict[str, str] = {
    "data-test-id": "dsr-stars-1"
}

DETAILED_SELLER_STARS_TWO_ATTRIBUTES: Dict[str, str] = {
    "data-test-id": "dsr-stars-2"
}

DETAILED_SELLER_STARS_THREE_ATTRIBUTES: Dict[str, str] = {
    "data-test-id": "dsr-stars-3"
}

DETAILED_SELLER_STARS_FOUR_ATTRIBUTES: Dict[str, str] = {
    "data-test-id": "dsr-stars-4"
}

# ----------------------------------------------------------------------- #
ERROR_PAGE_PHRASE: str = "Error Page"
ITEMS_NUMBER_PHRASE: str = " results for "
RETURNS_NOT_ACCEPTED: str = "Seller does not accept returns"
RETURNS_NEGATION: str = "does not"
READ_FULL_REVIEW: str = "Read full review..."
PRODUCT_RATINGS_KEYWORDS: List[str] = [
    " product", " ratings", " rating"
]
POSITIVE_FEEDBACK: str = "% positive feedback"
DETAILED_CONTENT_EXTRA_WORD: List[str] = [
    "width: ", "rem"
]
