from datetime import timedelta

from django import forms
from django.db import models
from django.forms import PasswordInput
from django.utils import timezone

from appuser.models import AppUser
from departments.models import Department
from file_upload.models import SchoolImage
from leave_applications.models import Leaveapplication
from leave_types.models import Leavetype
from models import ParentModel



class UppercaseInput(forms.TextInput):
    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)
        return value.upper() if value else value




def calculate_duration_excluding_weekends_and_holidays(start_date, end_date):
    duration = (end_date - start_date).days + 1
    weekend_days = 0
    holiday_dates = set(Holiday.objects.all().values_list('date', flat=True))

    for single_date in (start_date + timedelta(n) for n in range(duration)):
        if single_date.weekday() in [5, 6] or single_date in holiday_dates:
            weekend_days += 1

    duration_excluding_weekends_and_holidays = duration - weekend_days

    return duration_excluding_weekends_and_holidays



class FileUploadWeb(forms.ModelForm):
    class Meta:
        model = SchoolImage
        exclude = ()


class LoginModel(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    def __str__(self):
        return f"${self.username}-{self.password}"


class LoginForm(forms.ModelForm):
    class Meta:
        model = LoginModel
        fields = "__all__"



class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password', 'style': 'margin-bottom: 10px;'}))
    confirmpassword = forms.CharField(widget=PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password', 'style': 'margin-bottom: 10px;'}))

    class Meta:
        model = AppUser
        fields = ['email', 'password', 'confirmpassword', 'phone', 'hiring_date', 'department', 'first_name',
                  'last_name']

        widgets = {
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'Email', 'style': 'margin-bottom: 10px;'}),
            'phone': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Phone', 'style': 'margin-bottom: 10px;'}),
            'hiring_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control', 'style': 'margin-bottom: 10px;'}),
            'department': forms.Select(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px;'}),
            'first_name': UppercaseInput(
                attrs={'class': 'form-control', 'placeholder': 'First Name', 'style': 'margin-bottom: 10px;'}),
            'last_name': UppercaseInput(
                attrs={'class': 'form-control', 'placeholder': 'Last Name', 'style': 'margin-bottom: 10px;'}),
        }




class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


from django import forms
from datetime import date

class LeaveApplicationForm(forms.ModelForm):
    accompanying_documents = MultipleFileField(required=False)

    class Meta:
        model = Leaveapplication
        fields = [
            'leave',
            'expected_start_date',
            'expected_end_date',
            'description',
            'accompanying_documents'
        ]

        widgets = {
            'leave': forms.Select(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px;'}),
            'duration_in_days': forms.NumberInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px;'}),
            'expected_start_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control', 'style': 'margin-bottom: 10px;'},
                format='%Y-%m-%d'
            ),
            'expected_end_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control', 'style': 'margin-bottom: 30px;'},
                format='%Y-%m-%d'
            ),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'style': 'margin-bottom: 50px;', 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super(LeaveApplicationForm, self).__init__(*args, **kwargs)
        # Set the initial value for 'expected_start_date' and 'expected_end_date' to the current date
        self.initial['expected_start_date'] = date.today()
        self.initial['expected_end_date'] = date.today()





class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = [
            'name',
        ]

        widgets = {
            'name': UppercaseInput(
                attrs={'class': 'form-control', 'placeholder': 'Leave Type', 'style': 'margin-bottom: 20px;'}),
        }


class AdminEditUserForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = [
            'met_satisfactory_performance',
            'is_fulltime',
            'is_teamlead',
            'is_projectlead',
        ]

        widgets = {
            'met_satisfactory_performance': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-bottom: 10px;'}),
            'is_fulltime': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-bottom: 10px;'}),
            'is_teamlead': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-bottom: 10px;'}),
            'is_projectlead': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-bottom: 10px;'}),
        }




class EditAppUser(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = [
            'first_name',
            'last_name',
            'phone',
            'department',
            # 'is_fulltime',
            # 'is_teamlead',
            # 'is_projectlead',
            # 'hiring_date',
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name', 'style': 'margin-bottom: 10px;'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name', 'style': 'margin-bottom: 10px;'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number', 'style': 'margin-bottom: 10px;'}),
            'department': forms.Select(attrs={'class': 'form-select', 'style': 'margin-bottom: 10px;'}),
            # 'is_fulltime': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-bottom: 10px;'}),
            'is_teamlead': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-bottom: 10px;'}),
            'is_projectlead': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-bottom: 10px;'}),
            'hiring_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control', 'style': 'margin-bottom: 10px;'})
        }




    days_in_advance = models.IntegerField(default=3, null=True, blank=True)



class CreateLeaveTypeForm(forms.ModelForm):
    class Meta:
        model = Leavetype
        fields = [
            'name',
            'days_in_advance',
            'leave_duration_in_days',
            'length_of_service_months',
            'is_full_time_employee',
            'is_document_backed',
            'is_satisfactory_performance_based',
            'has_exhausted_normal_leave_days',
            'duration_is_request_basis',
            'is_compensatory',
            'is_normal',
            'is_paid',
            'description',
        ]

        widgets = {
            'name': UppercaseInput(attrs={'class': 'form-control', 'placeholder': 'Leave Type', 'style': 'margin-bottom: 10px;'}),
            'leave_duration_in_days':  forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number', 'style': 'margin-bottom: 10px;'}),
            'days_in_advance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number', 'style': 'margin-bottom: 10px;'}),
            'length_of_service_months': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number', 'style': 'margin-bottom: 10px;'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Last Name', 'style': 'margin-bottom: 10px;'}),
            'is_full_time_employee': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-bottom: 10px;'}),
            'is_document_backed': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-bottom: 10px;'}),
            'is_satisfactory_performance_based': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-bottom: 10px;'}),
            'has_exhausted_normal_leave_days': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-bottom: 10px;'}),
            'duration_is_request_basis': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-bottom: 10px;'}),
            'is_compensatory': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-bottom: 10px;'}),
            'is_normal': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-bottom: 10px;'}),
            'is_paid': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'margin-bottom: 10px;'}),
        }



class ClearDateModel(models.Model):
    clearance_date = models.DateField()
    def __str__(self):
        return self.id


class ClearDateForm(forms.ModelForm):
    class Meta:
        model = ClearDateModel
        fields = [
            'clearance_date',
        ]

        widgets = {
            'clearance_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control', 'style': 'margin-bottom: 10px;'},
            ),
        }


class LeaveHistoryModel(models.Model):
    clearance_date = models.DateField()
    def __str__(self):
        return self.id


class Holiday(ParentModel):
    name = models.CharField(max_length=255, unique=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name






class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = [
            'name','date',
        ]

        widgets = {
            'name': UppercaseInput(
                attrs={'class': 'form-control', 'placeholder': 'Leave Type', 'style': 'margin-bottom: 20px;'}),
            'date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control', 'style': 'margin-bottom: 10px;'},
            ),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            return name.upper()
        else:
            return name