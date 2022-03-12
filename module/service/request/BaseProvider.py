from abc import ABC
from typing import Tuple
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup, Comment
from requests import Response
from requests.exceptions import ChunkedEncodingError

from module.constants import ERROR_PAGE_PHRASE, HTML_PARSER, REQUEST_HEADER
from module.service.common.Logger import Logger


class BaseProvider(ABC):

    def __init__(self) -> None:
        self.logger = Logger().get_logging_instance()


    def get_beautiful_soup_instance_by_url(self, url: str) -> Tuple[BeautifulSoup, bool]:
        response = self.make_request(url)
        self.logger.info("url: " + url + " ||| Status Code: " + str(response.status_code))
        soup: BeautifulSoup = self.get_beautiful_soup_instance_by_content(response.content)
        self.remove_html_comments(soup)

        is_error_page: bool = False
        if soup.title.string is not None:
            is_error_page = ERROR_PAGE_PHRASE in soup.title.string
        if soup.title.string is None:
            is_error_page = True

        return soup, is_error_page


    def make_request(self, url: str) -> Response:
        is_request_exception = True
        response = None

        while is_request_exception:
            try:
                response = self.create_session().get(url)
                is_request_exception = False
            except ChunkedEncodingError as e:
                self.logger.error("ChunkedEncodingError " + str(e))

        return response


    def create_session(self) -> requests.Session:
        session: requests.Session = requests.Session()
        session.headers = REQUEST_HEADER
        return session


    def get_beautiful_soup_instance_by_content(self, content: str) -> BeautifulSoup:
        return BeautifulSoup(content, HTML_PARSER)


    def remove_html_comments(self, soup: BeautifulSoup) -> None:
        for comment in soup.find_all(text=lambda text: isinstance(text, Comment)):
            comment.extract()


    def urlparse_path_replace(self, url: str, replaced_text: str, replacing_text: str = "") -> str:
        return urlparse(url).path.replace(replaced_text, replacing_text)
