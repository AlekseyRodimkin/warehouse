from django.urls import path

from .views import StructureManagerView, StructureSearchView

app_name = "structure"

urlpatterns = [
    path(
        "manager/structure/", StructureManagerView.as_view(), name="structure-manager"
    ),
    path("search/structure/", StructureSearchView.as_view(), name="structure-search"),
]
