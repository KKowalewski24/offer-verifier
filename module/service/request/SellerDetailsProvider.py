from typing import Dict

from module.service.request.BaseProvider import BaseProvider


class SellerDetailsProvider(BaseProvider):

    def __init__(self) -> None:
        super().__init__()


    def get_seller_details(self, seller_id: str) -> Dict[str, str]:
        return {
            "seller_id": seller_id
        }
