from abc import ABC
from typing import Tuple
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from module.constants import ERROR_PAGE_PHRASE, HTML_PARSER, REQUEST_HEADER
from module.service.Logger import Logger


class BaseProvider(ABC):

    def __init__(self) -> None:
        self.requests_session = self._create_session()
        self.logger = Logger().get_logging()


    def _create_session(self) -> requests.Session:
        session: requests.Session = requests.Session()
        session.headers = REQUEST_HEADER
        return session


    def get_beautiful_soup_instance(self, url: str) -> Tuple[BeautifulSoup, bool]:
        response = self.requests_session.get(url)
        self.logger.info("url: " + url + " ||| Status Code: " + str(response.status_code))
        soup: BeautifulSoup = BeautifulSoup(response.content, HTML_PARSER)
        is_error_page: bool = ERROR_PAGE_PHRASE in soup.title.string
        return soup, is_error_page


    def urlparse_path_replace(self, url: str, replaced_text: str, replacing_text: str = "") -> str:
        return urlparse(url).path.replace(replaced_text, replacing_text)
