from typing import Any, Dict, List, Optional

from tqdm import tqdm

from module.model.Offer import Offer
from module.model.Seller import Seller
from module.service.Logger import Logger
from module.service.request.OfferDetailsProvider import OfferDetailsProvider
from module.service.request.OfferIdProvider import OfferIdProvider
from module.service.request.SellerDetailsProvider import SellerDetailsProvider
from module.utils import print_and_log, remove_none_items


class RequestProvider:

    def __init__(self, search_phrase: str) -> None:
        self.offer_id_provider: OfferIdProvider = OfferIdProvider(search_phrase)
        self.offer_details_provider: OfferDetailsProvider = OfferDetailsProvider()
        self.seller_details_provider: SellerDetailsProvider = SellerDetailsProvider()
        self.logger = Logger().get_logging_instance()


    def get_offers(self) -> List[Offer]:
        offers_id: List[str] = self.offer_id_provider.get_offers_id()
        print_and_log(self.logger, "Offers to download: " + str(len(offers_id)))
        return remove_none_items([self._prepare_offer(offer_id) for offer_id in tqdm(offers_id)])


    def _prepare_offer(self, offer_id: str) -> Optional[Offer]:
        self.logger.info("Preparing offer id: " + offer_id)
        try:
            offer_details = self.offer_details_provider.get_offer_details(offer_id)
            seller_details = self.seller_details_provider.get_seller_details(
                offer_details["seller"]["id"]
            )
            return self._map_json_to_offer(offer_details, seller_details)

        except KeyError as e:
            self.logger.error("KeyError " + str(e) + " offer_id: " + offer_id)
            return None


    def _map_json_to_offer(self, offer_details: Dict[str, Any],
                           seller_details: Dict[str, Any]) -> Offer:
        return Offer(
            offer_details["id"],
            offer_details["title"],
            float(offer_details["price"]),
            offer_details["image_url"],
            bool(offer_details["has_return_option"]),
            int(offer_details["description_length"]),
            int(offer_details["product_reviews_number"]),
            float(offer_details["product_rating"]),
            int(offer_details["product_ratings_number"]),
            Seller(
                seller_details["id"],
                float(seller_details["seller_feedback_score"]),
                float(seller_details["seller_feedback_percentage"]),
                int(seller_details["year_of_joining"]),
                int(seller_details["seller_positive_ratings_number"]),
                int(seller_details["seller_neutral_ratings_number"]),
                int(seller_details["seller_negative_ratings_number"]),
                float(seller_details["accurate_description"]),
                float(seller_details["reasonable_shipping_cost"]),
                float(seller_details["shipping_speed"]),
                float(seller_details["communication"]),
            )
        )
