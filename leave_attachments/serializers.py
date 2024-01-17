from rest_framework import serializers

from leave_applications.models import Leaveapplication
from .models import Leaveattachment


class BasicLeaveattachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaveapplication
        fields = ['id']


class Leaveattachmentserializer(serializers.ModelSerializer):
    leave_application_details = BasicLeaveattachmentSerializer(source='leave_application', many=False, read_only=True)

    class Meta:
        model = Leaveattachment
        fields = '__all__'