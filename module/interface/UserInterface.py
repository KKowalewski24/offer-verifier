import sys
from typing import List, Tuple

from module.constants import CURRENCY_US_DOLLAR, RESULTS_DIRECTORY, STATISTICS_PATH
from module.exception.VerificationImpossibleException import VerificationImpossibleException
from module.model.Offer import Offer
from module.model.Statistics import Statistics
from module.service.LatexGenerator import LatexGenerator
from module.service.Logger import Logger
from module.service.OfferVerifier import OfferVerifier
from module.service.PdfGenerator import PdfGenerator
from module.utils import has_access_to_internet, save_to_file


class UserInterface:

    def __init__(self, search_phrase: str, save_offers: bool,
                 generate_pdf: bool, generate_statistics: bool) -> None:
        self.search_phrase: str = search_phrase
        self.generate_pdf: bool = generate_pdf
        self.generate_statistics = generate_statistics
        self.offer_verifier: OfferVerifier = OfferVerifier(search_phrase, save_offers)
        self.pdf_generator: PdfGenerator = PdfGenerator()
        self.latex_generator: LatexGenerator = LatexGenerator(RESULTS_DIRECTORY)
        self.logger: Logger = Logger()

        if not has_access_to_internet():
            print("No access to the Internet, program cannot be run")
            self.logger.error("No access to the Internet, program cannot be run")
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

            if self.generate_statistics:
                self._display_statistics(statistics)

        except VerificationImpossibleException:
            print(
                "Program cannot decide whether offers are credible or not - both clusters "
                "have the same number of super sellers"
            )
            self.logger.error(
                "Program cannot decide whether offers are credible or not - both clusters "
                "have the same number of super sellers"
            )
            sys.exit()


    def _display_offers(self, combined_offers: Tuple[List[Offer], bool]) -> None:
        offers, is_verified = combined_offers
        for offer in offers:
            self._display_offer_details(offer, is_verified)


    def _display_offer_details(self, offer: Offer, is_verified: bool) -> None:
        # TODO
        print("\nOffer details: ")
        print("\tOffer ID:", offer.id)
        print("\tOffer title:", offer.title)
        print("\tOffer price:", CURRENCY_US_DOLLAR, offer.price)
        print("\tImage URL:", offer.image_url)
        print("\tOption to return item:", offer.has_return_option)
        print("\tNumber of reviews:", offer.reviews_number)
        print("\tRatings of product:", offer.product_rating)
        print("\tNumber of ratings:", offer.ratings_number)
        # print("\tInformation about seller")
        # print("\t\tSeller ID:", offer.seller.id)
        # print("\t\tSeller login:", offer.seller.login)
        # print(
        #     "\t\tIs it 'Super Seller':",
        #     convert_bool_to_string(offer.seller.is_super_seller)
        # )
        # print("\t\tMean rates: ", offer.seller.mean_rates)
        # print("\t\tNumber of recommendations: ", offer.seller.recommendation_number)
        # print("\t\tNumber of negative feedback: ", offer.seller.not_recommendation_number)
        # print("\t\tRecommendations percentage: ", offer.seller.recommendation_percentage)
        # print(
        #     "\n\tIs the offer verified as credible:",
        #     convert_bool_to_string(is_verified)
        # )

        pass


    def _display_statistics(self, statistics: Statistics) -> None:
        print("Silhouette score:", statistics.silhouette_score)
        print("Calinski Harabasz score:", statistics.calinski_harabasz_score)
        print("Davies Bouldin score:", statistics.davies_bouldin_score)
        latex_table_row: str = self.latex_generator.get_table_body(
            [[self.search_phrase] + statistics.to_list()]
        )
        print(latex_table_row)
        save_to_file(STATISTICS_PATH, latex_table_row, "a")
