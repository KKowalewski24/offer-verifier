from typing import List

from module.model.Offer import Offer
from module.service.request.OfferDetailsProvider import OfferDetailsProvider
from module.service.request.OfferIdProvider import OfferIdProvider
from module.service.request.SellerProvider import SellerProvider


class RequestProvider:

    def __init__(self, search_phrase: str) -> None:
        self.offer_id_provider: OfferIdProvider = OfferIdProvider(search_phrase)
        self.offer_details_provider: OfferDetailsProvider = OfferDetailsProvider()
        self.seller_provider: SellerProvider = SellerProvider()


    def get_offers(self) -> List[Offer]:
        return []
    # TODO