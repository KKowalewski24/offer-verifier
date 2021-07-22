from typing import Dict, List

from module.model.Offer import Offer
from module.model.Seller import Seller
from module.service.request.OfferDetailsProvider import OfferDetailsProvider
from module.service.request.OfferIdProvider import OfferIdProvider
from module.service.request.SellerDetailsProvider import SellerDetailsProvider


class RequestProvider:

    def __init__(self, search_phrase: str) -> None:
        self.offer_id_provider: OfferIdProvider = OfferIdProvider(search_phrase)
        self.offer_details_provider: OfferDetailsProvider = OfferDetailsProvider()
        self.seller_details_provider: SellerDetailsProvider = SellerDetailsProvider()


    def get_offers(self) -> List[Offer]:
        return [
            self._prepare_offer(offer_id)
            for offer_id in self.offer_id_provider.get_offers_id()
        ]


    def _prepare_offer(self, offer_id: str) -> Offer:
        offer_details = self.offer_details_provider.get_offer_details(offer_id)
        seller_details = self.seller_details_provider.get_seller_details(offer_details["seller_id"])
        return self._map_json_to_offer(offer_details, seller_details)


    def _map_json_to_offer(self, offer_details: Dict[str, str],
                           seller_details: Dict[str, str]) -> Offer:
        return Offer(
            offer_details["offer_id"],
            Seller(
                seller_details["seller_id"]
            )
        )
