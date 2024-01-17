from django.db import models

from models import ParentModel


class Leavetype(ParentModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=19255, null=True,blank=True)
    is_full_time_employee = models.BooleanField(default=False)
    leave_duration_in_days = models.IntegerField(default=3, null=True, blank=True)
    length_of_service_months = models.IntegerField(default=3, null=True, blank=True)
    is_document_backed = models.BooleanField(default=False)
    is_satisfactory_performance_based = models.BooleanField(default=False)
    has_exhausted_normal_leave_days = models.BooleanField(default=False)
    duration_is_request_basis = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=True)
    is_compensatory = models.BooleanField(default=False)
    is_normal = models.BooleanField(default=False)
    days_in_advance = models.IntegerField(default=3, null=True, blank=True)


    def __str__(self):
        return self.name
