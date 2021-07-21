from typing import Dict, Tuple

# ----------------------------------------------------------------------- #
HTTP_OK: int = 200
UTF_8: str = "UTF-8"

RESULTS_DIRECTORY: str = "results/"
STATISTICS_PATH: str = RESULTS_DIRECTORY + "statistics.txt"
CURRENCY_PLN: str = "PLN"

# ----------------------------------------------------------------------- #
EBAY_BASE_PATH: str = "https://www.ebay.pl/"
EBAY_SEARCH_PATH: str = "https://www.ebay.pl/sch/i.html?_nkw="
PARAM_BRAND_NEW: str = "&LH_ItemCondition=3"
PARAM_BUY_NOW: str = "&LH_BIN=1"
PARAM_PAGE_NUMBER: str = "&_pgn="
ITEM_PER_PAGE: Tuple[str, int] = ("&_ipg=200", 200)

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

_DIV_ATTRIBUTES: Dict[str, str] = {}

# ----------------------------------------------------------------------- #
