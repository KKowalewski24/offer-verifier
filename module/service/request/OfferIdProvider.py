from typing import List

from module.service.request.BaseProvider import BaseProvider


class OfferIdProvider(BaseProvider):

    def __init__(self, search_phrase: str) -> None:
        super().__init__()
        self.search_phrase = search_phrase


    def get_offers_id(self) -> List[str]:
        return []
