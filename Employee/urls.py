from django.urls import path
from . import views

urlpatterns = [

    path('', views.EmployeeList.as_view(), name='EmployeeListView'),

    path('portal', views.emplogin.as_view(), name='emploginview'),

    path('portal/<str:username>/add-designation', views.addDesignation.as_view(), name='DesignationCreateView'),

    path('portal/<str:username>/add-employee', views.EmployeeSignup.as_view(), name='EmployeeCreateView'),

    path('portal/<str:username>/add-event', views.addEvent.as_view(), name='EventCreateView'),

    path('portal/<str:username>/add-attendance', views.addAttendance.as_view(), name='AttendanceCreateView'),

    path('portal/<str:username>/add-application', views.addApplication.as_view(), name='ApplicationCreateView'),

    path('portal/<str:username>', views.EmployeeDetail.as_view(),name='EmployeeLoginDetailView'),

    path('portal/<str:username>/add-certification', views.addCertification.as_view(), name='CreateCertificationView'),

    path('portal/<str:username>/all-pendingapplication',views.PendingApplicationList.as_view(), name='PendingApplicationList'),

    path('portal/<str:username>/applications',views.MyApplicationList.as_view(), name='AllApplicationList'),

    path('portal/<str:username>/payments',views.PaymentList.as_view(), name='AllPaymentList'),

    path('<str:username>', views.EmployeeDetail.as_view(), name='EmployeeDetailView'),



]