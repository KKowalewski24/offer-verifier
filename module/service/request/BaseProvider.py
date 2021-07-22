from abc import ABC

import requests
from bs4 import BeautifulSoup

from module.constants import REQUEST_HEADER


class BaseProvider(ABC):

    def __init__(self) -> None:
        self.requests_session = self._create_session()


    def _create_session(self) -> requests.Session:
        session: requests.Session = requests.Session()
        session.headers = REQUEST_HEADER
        return session


    def _get_beautiful_soup_instance(self, url: str) -> BeautifulSoup:
        return BeautifulSoup(self.requests_session.get(url).content, "html.parser")
