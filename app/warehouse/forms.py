from django import forms
from .models import Stock, Zone, Place, Item

# Статусы продублированы от Models.PlaceItem.STATUS_CHOICES
STATUS_CHOICES = [
    ("ok", "ok"),
    ("blk", "blk"),
    ("no", "no"),
    ("new", "new"),
    ("dock", "dock"),
]


class PlaceItemSearchForm(forms.Form):
    """Форма поиска на вкладке LotInventorySearch"""
    stock = forms.ModelChoiceField(queryset=Stock.objects.all(), required=False)
    zone = forms.CharField(required=False)
    place = forms.CharField(required=False)
    item_code = forms.CharField(max_length=100, required=False)
    status = forms.ChoiceField(choices=[("", "---")] + STATUS_CHOICES, required=False)
    qty_min = forms.IntegerField(required=False, min_value=0)
    qty_max = forms.IntegerField(required=False, min_value=0)
