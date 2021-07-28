from typing import List, Tuple

from fpdf import FPDF

from module.constants import CURRENCY_US_DOLLAR, PDF_EXTENSION
from module.model.Offer import Offer
from module.utils import get_filename


class PDF(FPDF):

    def lines(self):
        self.set_line_width(0.0)
        self.line(5.0, 5.0, 205.0, 5.0)
        self.line(5.0, 292.0, 205.0, 292.0)
        self.line(5.0, 5.0, 5.0, 292.0)
        self.line(205.0, 5.0, 205.0, 292.0)


class PdfGenerator:

    def __init__(self) -> None:
        self.pdf = PDF()


    def generate(
            self, combined_offers: Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]]
    ) -> None:
        self._generate_single_report(combined_offers[0])
        self._generate_single_report(combined_offers[1])


    def _generate_single_report(self, combined_offers: Tuple[List[Offer], bool]) -> None:
        offers, is_verified = combined_offers
        for offer in offers:
            self._draw_single_offer(offer, is_verified)

        self.pdf.output(get_filename(
            "credible_offer_report" if is_verified else "not_credible_offer_report", PDF_EXTENSION
        ), "F")


    def _draw_single_offer(self, offer: Offer, is_verified: bool) -> None:
        self.pdf.add_page()
        self.pdf.lines()
        self.pdf.set_font("Arial", "B", 16)
        self._draw_cell("Offer details", "C")

        self._draw_cell("Offer ID: " + str(offer.id))
        self._draw_cell("Offer title: " + offer.title)
        self._draw_cell("Offer price: " + CURRENCY_US_DOLLAR + " " + offer.price)
        self._draw_cell("Image URL - Click here", link=offer.image_url)
        self._draw_cell("Option to return item: " + offer.has_return_option)
        self._draw_cell("Number of reviews: " + offer.product_reviews_number)
        self._draw_cell("Ratings of product: " + offer.product_rating)
        self._draw_cell("Number of ratings: " + offer.product_ratings_number)

        # TODO
        # self._draw_cell("", "C")
        # self._draw_cell("Information about seller", "C")
        # self._draw_cell("Seller ID: " + str(offer.seller.id))
        # self._draw_cell("Seller login: " + offer.seller.login)
        # self._draw_cell(
        #     "Is it 'Super Seller': " + convert_bool_to_string(offer.seller.is_super_seller)
        # )
        # self._draw_cell("Mean rates: " + str(offer.seller.mean_rates))
        # self._draw_cell("Number of recommendations: " + str(offer.seller.recommendation_number))
        # self._draw_cell(
        #     "Number of negative feedback: " + str(offer.seller.not_recommendation_number)
        # )
        # self._draw_cell(
        #     "Recommendations percentage: " + str(offer.seller.recommendation_percentage)
        # )
        # self._draw_cell(
        #     "Is the offer verified as credible: " + convert_bool_to_string(is_verified)
        # )


    def _draw_cell(self, text: str, align: str = "", link: str = "") -> None:
        self.pdf.cell(w=0, h=10, txt=text, align=align, border=0, ln=1, link=link)
