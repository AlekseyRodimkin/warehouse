from django.urls import path
from .views import StructureManagerView, StructureSearchView

app_name = 'structure'

urlpatterns = [
    path('structure/manager/', StructureManagerView.as_view(), name='structure-manager'),
    path('structure/search/', StructureSearchView.as_view(), name='structure-search'),
]
