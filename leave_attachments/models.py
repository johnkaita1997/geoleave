from django.db import models
from django.db.models import DO_NOTHING

from file_upload.models import SchoolImage
from leave_applications.models import Leaveapplication
from models import ParentModel


# Create your models here.
class Leaveattachment(ParentModel):
    name = models.CharField(max_length=255)
    fileid = models.ForeignKey(SchoolImage, null=True, default=None, on_delete=DO_NOTHING, related_name="leaveattachments")
    leave_application = models.ForeignKey(Leaveapplication, null=True, default=None, on_delete=models.SET_NULL, related_name="leaveattachments")

    def __str__(self):
        return f"{self.id}"


