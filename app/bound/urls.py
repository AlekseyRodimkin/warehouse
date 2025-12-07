from django.urls import path

from .views import InventoryInboundSearchView, download_inbound_docs

app_name = "bound"

urlpatterns = [
    path(
        "search/inbound/",
        InventoryInboundSearchView.as_view(),
        name="inbound-inventory-search",
    ),
    path("inbound/<int:pk>/docs/", download_inbound_docs, name="download_inbound_docs"),
]
