from django.contrib.auth.views import LoginView
from django.urls import path

from .views import main

app_name = "warehouse"

urlpatterns = [
    path("", main, name="main"),
    # path("inventory/", InventoryView.as_view(), name="inventory"),
]
