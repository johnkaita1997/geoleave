# urls.py

from django.urls import path

from .views import DepartmentListView, DepartmentDetailView, DepartmentCreateView

urlpatterns = [
    path('create', DepartmentCreateView.as_view(), name="department-create"),
    path('list', DepartmentListView.as_view(), name="department-list"),
    path('<str:pk>', DepartmentDetailView.as_view(), name="department-detail")
]
