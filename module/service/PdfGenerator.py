from typing import List, Tuple

from fpdf import FPDF

from module.constants import CURRENCY_US_DOLLAR, OFFER_REPORT_FILENAME, PDF_EXTENSION, \
    PDF_MAX_LINE_LENGTH, RESULTS_DIRECTORY
from module.model.Offer import Offer
from module.utils import break_string, convert_bool_to_string, get_filename, \
    replace_unsupported_characters


class PdfGenerator:

    def generate(self, combined_offers: Tuple[Tuple[List[Offer], bool], Tuple[List[Offer], bool]]) -> None:
        PdfDocument().generate_single_report(combined_offers[0])
        PdfDocument().generate_single_report(combined_offers[1])


class PDF(FPDF):

    def lines(self):
        self.set_line_width(0.0)
        self.line(5.0, 5.0, 205.0, 5.0)
        self.line(5.0, 292.0, 205.0, 292.0)
        self.line(5.0, 5.0, 5.0, 292.0)
        self.line(205.0, 5.0, 205.0, 292.0)


class PdfDocument:

    def __init__(self) -> None:
        self.pdf = PDF()


    def generate_single_report(self, combined_offers: Tuple[List[Offer], bool]) -> None:
        offers, is_verified = combined_offers
        for offer in offers:
            self._draw_single_offer(offer, is_verified)

        filename: str = OFFER_REPORT_FILENAME[0] if is_verified else OFFER_REPORT_FILENAME[1]
        self.pdf.output(get_filename(RESULTS_DIRECTORY + filename, PDF_EXTENSION), "F")


    def _draw_single_offer(self, offer: Offer, is_verified: bool) -> None:
        self.pdf.add_page()
        self.pdf.lines()
        self.pdf.set_font("Arial", "B", 16)
        self._draw_cell("Offer details", "C")

        self.pdf.set_font("Arial", "B", 12)
        self._draw_cell("Offer ID: " + str(offer.id))
        self._draw_cell("Offer title: " + offer.title)
        self._draw_cell("Offer price: " + CURRENCY_US_DOLLAR + " " + str(offer.price))
        self._draw_cell("Image URL - Click here", link=offer.image_url)
        self._draw_cell("Option to return item: " + convert_bool_to_string(offer.has_return_option))
        self._draw_cell("Number of reviews: " + str(offer.product_reviews_number))
        self._draw_cell("Ratings of product: " + str(offer.product_rating))
        self._draw_cell("Number of ratings: " + str(offer.product_ratings_number))

        self._draw_cell("", "C")
        self._draw_cell("Information about seller", "C")
        self._draw_cell("Seller ID: " + str(offer.seller.id))
        self._draw_cell("Seller feedback score: " + str(offer.seller.feedback_score))
        self._draw_cell("Seller feedback percentage: " + str(offer.seller.seller_feedback_percentage))
        self._draw_cell("Seller year of joining: " + str(offer.seller.year_of_joining))
        self._draw_cell(
            "Seller positive ratings number: " + str(offer.seller.seller_positive_ratings_number)
        )
        self._draw_cell(
            "Seller neutral ratings number: " + str(offer.seller.seller_neutral_ratings_number)
        )
        self._draw_cell(
            "Seller negative ratings number: " + str(offer.seller.seller_negative_ratings_number)
        )
        self._draw_cell("Seller accurate description: " + str(offer.seller.accurate_description))
        self._draw_cell(
            "Seller reasonable shipping cost: " + str(offer.seller.reasonable_shipping_cost)
        )
        self._draw_cell("Seller shipping speed: " + str(offer.seller.shipping_speed))
        self._draw_cell("Seller communication: " + str(offer.seller.communication))

        self._draw_cell(
            "Is the offer verified as credible: " + convert_bool_to_string(is_verified)
        )


    def _draw_cell(self, text: str, align: str = "", link: str = "") -> None:
        for string in break_string(replace_unsupported_characters(text), PDF_MAX_LINE_LENGTH):
            self.pdf.cell(w=0, h=10, txt=string, align=align, border=0, ln=1, link=link)
