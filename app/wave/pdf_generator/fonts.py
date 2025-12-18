import os

from django.conf import settings
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONTS_DIR = os.path.dirname(os.path.abspath(__file__))


def register_fonts():
    regular_path = os.path.join(FONTS_DIR, "OpenSans-Regular.ttf")
    bold_path = os.path.join(FONTS_DIR, "OpenSans-Bold.ttf")

    if not os.path.exists(regular_path):
        raise FileNotFoundError(f"Шрифт не найден: {regular_path}")
    if not os.path.exists(bold_path):
        raise FileNotFoundError(f"Шрифт не найден: {bold_path}")

    pdfmetrics.registerFont(TTFont("OpenSans", regular_path))
    pdfmetrics.registerFont(TTFont("OpenSans-Bold", bold_path))
