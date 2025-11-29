from django.contrib.auth.views import LoginView
from django.urls import path

from .views import (
    MainView,
    InventoryLotSearchView,
    InventoryItemSearchView,
    InventoryHistoryView,
    InventoryMoveView,
)

app_name = "warehouse"

urlpatterns = [
    path("", MainView.as_view(), name="main"),
    path("inventory/search/lot/", InventoryLotSearchView.as_view(), name="lot-inventory-search"),
    path("inventory/search/item/", InventoryItemSearchView.as_view(), name="item-inventory-search"),
    path("inventory/move/", InventoryMoveView.as_view(), name="inventory-move"),
    path("inventory/search/history/", InventoryHistoryView.as_view(), name="inventory-history"),
]
