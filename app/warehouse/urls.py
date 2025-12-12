from django.contrib.auth.views import LoginView
from django.urls import path

from .views import (InventoryHistoryView, InventoryItemSearchView,
                    InventoryLotSearchView, InventoryMoveView, MainView)

app_name = "warehouse"

urlpatterns = [
    path("", MainView.as_view(), name="main"),
    path(
        "inventory/search/lot/",
        InventoryLotSearchView.as_view(),
        name="lot-search",
    ),
    path(
        "inventory/search/item/",
        InventoryItemSearchView.as_view(),
        name="item-search",
    ),
    path("inventory/move/", InventoryMoveView.as_view(), name="inventory-move"),
    path(
        "inventory/search/history/",
        InventoryHistoryView.as_view(),
        name="history-search",
    ),
]
