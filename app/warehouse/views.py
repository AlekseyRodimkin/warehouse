from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import PlaceItem
from .forms import PlaceItemSearchForm


def main(request: HttpRequest) -> HttpResponse:
    """Функция главной страницы"""
    return render(request, "warehouse/main.html")


class InventoryLotSearchView(LoginRequiredMixin, ListView):
    """
        Представление для поиска партий товаров (PlaceItem) на складе.

        Основная логика:
        - Добавляет форму PlaceItemSearchForm в контекст шаблона и валидирует ей входные параметры
        - Выводит результаты постранично (100 элементов на страницу).

        Шаблон:
            warehouse/lot-inventory-search.html

        Поддерживаемые параметры поиска:
            stock      — фильтрация по складу (Stock)
            zone       — частичное совпадение названия зоны
            place      — частичное совпадение названия места хранения
            item_code  — частичное совпадение кода товара
            status     — точное совпадение статуса (STATUS)
            qty_min    — минимальное количество (quantity >= value)
            qty_max    — максимальное количество (quantity <= value)

        Возвращает:
            QuerySet — отфильтрованный набор PlaceItem или пустой набор
                        при отсутствии параметров запроса.
        """
    model = PlaceItem
    template_name = "warehouse/lot-inventory-search.html"
    context_object_name = "place_items"
    paginate_by = 100

    def get_queryset(self):
        qs = super().get_queryset().select_related('item', 'place', 'place__zone', 'place__zone__stock')
        form = PlaceItemSearchForm(self.request.GET)

        if not self.request.GET:
            return qs.none()

        if form.is_valid():
            data = form.cleaned_data
            if data.get("stock"):
                qs = qs.filter(place__zone__stock=data["stock"])
            if data.get("zone"):
                qs = qs.filter(place__zone__title__icontains=data["zone"])
            if data.get("place"):
                qs = qs.filter(place__title__icontains=data["place"])
            if data.get("item_code"):
                qs = qs.filter(item__item_code__icontains=data["item_code"])
            if data.get("status"):
                qs = qs.filter(STATUS=data["status"])
            if data.get("qty_min") is not None:
                qs = qs.filter(quantity__gte=data["qty_min"])
            if data.get("qty_max") is not None:
                qs = qs.filter(quantity__lte=data["qty_max"])
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PlaceItemSearchForm(self.request.GET)
        return context
