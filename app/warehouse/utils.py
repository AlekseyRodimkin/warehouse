def format_address(place_item):
    """Генерация полного адреса"""
    if not place_item or not place_item.place:
        return None

    place = place_item.place
    zone = place.zone
    stock = zone.stock

    return f"{stock.title}/{zone.title}/{place.title}"
