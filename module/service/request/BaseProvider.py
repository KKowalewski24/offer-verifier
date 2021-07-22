from abc import ABC
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from module.constants import HTML_PARSER, REQUEST_HEADER


class BaseProvider(ABC):

    def __init__(self) -> None:
        self.requests_session = self._create_session()


    def _create_session(self) -> requests.Session:
        session: requests.Session = requests.Session()
        session.headers = REQUEST_HEADER
        return session


    def get_beautiful_soup_instance(self, url: str) -> BeautifulSoup:
        return BeautifulSoup(self.requests_session.get(url).content, HTML_PARSER)


    def urlparse_path_replace(self, url: str, replaced_text: str, replacing_text: str = "") -> str:
        return urlparse(url).path.replace(replaced_text, replacing_text)
