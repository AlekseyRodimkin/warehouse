from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")


def base(request: HttpRequest) -> HttpResponse:
    return render(request, "accounts/base.html")


class AppLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")
