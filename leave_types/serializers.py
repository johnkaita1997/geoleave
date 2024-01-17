from rest_framework import serializers

from .models import Leavetype


class LeavetypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leavetype
        fields = '__all__'
