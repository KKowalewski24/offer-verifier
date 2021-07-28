from typing import Any, Dict

from module.service.Logger import Logger
from module.service.request.BaseProvider import BaseProvider


class SellerDetailsProvider(BaseProvider):

    def __init__(self) -> None:
        super().__init__()
        self.logger: Logger = Logger()


    def get_seller_details(self, seller_id: str) -> Dict[str, Any]:
        return {
            "id": seller_id
        }
