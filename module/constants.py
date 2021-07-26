from typing import Dict, Tuple

# ----------------------------------------------------------------------- #
HTML_PARSER: str = "html.parser"

HTTP_OK: int = 200
UTF_8: str = "UTF-8"

RESULTS_DIRECTORY: str = "results/"
STATISTICS_PATH: str = RESULTS_DIRECTORY + "statistics.txt"
CURRENCY_PLN: str = "PLN"

# ----------------------------------------------------------------------- #
SLASH: str = "/"
PARAM_BRAND_NEW: str = "&LH_ItemCondition=1000"
PARAM_BUY_NOW: str = "&LH_BIN=1"
ITEMS_PER_PAGE: Tuple[str, int] = ("&_ipg=200", 200)
PARAM_PAGE_NUMBER: str = "&_pgn="
PARAM_QUERY = "sch/i.html?_nkw="

ITM: str = "itm/"
SLASH_ITM: str = SLASH + ITM
USR: str = "usr/"
SLASH_USR: str = SLASH + USR

EBAY_BASE_PATH: str = "https://www.ebay.com/"
EBAY_SEARCH_PATH: str = EBAY_BASE_PATH + PARAM_QUERY
EBAY_ITEM_PATH: str = EBAY_BASE_PATH + ITM

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
    "tabindex": "-1"
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
    "id": "returnsPlacementHolderId"
}

RETURNS_OPTION_SPAN_ATTRIBUTES: Dict[str, str] = {
    "id": "vi-ret-accrd-txt"
}

RETURNS_OPTION_WHY_BUY_ATTRIBUTES: Dict[str, str] = {
    "id": "why2buy"
}

OFFER_DESCRIPTION_ATTRIBUTES: Dict[str, str] = {
    "id": "desc_ifr"
}

OFFER_RATINGS_ATTRIBUTES: Dict[str, str] = {
    "id": "rwid"
}

SELLER_PANEL_ATTRIBUTES: Dict[str, str] = {
    "id": "RightSummaryPanel"
}

# ----------------------------------------------------------------------- #
ITEMS_NUMBER_PHRASE: str = " results for "
RETURNS_NOT_ACCEPTED: str = "Seller does not accept returns"
RETURNS_KEYWORD: str = "returns"
PRODUCT_RATINGS: str = "product ratings"
