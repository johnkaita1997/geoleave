# urls.py

from django.urls import path

from .views import LeavetypeListView, LeavetypeDetailView, LeavetypeCreateView

urlpatterns = [
    path('create', LeavetypeCreateView.as_view(), name="currency-create"),
    path('list', LeavetypeListView.as_view(), name="currency-list"),
    path('<str:pk>', LeavetypeDetailView.as_view(), name="currency-detail")
]
