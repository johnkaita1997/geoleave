from django.db import models

from appuser.models import AppUser
from leave_types.models import Leavetype
from models import ParentModel


class Leaveapplication(ParentModel):
    appuser = models.ForeignKey(AppUser, default=None, null=True, on_delete=models.CASCADE, related_name="leave_applications")
    leave = models.ForeignKey(Leavetype, default=None, null=True, on_delete=models.CASCADE, related_name="leave_applications")
    duration_in_days = models.IntegerField(null=True, blank=True)

    expected_start_date = models.DateField(default="2020-12-12")
    expected_end_date = models.DateField(default="2020-12-12")

    is_cleared = models.BooleanField(default=False, blank=True, null=True)
    clearance_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    is_approved = models.BooleanField(default=False, blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)

    is_actedon = models.BooleanField(default=False, blank=True, null=True)
    approval_date = models.DateField(blank=True, null=True)
    approval_user = models.ForeignKey(AppUser, default=None, null=True, on_delete=models.CASCADE, related_name="leave_applications_approval")

    start_of_holiday_date = models.DateField(blank=True, null=True)
    end_of_holiday_date = models.DateField(blank=True, null=True)

    is_forwarded = models.BooleanField(default=False, blank=True, null=True)
    forwarded_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.appuser.first_name
