from django.urls import path

import web.views as webviews

urlpatterns = [

    path('', webviews.loginhomepage, name='loginpage'),
    path('registration', webviews.registration, name='registration'),
    path('logout', webviews.logoutView, name='logout'),

    path('apply', webviews.apply, name='apply'),
    path('userLeaves/<pk>', webviews.userLeavesView, name='userLeaves'),

    path('deleteLeaveApplication/<pk>', webviews.deleteLeaveApplicationView, name='deleteLeaveApplication'),
    path('approveApplication/<pk>', webviews.approveApplicationView, name='approveApplication'),
    path('rejectApplication/<pk>', webviews.rejectApplicationView, name='rejectApplication'),
    path('forwardApplication/<pk>', webviews.forwardApplicationView, name='forwardApplication'),
    path('deleteDepartment/<pk>', webviews.deleteDepartmentView, name='deleteDepartment'),

    path('applications', webviews.applicationsView, name='applications'),
    path('departments', webviews.departmentsView, name='departments'),
    path('users', webviews.usersView, name='users'),
    path('editprofile', webviews.editprofileView, name='editprofile'),
    path('leavetypes', webviews.leavetypesView, name='leavetypes'),
    path('editleavetype/<leavetypeid>', webviews.editleavetypeView, name='editleavetype'),
    path('deleteleavetype/<leavetypeid>', webviews.deleteleavetypeView, name='deleteleavetype'),
    path('leaveconfiguration', webviews.leaveconfigurationView, name='leaveconfiguration'),

    path('clear/<leaveapplicationid>', webviews.clearView, name='clear'),
    path('viewdocuments/<leaveapplicationid>', webviews.documentsView, name='viewdocuments'),

]
