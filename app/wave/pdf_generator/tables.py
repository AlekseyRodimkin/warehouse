from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle


def products_table(data):
    table = Table(
        data,
        colWidths=[160, 60, 60, 60, 160],
        repeatRows=1,  # заголовок повторяется на каждой странице
    )

    table.setStyle(TableStyle([
        # Общий шрифт
        ("FONT", (0, 0), (-1, -1), "OpenSans"),

        # Жирный шрифт для заголовка
        ("FONT", (0, 0), (-1, 0), "OpenSans-Bold"),

        # Сетка
        ("GRID", (0, 0), (-1, -1), 0.6, colors.black),

        # Выравнивание по центру колонок 2 - 4
        ("ALIGN", (1, 0), (3, -1), "CENTER"),

        # Вертикальное выравнивание
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        # Отступы
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))

    return table
