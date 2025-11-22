from django.contrib.auth.views import LoginView
from django.urls import path

from .views import main, InventoryLotSearchView, InventoryItemSearchView, InventoryHistoryView, InventoryMoveView

app_name = "warehouse"

urlpatterns = [
    path("", main, name="main"),
    path("inventory/lot/search/", InventoryLotSearchView.as_view(), name="lot-inventory-search"),
    path("inventory/item/search/", InventoryItemSearchView.as_view(), name="item-inventory-search"),
    path("inventory/move/", InventoryMoveView.as_view(), name="inventory-move"),
    path("inventory/history/", InventoryHistoryView.as_view(), name="inventory-history"),
    # path("wave/search/", InventoryWaveSearcgView.as_view(), name="wave-inventory-search"),
    # path("inbound/", InboundView.as_view(), name="inbound"),
    # path("outbound/", OutboundView.as_view(), name="outbound"),
]
