from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle

BASE = ParagraphStyle(
    name="Base",
    fontName="OpenSans",
    fontSize=10,
    leading=12,
)

TITLE_BOLD = ParagraphStyle(
    name="TitleBold",
    fontName="OpenSans-Bold",
    fontSize=16,
    leading=18,
    alignment=TA_CENTER,
)
