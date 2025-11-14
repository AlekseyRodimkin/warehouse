from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy


def main(request: HttpRequest) -> HttpResponse:
    return render(request, "warehouse/main.html")

# def inventory:
#     return render(request, "warehouse/main.html")
