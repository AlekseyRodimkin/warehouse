from django.urls import path

from .views import (InboundCreateView, InboundSearchView,
                    download_inbound_docs, download_inbound_form)

app_name = "bound"

urlpatterns = [
    path(
        "search/inbound/",
        InboundSearchView.as_view(),
        name="inbound-search",
    ),
    path(
        "inbound/create/",
        InboundCreateView.as_view(),
        name="inbound-create",
    ),
    path("inbound/<int:pk>/docs/", download_inbound_docs, name="download_inbound_docs"),
    path("inbound/form/", download_inbound_form, name="download_inbound_form"),
]
