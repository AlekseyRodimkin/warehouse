import io
import os
import zipfile

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView

from app.settings import MEDIA_ROOT

from .forms import InboundSearchForm
from .models import Inbound


class InventoryInboundSearchView(LoginRequiredMixin, ListView):
    """
    Представление для поиска поставок

    Основная логика:
    - Добавляет форму InboundSearchForm в контекст шаблона и валидирует ей входные параметры
    - Выводит результат поиска.

    Шаблон:
        bound/inbound-inventory-search.html

    Поддерживаемые параметры поиска:
        stock          - фильтрация по складу
        status         - фильтрация по статусу
        inbound_number - частичное совпадение номера поставки
        supplier       - частичное совпадение поставщика
        planned_date   - фильтрация по >= плановой дате поставки
        actual_date    - фильтрация по <= фактической дате поставки

    Возвращает:
        QuerySet - отфильтрованный набор Inbound или пустой набор
                    при отсутствии параметров запроса.
    """

    model = Inbound
    template_name = "bound/inbound-inventory-search.html"
    context_object_name = "inbounds"
    paginate_by = 100
    ordering = ["-planned_date", "-created_at"]

    def get_queryset(self):
        qs = Inbound.objects.select_related("stock").exclude(status="draft")

        if not self.request.GET:
            return qs.none()

        form = InboundSearchForm(self.request.GET)
        if not form.is_valid():
            return qs.none()

        data = form.cleaned_data

        if data["stock"]:
            qs = qs.filter(stock=data["stock"])

        if data["inbound_number"]:
            qs = qs.filter(inbound_number__icontains=data["inbound_number"].strip())

        if data["supplier"]:
            qs = qs.filter(supplier__icontains=data["supplier"].strip())

        if data["status"]:
            qs = qs.filter(status=data["status"])

        if data["planned_date"]:
            qs = qs.filter(planned_date__gte=data["planned_date"])

        if data["actual_date"]:
            qs = qs.filter(actual_date__lte=data["actual_date"])

        qs = qs.order_by("-planned_date")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = InboundSearchForm(self.request.GET or None)
        context["total"] = self.get_queryset().count()
        return context


@login_required
def download_inbound_docs(request, pk) -> HttpResponse:
    """
    Функция для отдачи архива документов конкретной поставки

    Получает id поставки из url
    Находит поставку или отдает ошибку
    Находит папку по inbound_number или возвращает сообщение об отсутствии документов
    Формирует архив в памяти и отдает его
    """
    try:
        inbound = Inbound.objects.get(pk=pk)
    except Inbound.DoesNotExist:
        messages.error(request, "Поставка не найдена")
        return redirect(
            request.META.get("HTTP_REFERER", reverse("bound:inbound-inventory-search"))
        )

    inb_num = str(inbound.inbound_number)
    folder = os.path.join(MEDIA_ROOT, "inbounds", inb_num)

    if not os.path.isdir(folder):
        messages.warning(request, "Документы отсутствуют")
        return redirect(
            request.META.get("HTTP_REFERER", reverse("bound:inbound-inventory-search"))
        )

    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)

            if os.path.isfile(file_path):
                zip_file.write(file_path, arcname=filename)

    buffer.seek(0)

    response = HttpResponse(buffer.read(), content_type="application/zip")
    response["Content-Disposition"] = f'attachment; filename="{inb_num}.zip"'

    return response
