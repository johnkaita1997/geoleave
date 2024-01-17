from rest_framework import serializers

from .models import Leavetype


class LeavetypeSerializer(serializers.ModelSerializer):
    attachments_values = serializers.ListField(child=serializers.DictField(), allow_null=True, required=False, write_only=True)
    attachments_items = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Leavetype
        fields = '__all__'


    def get_attachments_items(self, obj):
        from leave_attachments.serializers import Leaveattachmentserializer
        try:
            attachments_items = obj.leaveattachments.all()
        except AttributeError as exception:
            print(f"Found error {exception}")
            attachments_items = []
        return Leaveattachmentserializer(attachments_items, many=True).data