from django.db import transaction
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .models import PlaceItem, Item, History
from .forms import PlaceItemSearchForm, ItemSearchForm, HistorySearchForm, MoveItemForm


def main(request: HttpRequest) -> HttpResponse:
    """Функция главной страницы"""
    return render(request, "warehouse/main.html")


class InventoryLotSearchView(LoginRequiredMixin, ListView):
    """
        Представление для поиска партий товаров на складе.

        Основная логика:
        - Добавляет форму PlaceItemSearchForm в контекст шаблона и валидирует ей входные параметры
        - Выводит результаты постранично (100 элементов на страницу).

        Шаблон:
            warehouse/lot-inventory-search.html

        Поддерживаемые параметры поиска:
            stock      - фильтрация по складу
            zone       - частичное совпадение названия зоны
            place      - частичное совпадение названия места хранения
            item_code  - частичное совпадение кода товара
            status     - точное совпадение статуса
            qty_min    - минимальное количество
            qty_max    - максимальное количество

        Возвращает:
            QuerySet - отфильтрованный набор PlaceItem или пустой набор
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


class InventoryItemSearchView(LoginRequiredMixin, ListView):
    """
        Представление для поиска товаров на складе.

        Основная логика:
        - Добавляет форму PlaceItemSearchForm в контекст шаблона и валидирует ей входные параметры
        - Выводит результаты постранично (100 элементов на страницу).

        Шаблон:
            warehouse/item-inventory-search.html

        Поддерживаемые параметры поиска:
            stock      - фильтрация по складу
            zone       - частичное совпадение названия зоны
            place      - частичное совпадение названия места хранения
            item_code  - частичное совпадение кода товара
            status     - точное совпадение статуса
            weight_min - минимальный вес
            weight_max - максимальный вес

        Возвращает:
            QuerySet - отфильтрованный набор PlaceItem или пустой набор
                        при отсутствии параметров запроса.
        """
    model = PlaceItem
    template_name = "warehouse/item-inventory-search.html"
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
            if data.get("weight_min") is not None:
                qs = qs.filter(item__weight__gte=data["weight_min"])
            if data.get("weight_max") is not None:
                qs = qs.filter(item__weight__lte=data["weight_max"])
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ItemSearchForm(self.request.GET)
        return context


class InventoryHistoryView(LoginRequiredMixin, ListView):
    """
        Представление для поиска истории перемещения.

        Основная логика:
        - Добавляет форму HistorySearchForm в контекст шаблона и валидирует ей входные параметры
        - Выводит результаты постранично (100 элементов на страницу).

        Шаблон:
            warehouse/inventory-history.html

        Поддерживаемые параметры поиска:
            stock      - фильтрация по складу
            zone       - частичное совпадение названия зоны
            place      - частичное совпадение названия места хранения
            item_code  - частичное совпадение кода товара
            date       - дата
            работник   - частичное совпадение username / first_name / last_name

        Возвращает:
            QuerySet - отфильтрованный набор History или пустой набор
                        при отсутствии параметров запроса.
        """
    model = History
    template_name = "warehouse/inventory-history.html"
    context_object_name = "histories"
    paginate_by = 100

    def get_queryset(self):
        qs = History.objects.select_related(
            "item", "user",
            "old_place__zone__stock",
            "new_place__zone__stock"
        ).order_by("-date")

        # Если нет GET-параметров - показываем пусто
        if not self.request.GET:
            return qs.none()

        form = HistorySearchForm(self.request.GET)
        if not form.is_valid():
            return qs.none()

        data = form.cleaned_data

        # Поиск по складу (через old_place или new_place)
        if data["stock"]:
            stock_id = data["stock"].id
            qs = qs.filter(
                Q(old_place__zone__stock_id=stock_id) |
                Q(new_place__zone__stock_id=stock_id)
            )

        # Поиск по зоне (по названию)
        if data["zone"]:
            qs = qs.filter(
                Q(old_place__zone__title__icontains=data["zone"]) |
                Q(new_place__zone__title__icontains=data["zone"])
            )

        # Поиск по месту (по названию)
        if data["place"]:
            qs = qs.filter(
                Q(old_place__title__icontains=data["place"]) |
                Q(new_place__title__icontains=data["place"])
            )

        # По коду товара
        if data["item_code"]:
            qs = qs.filter(item__item_code__icontains=data["item_code"])

        # По пользователю
        if data["user"]:
            qs = qs.filter(
                Q(user__username__icontains=data["user"]) |
                Q(user__first_name__icontains=data["user"]) |
                Q(user__last_name__icontains=data["user"])
            )

        # По дате
        if data["date_from"]:
            qs = qs.filter(date__date__gte=data["date_from"])
        if data["date_to"]:
            qs = qs.filter(date__date__lte=data["date_to"])

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = HistorySearchForm(self.request.GET or None)
        context["total"] = self.get_queryset().count()
        return context


class InventoryMoveView(LoginRequiredMixin, View):
    """
        Представление для перемещения товара.

        Основная логика:
        - Добавляет форму MoveItemForm в контекст шаблона и валидирует ей входные параметры
        - Выводит результат о совершении перемещения (сообщение).

        Шаблон:
            warehouse/inventory-move.html

        Поддерживаемые параметры поиска:
            item_code    - частичное совпадение кода товара
            full_address - полный адрес (Склад/Зона/Место)
            stock        - фильтрация по складу
            zone         - частичное совпадение названия зоны
            place        - частичное совпадение названия места хранения

        Возвращает:
            Перенаправление на страницу перемещения
        """
    template_name = "warehouse/inventory-move.html"

    def get(self, request):
        form = MoveItemForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = MoveItemForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                place_item = form.cleaned_data["place_item"]
                to_place = form.cleaned_data["to_place"]
                item = form.cleaned_data["item"]
                quantity = form.cleaned_data["quantity"]

                if place_item.quantity <= quantity:
                    place_item.delete()
                else:
                    place_item.quantity -= quantity
                    place_item.save()

                to_pi, created = PlaceItem.objects.get_or_create(
                    place=to_place,
                    item=item,
                    defaults={"quantity": quantity, "STATUS": "ok"}
                )
                if not created:
                    to_pi.quantity += quantity
                    to_pi.STATUS = "ok"
                to_pi.save()

                History.objects.create(
                    user=request.user,
                    item=item,
                    old_place=place_item.place,
                    new_place=to_place,
                    count=quantity,
                )
                messages.success(request, "Товар успешно перемещён")
                return redirect("warehouse:inventory-move")

        return render(request, self.template_name, {"form": form})
