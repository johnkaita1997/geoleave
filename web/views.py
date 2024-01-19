# Create your views here.
import webbrowser
from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache

from appuser.models import AppUser
from departments.models import Department
from file_upload.models import SchoolImage
from geoleave import settings
from leave_applications.models import Leaveapplication
from leave_attachments.models import Leaveattachment
from leave_types.models import Leavetype
from utils import sendMail
from web.models import FileUploadWeb, LoginForm, RegistrationForm, LeaveApplicationForm, DepartmentForm, \
    AdminEditUserForm, EditAppUser, CreateLeaveTypeForm, ClearDateForm, HolidayForm, Holiday, \
    calculate_duration_excluding_weekends_and_holidays


def getProjectLeadSummaries(user):

    summarydictionary = {}

    current_date = datetime.now().date()
    current_year = current_date.year

    hiring_date = user.hiring_date
    difference = relativedelta(current_date, hiring_date)
    total_months = difference.years * 12 + difference.months
    length_of_service_in_months = total_months


    consumed_days = 0
    try:
        normal_leave_object = Leaveapplication.objects.get(
            dateofcreation__year=current_year,
            appuser=user,
            is_approved=True,
            leave__is_normal=True,
            is_active=True
        )

        if normal_leave_object:

            the_consumed_days = Leaveapplication.objects.filter(
                dateofcreation__year=current_year,
                appuser=user,
                leave__is_normal=True,
            ).exclude(id=normal_leave_object.id).aggregate(Sum('duration_in_days'))['duration_in_days__sum'] or 0

            start_date = normal_leave_object.expected_start_date
            end_date = normal_leave_object.expected_end_date

            if current_date > start_date:
                consumed_days = calculate_duration_excluding_weekends_and_holidays(start_date, current_date) + the_consumed_days
                print(f"Number of days until current date: {consumed_days}")
            else:
                consumed_days = the_consumed_days

    except ObjectDoesNotExist:

        print(f"Exception was surely found")

        consumed_days = Leaveapplication.objects.filter(
            dateofcreation__year=current_year,
            appuser=user,
            leave__is_normal=True,
            is_active=False
        ).aggregate(Sum('duration_in_days'))['duration_in_days__sum'] or 0


    try:
        leave_assigned_days = Leavetype.objects.get(is_normal=True)
        normal_leave_days_available = leave_assigned_days.leave_duration_in_days - consumed_days
    except ObjectDoesNotExist:
        leave_assigned_days = 0
        normal_leave_days_available = 0


    all_leave_applications = Leaveapplication.objects.filter (dateofcreation__year=current_year) or []
    all_approved_leave_applications = Leaveapplication.objects.filter (dateofcreation__year=current_year,is_approved=True) or []
    all_rejected_leave_applications = Leaveapplication.objects.filter (dateofcreation__year=current_year,is_approved=False) or []
    all_forwarded_leave_applications = Leaveapplication.objects.filter (dateofcreation__year=current_year,is_forwarded=True) or []

    all_Departments = Department.objects.all() or []

    departments = []
    for thedepartment in all_Departments:
        department_name = thedepartment.name
        department_leave_application_list = Leaveapplication.objects.filter(appuser__department=thedepartment, dateofcreation__year=current_year) or []
        number_of_leave_applications_in_department = len(department_leave_application_list)

        departments.append({
            "department_name" : department_name,
            "department_leave_application_list" : department_leave_application_list,
            "number_of_leave_applications_in_department" : number_of_leave_applications_in_department,
        })

    summarydictionary['all_leave_application_list'] = all_leave_applications
    summarydictionary['all_approved_leave_applications'] = all_approved_leave_applications
    summarydictionary['all_rejected_leave_applications'] = all_rejected_leave_applications
    summarydictionary['all_forwarded_leave_applications'] = all_forwarded_leave_applications

    summarydictionary['all_leave_application_list_len'] = len(all_leave_applications)
    summarydictionary['all_approved_leave_applications_len'] = len(all_approved_leave_applications)
    summarydictionary['all_rejected_leave_applications_len'] = len(all_rejected_leave_applications)
    summarydictionary['all_forwarded_leave_applications_len'] = len(all_forwarded_leave_applications)

    summarydictionary['normal_leave_days_available'] = normal_leave_days_available
    summarydictionary['days_on_leave'] = consumed_days
    summarydictionary['legth_of_service'] = length_of_service_in_months
    summarydictionary['departments'] = departments

    summarydictionary['user'] = user

    print(f"")


    return summarydictionary










def getuserLeaveDetails(user, department=None):

    summarydictionary = {}

    current_date = datetime.now().date()
    current_year = current_date.year

    hiring_date = user.hiring_date

    hiring_date = user.hiring_date
    difference = relativedelta(current_date, hiring_date)
    total_months = difference.years * 12 + difference.months
    length_of_service_in_months = total_months

    consumed_days = 0
    try:
        normal_leave_object = Leaveapplication.objects.get(
            dateofcreation__year=current_year,
            appuser=user,
            is_approved=True,
            leave__is_normal=True,
            is_active=True
        )

        if normal_leave_object:
            the_consumed_days = Leaveapplication.objects.filter(
                dateofcreation__year=current_year,
                appuser=user,
                leave__is_normal=True,
            ).exclude(id=normal_leave_object.id).aggregate(Sum('duration_in_days'))['duration_in_days__sum'] or 0

            start_date = normal_leave_object.expected_start_date
            end_date = normal_leave_object.expected_end_date

            if current_date > start_date:
                print(f"Added")
                consumed_days = calculate_duration_excluding_weekends_and_holidays(start_date, current_date) + the_consumed_days
                print(f"Number of days until current date: {consumed_days}")
            else:
                consumed_days = the_consumed_days

    except ObjectDoesNotExist:

        print(f"Exception was surely found")

        consumed_days = Leaveapplication.objects.filter(
            dateofcreation__year=current_year,
            appuser=user,
            leave__is_normal=True,
            is_active=False
        ).aggregate(Sum('duration_in_days'))['duration_in_days__sum'] or 0



    try:
        leave_assigned_days = Leavetype.objects.get(is_normal=True)
        normal_leave_days_available = leave_assigned_days.leave_duration_in_days - consumed_days
    except ObjectDoesNotExist:
        leave_assigned_days = 0
        normal_leave_days_available = 0


    leave_applications = Leaveapplication.objects.filter (appuser = user, dateofcreation__year=current_year) or []
    if department:
        print(f"Here {department}")
        leave_applications = Leaveapplication.objects.filter(appuser__department=department, dateofcreation__year=current_year) or []

    number_of_leave_appliations = len(leave_applications)


    summarydictionary['number_of_leave_appliations'] = number_of_leave_appliations
    summarydictionary['normal_leave_days_available'] = normal_leave_days_available
    summarydictionary['days_on_leave'] = consumed_days
    summarydictionary['legth_of_service'] = length_of_service_in_months
    summarydictionary['leave_application_list'] = leave_applications

    summarydictionary['user'] = user

    return summarydictionary



def checkLogin(request):
    if request.user.is_authenticated:
        user = request.user
        return user
    else:
        return redirect('loginpage')

@never_cache
def logoutView(request):
    print(f"activityName: logoutView")
    if request.user.is_authenticated:
        if 'globalschoolid' in globals():
            global globalschoolid
            del globalschoolid
        logout(request)
        return redirect('loginpage')


@never_cache
def FileUploadWebView(request):
    summarydictionary  = {}
    if request.method == 'POST':
        form = FileUploadWeb(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('The file is saved')
        else:
            print(form.errors)


    else:
        form = FileUploadWeb()
        summarydictionary['form'] = form

    return render(request, "addschool.html", {"summary": summarydictionary})




@never_cache
def loginhomepage(request):
    print(f"activityName: loginhomepage")
    summarydictionary = {}

    if request.user.is_authenticated:
        user = request.user
        if user.is_projectlead:
            summarydictionary = getProjectLeadSummaries(user)
            return render(request, "projectlead.html", {"summary": summarydictionary})
        elif user.is_teamlead:
            summarydictionary = getuserLeaveDetails(user, user.department)
            return render(request, "index.html", {"summary": summarydictionary})
        else:
            summarydictionary = getuserLeaveDetails(user)
            print(f"Getting now")
            return render(request, "index.html", {"summary": summarydictionary})

    else:
        print(f"Here 1")
        if request.method == 'POST':
            form = LoginForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username').strip()
                password = form.cleaned_data.get('password').strip()
                user = authenticate(request, username=username, password=password)
                if user is None:
                    form = LoginForm()
                    summarydictionary['form'] = form
                    messages.error(request, 'No active user found with the credentials')
                else:
                    login(request, user)
                    return redirect('loginpage')

            else:
                messages.error(request, 'Invalid Form')
                summarydictionary['form'] = form
                return redirect('loginpage')
        else:
            form = LoginForm()
            summarydictionary['form'] = form
            print(f"Here 1")
    response = render(request, "login.html", {"summary": summarydictionary})
    return response




@never_cache
def registration(request):
    summarydictionary = {}

    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password').strip()
            email = form.cleaned_data.get('email').strip()
            confirmpassword = form.cleaned_data.get('confirmpassword').strip()
            phone = form.cleaned_data.get('phone').strip()
            first_name = form.cleaned_data.get('first_name').strip()
            last_name = form.cleaned_data.get('last_name').strip()
            hiring_date = form.cleaned_data.get('hiring_date')
            department = form.cleaned_data.get('department')

            if password != confirmpassword:
                messages.error(request, 'Passwords did not match')
                return redirect('registration')

            data = {
                "email": email,
                "username": email,
                "last_name": last_name,
                "first_name": first_name,
                "phone": phone,
                "hiring_date": hiring_date,
                "password": password,
                "department": department,
                "confirmpassword": confirmpassword,
            }

            try:
                user = AppUser.objects.create(**data)
                with transaction.atomic():
                    user.set_password(password)
                    user.save()
            except Exception as exception:
                messages.error(request, str(exception))
                return redirect('registration')

            user = authenticate(request, username=email, password=password)
            if user is None:
                form = LoginForm()
                summarydictionary['form'] = form
                messages.error(request, 'No active user found with the credentials')
                return redirect('loginpage')
            else:
                login(request, user)
                return redirect('loginpage')

    form = RegistrationForm()
    summarydictionary['form'] = form
    response = render(request, "register.html", {"summary": summarydictionary})
    return response






@never_cache
def homepage(request):
    user = checkLogin(request)
    summarydictionary = {}
    summarydictionary['user'] = user

    response = render(request, "index.html", {"summary": summarydictionary})
    return response



@never_cache
def apply(request):
    user = checkLogin(request)
    summarydictionary = {}
    summarydictionary['user'] = user

    if request.method == 'POST':
        form = LeaveApplicationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            
            
            
            try:
                leave = form.cleaned_data.get('leave')
                duration_in_days = form.cleaned_data.get('duration_in_days')
                expected_start_date = form.cleaned_data.get('expected_start_date')
                expected_end_date = form.cleaned_data.get('expected_end_date')
                start_of_holiday_date = form.cleaned_data.get('start_of_holiday_date')
                end_of_holiday_date = form.cleaned_data.get('end_of_holiday_date')
                description = form.cleaned_data.get('description').strip()

                files = request.FILES.getlist('accompanying_documents')
                duration =calculate_duration_excluding_weekends_and_holidays(expected_start_date, expected_end_date)

                with transaction.atomic():
    
                    current_date = datetime.now().date()
                    current_year = current_date.year

                    normal_leave_days = 0
                    normal_leave_available_days = 0
                    if not leave.duration_is_request_basis:
                        normal_leave_days = Leavetype.objects.filter(is_normal=True).aggregate(Sum('leave_duration_in_days'))['leave_duration_in_days__sum'] or 0
                        normal_leave_available_days = normal_leave_days - duration
                        print(f"We got here {normal_leave_available_days}")

    
                    hiring_date = user.hiring_date
                    difference = relativedelta(current_date, hiring_date)
                    total_months = difference.years * 12 + difference.months
                    length_of_service_in_months = total_months

                    print(f"{hiring_date}, {current_date} {length_of_service_in_months}")

                    application_days_in_advance = (expected_start_date - current_date).days
    
                    consumed_days = Leaveapplication.objects.filter(
                        dateofcreation__year=current_year,
                        is_cleared=True,
                        appuser=user,
                        leave__is_normal=True,
                    ).aggregate(Sum('duration_in_days'))['duration_in_days__sum'] or 0


                    is_active_normal_leave = Leaveapplication.objects.filter(
                        dateofcreation__year=current_year,
                        is_active=True,
                        appuser=user,
                        leave__is_normal=True,
                    )
    

                    if is_active_normal_leave and leave.is_normal:
                        messages.success(request, f"You have an existing Normal Leave Application. It should be acted upon first")
                        return redirect('apply')
    

                    if leave.is_compensatory:
                        if not start_of_holiday_date or not end_of_holiday_date:
                            messages.error(request, f"Both start and end of holiday dates are required")
                            return redirect('apply')
                    if leave.is_full_time_employee:
                        if not user.is_fulltime:
                            messages.error(request, f"You must be a full time employee to apply for this leave")
                            return redirect('apply')
                    if leave.is_document_backed:
                        if not files or len(files) == 0:
                            messages.error(request, f"The requested leave requires backing documents")
                            return redirect('apply')
                    if leave.is_satisfactory_performance_based:
                        if not user.met_satisfactory_performance:
                            messages.error(request, f"You haven't met satisfactory requirements. Seek guidance from Project  Lead")
                            return redirect('apply')
                    if leave.has_exhausted_normal_leave_days:
                        if not user.met_satisfactory_performance:
                            messages.error(request, f"You haven't met satisfactory requirements. Seek guidance from Project  Lead")
                            return redirect('apply')

                    if leave.length_of_service_months and leave.length_of_service_months > 0:
                        if length_of_service_in_months < leave.length_of_service_months:
                            messages.error(request, f"You need to have worked for {leave.length_of_service_months} months to be eligible for this leave")
                            return redirect('apply')

                    if expected_start_date < current_date:
                        messages.error(request, "Start day cannot be in the past")
                        return redirect('apply')
                    else:
                        print("Start date is today or in the future.")

                    if expected_end_date < expected_start_date:
                        messages.error(request, "Leave end date must be after the start date")
                        return redirect('apply')
                    else:
                        print("Start date is today or in the future.")

                    if leave.days_in_advance and leave.days_in_advance >= 0:
                        if not leave.is_normal:
                            if application_days_in_advance < leave.days_in_advance:
                                messages.error(request, f"You are supposed to apply at least {leave.days_in_advance} days early. Your application is {application_days_in_advance} days early")
                                return redirect('apply')
                        else:
                            if duration <= 1:
                                check_against_days = 1
                            else:
                                check_against_days = leave.days_in_advance
                            if duration < check_against_days:
                                messages.error(request, f"You are supposed to apply at least {leave.days_in_advance} days early. Your application is {application_days_in_advance} days early")
                                return redirect('apply')


                    if not leave.duration_is_request_basis:
                        if leave.leave_duration_in_days and leave.leave_duration_in_days >0:
                            if duration > leave.leave_duration_in_days:
                                messages.error(request, f"You are only allowed {leave.leave_duration_in_days} days")
                                return redirect('apply')

                    if leave.is_normal:
                        if consumed_days >= normal_leave_days:
                            print(f"Consumed days is {consumed_days}")
                            messages.error(request,f"You have exhausted your normal leave days for this year 1")
                            return redirect('apply')
                        if normal_leave_available_days <= 0:
                            messages.error(request, f"You have exhausted your normal leave days for this year 2 {normal_leave_available_days}")
                            return redirect('apply')
    
    
    
                    leave_instance = Leaveapplication.objects.create(
                        appuser=user,
                        leave=leave,
                        description = description,
                        duration_in_days=duration,
                        expected_start_date=expected_start_date,
                        expected_end_date=expected_end_date,
                        start_of_holiday_date=start_of_holiday_date,
                        end_of_holiday_date=end_of_holiday_date
                    )
    
                    for file in files:
                        saved_file = SchoolImage.objects.create(
                            document=file,
                            creator=request.user,
                            original_file_name=file.name,
                            title="Upload",
                        )
    
                        Leaveattachment.objects.create(
                            name="name",
                            fileid=saved_file,
                            leave_application=leave_instance
                        )

                subject = f"{user.first_name} {user.last_name} -{user.department.name} - {duration} Days - {leave.name} Application"
                message = f"Leave request between {expected_start_date} and {expected_end_date}.\nReason : {description}"

                teamleademail = None
                projectleademail = None
                userdepartment = user.department
                try:
                    teamlead = AppUser.objects.filter(is_teamlead=True, department=userdepartment).first()
                    if teamlead:
                        teamleademail = teamlead.email
                except ObjectDoesNotExist:
                    pass

                try:
                    projectlead = AppUser.objects.filter(is_projectlead=True).first()
                    if projectlead:
                        projectleademail = projectlead.email
                except ObjectDoesNotExist:
                    pass

                if teamleademail:
                     sendMail(teamleademail, subject, message)
                if projectleademail:
                    sendMail(projectleademail, subject, message)

                messages.success(request, "Application made successfully")

                return redirect('loginpage')

            except Exception as exception:
                messages.success(request, f"{exception}")
                return redirect(request.META.get('HTTP_REFERER', 'loginpage'))


        else:
            print(f"Form is in-valid")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect('apply')

    form = LeaveApplicationForm()
    attatchmentform = FileUploadWeb()
    summarydictionary['form'] = form
    summarydictionary['attatchmentform'] = attatchmentform
    response = render(request, "apply.html", {"summary": summarydictionary})
    return response



@never_cache
def deleteLeaveApplicationView(request, pk):
    try:
        leaveapplication = Leaveapplication.objects.get(id=pk)
        leaveapplication.delete()
        messages.success(request, f"Leave was deleted successfully")
        return redirect('loginpage')
    except ObjectDoesNotExist:
        messages.success(request, f"Leave object does not exist")
        return redirect('loginpage')


@never_cache
def applicationsView(request):
    user = request.user
    summarydictionary = getuserLeaveDetails(user, user.department)
    summarydictionary['user'] = user
    response = render(request, "applications.html", {"summary": summarydictionary})
    return response


@never_cache
def approveApplicationView(request, pk):
    approve_user = request.user
    try:
        leaveapplication = Leaveapplication.objects.get(id=pk)
        leaveapplication.is_approved = True
        leaveapplication.approval_date = datetime.now()
        leaveapplication.approval_user = approve_user
        leaveapplication.is_forwarded = False
        leaveapplication.is_actedon = True
        leaveapplication.save()

        applicationuser = leaveapplication.appuser
        applicationuseremail = leaveapplication.appuser.email

        subject = f"APPROVAL {applicationuser.first_name} {applicationuser.last_name} -{applicationuser.department.name}  - {leaveapplication.leave.name} Application"
        message = f"Leave request for between dates {leaveapplication.expected_start_date} and {leaveapplication.expected_end_date} has been rejected by {approve_user.first_name} {approve_user.last_name}."

        projectleademail = None
        try:
            projectlead = AppUser.objects.filter(is_projectlead=True).first()
            if projectlead:
                projectleademail = projectlead.email
        except ObjectDoesNotExist:
            pass

        sendMail(applicationuseremail, subject, message)
        if projectleademail:
            sendMail(projectleademail, subject, message)


        messages.success(request, f"Leave was approved successfully")
        if approve_user.is_projectlead:
            return redirect('loginpage')
        return redirect('applications')

    except ObjectDoesNotExist:
        messages.success(request, f"Leave object does not exist")
        if approve_user.is_projectlead:
            return redirect('loginpage')
        return redirect('applications')



@never_cache
def rejectApplicationView(request, pk):
    reject_user = request.user
    try:
        leaveapplication = Leaveapplication.objects.get(id=pk)
        leaveapplication.is_approved = False
        leaveapplication.approval_date = datetime.now()
        leaveapplication.approval_user = reject_user
        leaveapplication.is_forwarded = False
        leaveapplication.is_actedon = True
        leaveapplication.is_active = False
        leaveapplication.save()

        applicationuser = leaveapplication.appuser
        applicationuseremail = leaveapplication.appuser.email

        subject = f"REJECTION {applicationuser.first_name} {applicationuser.last_name} -{applicationuser.department.name}  - {leaveapplication.leave.name} Application"
        message = f"Leave request for between dates {leaveapplication.expected_start_date} and {leaveapplication.expected_end_date} has been rejected by {reject_user.first_name} {reject_user.last_name}."

        projectleademail = None
        try:
            projectlead = AppUser.objects.filter(is_projectlead=True).first()
            if projectlead:
                projectleademail = projectlead.email
        except ObjectDoesNotExist:
            pass

        sendMail(applicationuseremail, subject, message)
        if projectleademail:
            sendMail(projectleademail, subject, message)

        messages.success(request, f"Leave was rejected successfully")
        if reject_user.is_projectlead:
            return redirect('loginpage')
        return redirect('applications')


    except ObjectDoesNotExist:
        messages.success(request, f"Leave object does not exist")
        if reject_user.is_projectlead:
            return redirect('loginpage')
        return redirect('applications')

@never_cache
def forwardApplicationView(request, pk):
    try:
        forward_user = request.user
        leaveapplication = Leaveapplication.objects.get(id=pk)
        leaveapplication.is_forwarded = True
        leaveapplication.forwarded_date = datetime.now()
        leaveapplication.approval_user = forward_user
        leaveapplication.is_approved = False
        leaveapplication.is_actedon = True
        leaveapplication.save()


        applicationuser = leaveapplication.appuser
        applicationuseremail = leaveapplication.appuser.email

        subject = f"FORWARDED - {applicationuser.first_name} {applicationuser.last_name} -{applicationuser.department.name}  - {leaveapplication.leave.name} Application"
        message = f"Leave request for between dates {leaveapplication.expected_start_date} and {leaveapplication.expected_end_date} has been forwarded to Project Lead."

        projectleademail = None
        try:
            projectlead = AppUser.objects.filter(is_projectlead=True).first()
            if projectlead:
                projectleademail = projectlead.email
        except ObjectDoesNotExist:
            pass

        sendMail(applicationuseremail, subject, message)
        if projectleademail:
            sendMail(projectleademail, subject, message)

        messages.success(request, f"Leave was forwarded successfully")
        return redirect('applications')
    except ObjectDoesNotExist:
        messages.success(request, f"Leave object does not exist")
        return redirect('applications')

@never_cache
def deleteDepartmentView(request, pk):
    try:
        department = Department.objects.get(id=pk)
        department.delete()
        messages.success(request, f"Department was deleted successfully")
        return redirect('departments')
    except ObjectDoesNotExist:
        messages.success(request, f"Department does not exist")
        return redirect('departments')





@never_cache
def departmentsView(request):
    user = request.user
    summarydictionary = getuserLeaveDetails(user, user.department)
    summarydictionary['user'] = user

    department_list = Department.objects.all()
    summarydictionary['department_list'] = department_list

    if request.method == 'POST':
        form = DepartmentForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name').strip()
            Department.objects.create(
                name = name
            )
            messages.success(request, f"Department was saved successfully")
            return redirect('departments')

        else:
            messages.error(request, 'Invalid Form')
            summarydictionary['form'] = form
            return redirect('departments')

    else:
        form = DepartmentForm()
        summarydictionary['form'] = form

    response = render(request, "departments.html", {"summary": summarydictionary})
    return response



@never_cache
def usersView(request):
    user = request.user
    summarydictionary = getuserLeaveDetails(user, user.department)
    summarydictionary['user'] = user

    user_list = AppUser.objects.all()
    summarydictionary['user_list'] = user_list

    response = render(request, "users.html", {"summary": summarydictionary})
    return response



@never_cache
def userLeavesView(request, pk):
    try:
        user = AppUser.objects.get(id=pk)
    except ObjectDoesNotExist:
        messages.success(request, f"User does not exist")
        return redirect('users')

    summarydictionary = getuserLeaveDetails(user)
    summarydictionary['user'] = user

    if request.method == 'POST':
        form = AdminEditUserForm(data=request.POST)
        if form.is_valid():
            met_satisfactory_performance = form.cleaned_data.get('met_satisfactory_performance')
            is_fulltime = form.cleaned_data.get('is_fulltime')
            is_teamlead = form.cleaned_data.get('is_teamlead')
            hiring_date = form.cleaned_data.get('hiring_date')

            user.met_satisfactory_performance = met_satisfactory_performance
            user.is_fulltime = is_fulltime
            user.is_teamlead = is_teamlead
            user.hiring_date = hiring_date

            user.save()
            messages.success(request, f"User was saved successfully")
            return redirect('userLeaves', pk)

        else:
            messages.error(request, 'Invalid Form')
            summarydictionary['form'] = form
            return redirect('userLeaves', pk)

    else:
        form = AdminEditUserForm(initial={
            'met_satisfactory_performance': user.met_satisfactory_performance,
            'is_fulltime': user.is_fulltime,
            'is_teamlead': user.is_teamlead,
            'hiring_date': user.hiring_date,
        })
        summarydictionary['form'] = form

    response = render(request, "viewuserdetails.html", {"summary": summarydictionary})
    return response




@never_cache
def editprofileView(request):
    user = request.user
    summarydictionary = getuserLeaveDetails(user)
    summarydictionary['user'] = user

    if request.method == 'POST':
        form = EditAppUser(data=request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name').strip()
            last_name = form.cleaned_data.get('last_name').strip()
            phone = form.cleaned_data.get('phone').strip()
            department = form.cleaned_data.get('department')
            is_fulltime = form.cleaned_data.get('is_fulltime')
            is_teamlead = form.cleaned_data.get('is_teamlead')
            is_projectlead = form.cleaned_data.get('is_projectlead')

            user.is_fulltime = is_fulltime
            user.department = department
            user.first_name = first_name
            user.last_name = last_name
            user.is_teamlead = is_teamlead
            user.is_projectlead = is_projectlead
            user.phone = phone

            user.save()
            messages.success(request, f"Update was successful")
            return redirect('loginpage')

        else:
            messages.error(request, 'Invalid Form')
            summarydictionary['form'] = form
            return redirect('editprofile', )

    else:
        form = EditAppUser(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone,
            'department': user.department,
            'is_fulltime': user.is_fulltime,
            'is_teamlead': user.is_teamlead,
            'is_projectlead': user.is_projectlead,
        })
        summarydictionary['form'] = form

    response = render(request, "editprofile.html", {"summary": summarydictionary})
    return response






@never_cache
def documentsView(request, leaveapplicationid):
    try:

        user = request.user
        summarydictionary = getuserLeaveDetails(user)
        summarydictionary['user'] = user

        try:
            leaveapplication = Leaveapplication.objects.get(id=leaveapplicationid)
            leave_description = leaveapplication.description
        except ObjectDoesNotExist:
            messages.success(request, f"This leave application does not exist")
            return redirect(request.META.get('HTTP_REFERER', 'loginpage'))

        attachments = Leaveattachment.objects.filter(leave_application__id=leaveapplicationid)

        # if not attachments:
        #     messages.success(request, f"This application has no attachments")
        #     return redirect(request.META.get('HTTP_REFERER', 'loginpage'))

        attachment_list = []
        for attachment in attachments:
            try:
                actual_file = SchoolImage.objects.get(id=attachment.fileid.id)
                attachment_url = request.build_absolute_uri(f"{settings.MEDIA_URL}{actual_file.document}")
                attachment_list.append(attachment_url)
                print(f"{attachment_url}")
            except ObjectDoesNotExist:
                pass
        return render(request, 'openattachments.html', {'attachments': attachment_list, 'description': leave_description, 'summary':summarydictionary})

    except ObjectDoesNotExist:
        messages.success(request, f"This leave application does not exist")
        return redirect(request.META.get('HTTP_REFERER', 'loginpage'))






@never_cache
def leavetypesView(request):
    user = checkLogin(request)
    summarydictionary = {}
    summarydictionary['user'] = user

    if request.method == 'POST':
        form = CreateLeaveTypeForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            is_full_time_employee = form.cleaned_data.get('is_full_time_employee')
            leave_duration_in_days = form.cleaned_data.get('leave_duration_in_days')
            length_of_service_months = form.cleaned_data.get('length_of_service_months')
            is_document_backed = form.cleaned_data.get('is_document_backed')
            is_satisfactory_performance_based = form.cleaned_data.get('is_satisfactory_performance_based')
            has_exhausted_normal_leave_days = form.cleaned_data.get('has_exhausted_normal_leave_days')
            duration_is_request_basis = form.cleaned_data.get('duration_is_request_basis')
            is_compensatory = form.cleaned_data.get('is_compensatory')
            is_normal = form.cleaned_data.get('is_normal')
            is_paid = form.cleaned_data.get('is_paid')
            days_in_advance = form.cleaned_data.get('days_in_advance')

            normal_leave_type = Leavetype.objects.get(is_normal=True)
            if normal_leave_type and is_normal:
                messages.success(request, f"A normal leave type already exists")
                return redirect(request.META.get('HTTP_REFERER', 'loginpage'))

            try:
                with transaction.atomic():

                    Leavetype.objects.create(
                        name = name,
                        description = description,
                        is_full_time_employee = is_full_time_employee,
                        leave_duration_in_days = leave_duration_in_days,
                        length_of_service_months = length_of_service_months,
                        is_document_backed = is_document_backed,
                        is_satisfactory_performance_based = is_satisfactory_performance_based,
                        has_exhausted_normal_leave_days = has_exhausted_normal_leave_days,
                        duration_is_request_basis = duration_is_request_basis,
                        is_compensatory = is_compensatory,
                        is_normal = is_normal,
                        days_in_advance = days_in_advance,
                        is_paid = is_paid,
                    )

                messages.success(request, "Leave Type Created Successfully")
                return redirect(request.META.get('HTTP_REFERER', 'loginpage'))
            except Exception as exception:
                print(f"An error has occured {str(exception)}")
                messages.error(request, str(exception))
                return redirect(request.META.get('HTTP_REFERER', 'loginpage'))

        else:
            print(f"Form is in-valid")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect(request.META.get('HTTP_REFERER', 'loginpage'))


    leavetypes = Leavetype.objects.all()
    form = CreateLeaveTypeForm()
    summarydictionary['form'] = form
    summarydictionary['leavetypes'] = leavetypes

    response = render(request, "leavetypes.html", {"summary": summarydictionary})
    return response





@never_cache
def editleavetypeView(request, leavetypeid):
    user = request.user
    summarydictionary = getuserLeaveDetails(user)
    summarydictionary['user'] = user

    try:
        leave_type = Leavetype.objects.get(id=leavetypeid)
    except ObjectDoesNotExist:
        messages.success(request, f"Selected Leave Type Does Not Exist")
        return redirect(request.META.get('HTTP_REFERER', 'loginpage'))

    if request.method == 'POST':
        form = CreateLeaveTypeForm(data=request.POST)
        if form.is_valid():

            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            is_full_time_employee = form.cleaned_data.get('is_full_time_employee')
            leave_duration_in_days = form.cleaned_data.get('leave_duration_in_days')
            length_of_service_months = form.cleaned_data.get('length_of_service_months')
            is_document_backed = form.cleaned_data.get('is_document_backed')
            is_satisfactory_performance_based = form.cleaned_data.get('is_satisfactory_performance_based')
            has_exhausted_normal_leave_days = form.cleaned_data.get('has_exhausted_normal_leave_days')
            duration_is_request_basis = form.cleaned_data.get('duration_is_request_basis')
            is_compensatory = form.cleaned_data.get('is_compensatory')
            is_normal = form.cleaned_data.get('is_normal')
            days_in_advance = form.cleaned_data.get('days_in_advance')

            leave_type.name = name
            leave_type.description = description
            leave_type.is_full_time_employee = is_full_time_employee
            leave_type.leave_duration_in_days = leave_duration_in_days
            leave_type.length_of_service_months = length_of_service_months
            leave_type.is_document_backed = is_document_backed
            leave_type.is_satisfactory_performance_based = is_satisfactory_performance_based
            leave_type.has_exhausted_normal_leave_days = has_exhausted_normal_leave_days
            leave_type.duration_is_request_basis = duration_is_request_basis
            leave_type.is_compensatory = is_compensatory
            leave_type.is_normal = is_normal
            leave_type.days_in_advance = days_in_advance

            leave_type.save()

            messages.success(request, f"Update was successful")
            return redirect('leavetypes')

        else:
            messages.error(request, 'Invalid Form')
            summarydictionary['form'] = form
            return redirect('editprofile', )

    else:
        form = CreateLeaveTypeForm(initial={
        "name": leave_type.name,
        "description": leave_type.description,
        "is_full_time_employee": leave_type.is_full_time_employee,
        "leave_duration_in_days": leave_type.leave_duration_in_days,
        "length_of_service_months": leave_type.length_of_service_months,
        "is_document_backed": leave_type.is_document_backed,
        "is_satisfactory_performance_based": leave_type.is_satisfactory_performance_based,
        "has_exhausted_normal_leave_days": leave_type.has_exhausted_normal_leave_days,
        "duration_is_request_basis": leave_type.duration_is_request_basis,
        "is_compensatory": leave_type.is_compensatory,
        "is_normal": leave_type.is_normal,
        })
        summarydictionary['form'] = form

    response = render(request, "editleave.html", {"summary": summarydictionary})
    return response





@never_cache
def deleteleavetypeView(request, leavetypeid):
    user = request.user
    summarydictionary = getuserLeaveDetails(user)
    summarydictionary['user'] = user

    try:
        leave_type = Leavetype.objects.get(id=leavetypeid)
    except ObjectDoesNotExist:
        messages.success(request, f"Selected Leave Type Does Not Exist")
        return redirect(request.META.get('HTTP_REFERER', 'loginpage'))

    leave_type.delete()
    messages.success(request, f"Action was successful")
    return redirect('leavetypes')






@never_cache
def leaveconfigurationView(request):
        user = request.user
        summarydictionary = getuserLeaveDetails(user)
        summarydictionary['user'] = user

        leavetypes = Leavetype.objects.all()
        summarydictionary['leavetypes'] = leavetypes

        response = render(request, "leaveconfig.html", {"summary": summarydictionary})

        return response





@never_cache
def clearView(request, leaveapplicationid):
    summarydictionary = {}
    summarydictionary['user'] = request.user
    if request.method == 'POST':
        form = ClearDateForm(data=request.POST)
        if form.is_valid():
            clearance_date = form.cleaned_data.get('clearance_date')
            return redirect('clearDateView', leaveapplicationid, clearance_date)
        else:
            messages.error(request, 'Invalid Form')
            summarydictionary['form'] = form
            return redirect(request.META.get('HTTP_REFERER', 'loginpage'))
    else:
        form = ClearDateForm()
        summarydictionary['form'] = form
        print(f"Form is bound: {form.is_bound}")
        print(f"Form errors: {form.errors}")
    response = render(request, "cleardate.html", {"summary": summarydictionary})
    return response







@never_cache
def clearDateView(request, leaveapplicationid, thetime):
    user = request.user

    try:

        thetime = datetime.strptime(thetime, '%Y-%m-%d').date()

        leave_application = Leaveapplication.objects.get(id=leaveapplicationid)
        leave_application.is_cleared = True
        leave_application.clearance_date = thetime
        leave_application.duration_in_days = calculate_duration_excluding_weekends_and_holidays(leave_application.expected_start_date, thetime)

        leave_application.is_approved = False
        leave_application.is_forwarded = False
        leave_application.is_actedon = True
        leave_application.approval_user = user
        leave_application.is_active = False

        leave_application.save()

        messages.success(request, f"Leave application has been marked as cleared")
        return redirect('loginpage')
    except ObjectDoesNotExist:
        messages.success(request, f"This leave application does not exist")
        return redirect('loginpage')









@never_cache
def holidayView(request):
    user = request.user
    summarydictionary = getProjectLeadSummaries(user)
    summarydictionary['user'] = user

    holiday_list = Holiday.objects.all()
    summarydictionary['holiday_list'] = holiday_list

    if request.method == 'POST':
        form = HolidayForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name').strip()
            date = form.cleaned_data.get('date')
            Holiday.objects.create(
                name = name,
                date = date
            )
            messages.success(request, f"Holiday was saved successfully")
            return redirect('holiday')

        else:
            messages.error(request, 'Invalid Form')
            summarydictionary['form'] = form
            return redirect('holiday')

    else:
        form = HolidayForm()
        summarydictionary['form'] = form

    response = render(request, "holiday.html", {"summary": summarydictionary})
    return response




@never_cache
def deleteholidayView(request, pk):
    try:
        holiday = Holiday.objects.get(id=pk)
        holiday.delete()
        messages.success(request, f"Holiday was deleted successfully")
        return redirect('holiday')
    except ObjectDoesNotExist:
        messages.success(request, f"Holiday does not exist")
        return redirect('holiday')
