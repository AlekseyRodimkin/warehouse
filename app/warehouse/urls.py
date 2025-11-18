from django.contrib.auth.views import LoginView
from django.urls import path

from .views import main, InventoryLotSearchView

app_name = "warehouse"

urlpatterns = [
    path("", main, name="main"),
    path("inventory/lot/search/", InventoryLotSearchView.as_view(), name="lot-inventory-search"),
    # path("inventory/item/search/", InventoryItemSearchView.as_view(), name="lot-inventory-search"),
]
