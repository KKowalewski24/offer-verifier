from abc import ABC
from typing import Tuple
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from requests import Response
from requests.exceptions import ChunkedEncodingError

from module.constants import ERROR_PAGE_PHRASE, HTML_PARSER, REQUEST_HEADER
from module.service.Logger import Logger


class BaseProvider(ABC):

    def __init__(self) -> None:
        self.logger = Logger().get_logging_instance()


    def create_session(self) -> requests.Session:
        session: requests.Session = requests.Session()
        session.headers = REQUEST_HEADER
        return session


    def urlparse_path_replace(self, url: str, replaced_text: str, replacing_text: str = "") -> str:
        return urlparse(url).path.replace(replaced_text, replacing_text)


    def get_beautiful_soup_instance(self, url: str) -> Tuple[BeautifulSoup, bool]:
        response = self._make_request(url)
        self.logger.info("url: " + url + " ||| Status Code: " + str(response.status_code))
        soup: BeautifulSoup = BeautifulSoup(response.content, HTML_PARSER)
        is_error_page: bool = ERROR_PAGE_PHRASE in soup.title.string
        return soup, is_error_page


    def _make_request(self, url: str) -> Response:
        is_request_exception = True
        response = None

        while is_request_exception:
            try:
                response = self.create_session().get(url)
                is_request_exception = False
            except ChunkedEncodingError as e:
                self.logger.error("ChunkedEncodingError " + str(e))

        return response
