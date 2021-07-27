from typing import Any, Dict, List, Optional

from module.model.Offer import Offer
from module.model.Seller import Seller
from module.service.request.OfferDetailsProvider import OfferDetailsProvider
from module.service.request.OfferIdProvider import OfferIdProvider
from module.service.request.SellerDetailsProvider import SellerDetailsProvider
from module.utils import remove_none_items


class RequestProvider:

    def __init__(self, search_phrase: str) -> None:
        self.offer_id_provider: OfferIdProvider = OfferIdProvider(search_phrase)
        self.offer_details_provider: OfferDetailsProvider = OfferDetailsProvider()
        self.seller_details_provider: SellerDetailsProvider = SellerDetailsProvider()


    def get_offers(self) -> List[Offer]:
        return remove_none_items([
            self._prepare_offer(offer_id)
            for offer_id in self.offer_id_provider.get_offers_id()
        ])


    def _prepare_offer(self, offer_id: str) -> Optional[Offer]:
        try:
            offer_details = self.offer_details_provider.get_offer_details(offer_id)
            seller_details = self.seller_details_provider.get_seller_details(
                offer_details["seller"]["id"]
            )
            return self._map_json_to_offer(offer_details, seller_details)

        except KeyError:
            return None


    def _map_json_to_offer(self, offer_details: Dict[str, Any],
                           seller_details: Dict[str, Any]) -> Offer:
        # TODO
        return Offer(
            offer_details["id"],
            offer_details["title"],
            float(offer_details["price"]),
            offer_details["image_url"],
            bool(offer_details["has_return_option"]),
            int(offer_details["description_length"]),
            int(offer_details["reviews_number"]),
            float(offer_details["product_rating"]),
            int(offer_details["ratings_number"]),
            Seller(
                seller_details["id"]
            )
        )
