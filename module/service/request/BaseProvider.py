from abc import ABC

import requests

from module.constants import EBAY_BASE_PATH, REQUEST_HEADER


class BaseProvider(ABC):

    def __init__(self) -> None:
        self.requests_session = self._create_session()


    def _create_session(self) -> requests.Session:
        session: requests.Session = requests.Session()
        session.get(EBAY_BASE_PATH, headers=REQUEST_HEADER)
        return session
    # TODO