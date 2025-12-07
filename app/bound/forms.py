from django import forms
from warehouse.models import Stock

# Статусы продублированы от Models.Inbound.INBOUND_STATUS_CHOICES
INBOUND_STATUS_CHOICES = [
    ("planned", "Запланирован"),
    ("in_progress", "В процессе"),
    ("completed", "Завершен"),
    ("cancelled", "Отменен"),
]


class InboundSearchForm(forms.Form):
    """Форма на вкладке Поиск прихода"""

    stock = forms.ModelChoiceField(
        queryset=Stock.objects.all(), required=False, label="Склад"
    )
    status = forms.ChoiceField(
        choices=[("", "---")] + INBOUND_STATUS_CHOICES, required=False, label="Статус"
    )

    inbound_number = forms.CharField(
        max_length=50,
        required=False,
        label="Номер поставки",
        widget=forms.TextInput(attrs={"placeholder": "INB-..."}),
    )

    supplier = forms.CharField(
        max_length=200,
        required=False,
        label="Поставщик",
        widget=forms.TextInput(attrs={"placeholder": "ИП..."}),
    )

    planned_date = forms.DateField(
        required=False,
        label="Планируемая дата",
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    actual_date = forms.DateField(
        required=False,
        label="Фактическая дата",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
