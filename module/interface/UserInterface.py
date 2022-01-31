import sys
from typing import List, Tuple

from module.constants import CURRENCY_US_DOLLAR
from module.exception.ChoosingCredibleOfferNotPossibleException import \
    ChoosingCredibleOfferNotPossibleException
from module.exception.EmptyDatasetException import EmptyDatasetException
from module.model.Offer import Offer
from module.service.Logger import Logger
from module.service.OfferVerifier import OfferVerifier
from module.service.PdfGenerator import PdfGenerator
from module.utils import convert_bool_to_string, display_and_log_error, has_access_to_internet


class UserInterface:

    def __init__(self, search_phrase: str, generate_pdf: bool) -> None:
        self.generate_pdf: bool = generate_pdf
        self.offer_verifier: OfferVerifier = OfferVerifier(search_phrase=search_phrase)
        self.pdf_generator: PdfGenerator = PdfGenerator()
        self.logger = Logger().get_logging_instance()

        if not has_access_to_internet():
            display_and_log_error(self.logger, "No access to the Internet, program cannot be run")
            sys.exit()
        print()


    def display_result(self) -> None:
        try:
            combined_offers, statistics = self.offer_verifier.verify()
            print("------------------------------------------------------------------------")
            self._display_offers(combined_offers[0])
            print("------------------------------------------------------------------------")
            self._display_offers(combined_offers[1])

            if self.generate_pdf:
                self.pdf_generator.generate(combined_offers)

        except ChoosingCredibleOfferNotPossibleException:
            display_and_log_error(
                self.logger,
                "Program cannot decide whether offers are credible or not - both clusters "
                "have the same number of super sellers"
            )
            sys.exit()

        except EmptyDatasetException:
            display_and_log_error(self.logger, "Dataset cannot be empty!")
            sys.exit()


    def _display_offers(self, combined_offers: Tuple[List[Offer], bool]) -> None:
        offers, is_verified = combined_offers
        for offer in offers:
            self._display_offer_details(offer, is_verified)


    def _display_offer_details(self, offer: Offer, is_verified: bool) -> None:
        print("\nOffer details: ")
        print("\tOffer ID:", offer.id)
        print("\tOffer title:", offer.title)
        print("\tOffer price:", CURRENCY_US_DOLLAR, offer.price)
        print("\tImage URL:", offer.image_url)
        print("\tOption to return item:", offer.has_return_option)
        print("\tNumber of reviews:", offer.product_reviews_number)
        print("\tRatings of product:", offer.product_rating)
        print("\tNumber of ratings:", offer.product_ratings_number)

        print("\tInformation about seller")
        print("\t\tSeller ID:", offer.seller.id)
        print("\t\tSeller feedback score:", offer.seller.feedback_score)
        print("\t\tSeller feedback percentage:", offer.seller.seller_feedback_percentage)
        print("\t\tSeller year of joining:", offer.seller.year_of_joining)
        print("\t\tSeller positive ratings number:", offer.seller.seller_positive_ratings_number)
        print("\t\tSeller neutral ratings number:", offer.seller.seller_neutral_ratings_number)
        print("\t\tSeller negative ratings number:", offer.seller.seller_negative_ratings_number)
        print("\t\tSeller accurate description:", offer.seller.accurate_description)
        print("\t\tSeller reasonable shipping cost:", offer.seller.reasonable_shipping_cost)
        print("\t\tSeller shipping speed:", offer.seller.shipping_speed)
        print("\t\tSeller communication:", offer.seller.communication)

        print(
            "\n\tIs the offer verified as credible:",
            convert_bool_to_string(is_verified)
        )
