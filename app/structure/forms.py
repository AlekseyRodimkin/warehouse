from django import forms
from warehouse.models import Place, Stock, Zone


class StructureActionForm(forms.Form):
    """Форма на вкладке Создание / удаление структуры"""

    stock = forms.CharField(
        max_length=100,
        required=True,
        label="Склад",
        widget=forms.TextInput(attrs={"placeholder": "Склад", "class": "form-control"}),
    )
    zone = forms.CharField(
        max_length=100,
        required=False,
        label="Зона",
        widget=forms.TextInput(attrs={"placeholder": "Зона", "class": "form-control"}),
    )
    place = forms.CharField(
        max_length=100,
        required=False,
        label="Место",
        widget=forms.TextInput(attrs={"placeholder": "Место", "class": "form-control"}),
    )

    ACTION_CHOICES = [("create", "Создать"), ("delete", "Удалить")]
    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="Действие",
    )

    def clean(self):
        cleaned_data = super().clean()
        stock = cleaned_data.get("stock", "").strip().upper()
        zone = cleaned_data.get("zone", "").strip().upper()
        place = cleaned_data.get("place", "").strip().upper()
        action = cleaned_data.get("action")

        if not stock:
            raise forms.ValidationError("Укажите хотя бы склад")

        if place and zone and stock:
            level = "place"
        elif zone and stock:
            level = "zone"
        else:
            level = "stock"

        try:
            stock_obj = Stock.objects.get(title__iexact=stock)
        except Stock.DoesNotExist:
            if action == "delete":
                raise forms.ValidationError(f"Склад «{stock}» не найден")
            stock_obj = None

        zone_obj = None
        if level in ("zone", "place"):
            if stock_obj:
                try:
                    zone_obj = Zone.objects.get(stock=stock_obj, title__iexact=zone)
                except Zone.DoesNotExist:
                    if action == "delete":
                        raise forms.ValidationError(
                            f"Зона «{zone}» не найдена на складе «{stock}»"
                        )
                    zone_obj = None

        place_obj = None
        if level == "place":
            if zone_obj:
                try:
                    place_obj = Place.objects.get(zone=zone_obj, title__iexact=place)
                except Place.DoesNotExist:
                    if action == "delete":
                        raise forms.ValidationError(
                            f"Место «{place}» не найдено в зоне «{zone}» на складе «{stock}»"
                        )
                    place_obj = None

        if action == "delete":
            if level == "stock" and stock_obj.zones.exists():
                raise forms.ValidationError("Нельзя удалить склад — в нём есть зоны")
            if level == "zone" and zone_obj.places.exists():
                raise forms.ValidationError("Нельзя удалить зону — в ней есть места")
            if level == "place" and place_obj.place_items.exists():
                raise forms.ValidationError("Нельзя удалить место — на нём есть товары")

        cleaned_data["level"] = level
        cleaned_data["stock_obj"] = stock_obj
        cleaned_data["zone_obj"] = zone_obj
        cleaned_data["place_obj"] = place_obj

        return cleaned_data


class StructureSearchForm(forms.Form):
    """Форма на вкладке Поиск структуры"""

    stock = forms.ModelChoiceField(
        queryset=Stock.objects.all(), required=False, label="Склад"
    )
    zone = forms.CharField(
        max_length=100,
        required=False,
        label="Зона",
        widget=forms.TextInput(attrs={"placeholder": "Зона", "class": "form-control"}),
    )
    place = forms.CharField(
        max_length=100,
        required=False,
        label="Место",
        widget=forms.TextInput(attrs={"placeholder": "Место", "class": "form-control"}),
    )
