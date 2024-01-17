from django.db import models
from django.db.models import DO_NOTHING

from appuser.models import AppUser
from models import ParentModel
from utils import file_upload


class SchoolImage(ParentModel):
    creator = models.ForeignKey(AppUser, on_delete=DO_NOTHING, related_name="innovation_document_creator")
    document = models.FileField(upload_to=file_upload, null=True, blank=True)
    original_file_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, default = "Ttitle", blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    school_id = models.UUIDField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.title)
