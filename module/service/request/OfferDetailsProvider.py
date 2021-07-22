from typing import Dict

from module.constants import EBAY_ITEM_PATH
from module.service.request.BaseProvider import BaseProvider


class OfferDetailsProvider(BaseProvider):

    def __init__(self) -> None:
        super().__init__()


    def get_offer_details(self, offer_id: str) -> Dict[str, str]:
        self.requests_session.get(EBAY_ITEM_PATH + offer_id)
        return {
            "offer_id": offer_id,
            "seller_id": "-1"
        }
