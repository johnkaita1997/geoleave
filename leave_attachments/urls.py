# urls.py

from django.urls import path

from .views import LeaveattachmentListView, LeaveattachmentDetailView, LeaveattachmentCreateView

urlpatterns = [
    path('create', LeaveattachmentCreateView.as_view(), name="Leaveattachment-create"),
    path('list', LeaveattachmentListView.as_view(), name="Leaveattachment-list"),
    path('<str:pk>', LeaveattachmentDetailView.as_view(), name="Leaveattachment-detail")
]
