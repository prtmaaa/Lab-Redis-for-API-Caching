from django.urls import path
from .views import *

urlpatterns = [
    path('get-institution-trade', InstitutionsView.as_view(), name='get-institution-trade'),
    path('get-subsector-reports', ReportsView.as_view(), name='get-subsector-reports'),
    path('get-metadata', MetadataView.as_view(), name='get-metadata'),
]
