from django import forms
from .models import Employee, Designation, Certification, Attendence,Event,Application,Payment
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.models import User



USER_TYPES = (

    ('Director', 'Director'),
    ('CHIEF_EXECUTIVE_OFFICER', 'CEO'),
    ('CHIEF_FINANCE_OFFICER', 'CFO'),
    ('CHIEF_TECHNOLOGY_OFFICER', 'CTO'),
    ('CHIEF_OPERATING_OFFICER', 'COO'),
    ('MANAGER_HUMAN_RESOURCES', 'MHR'),
    ('CONS', 'Consultant'),
    ('DEV', 'Developer'),
    ('INTERN', 'Internee')

)

ATTENDANCE_TYPES = (
    (1, 'ON TIME'),
    (2, 'LATE'),
    (3, 'ABSENT')
)

APPLICATION_TYPES = (
    (1, 'Sick Leave'),
    (2, 'Home Emergency'),
    (3, 'Others')
)

STATUS_TYPES = (
    (1,'Approved'),
    (2, 'Rejected'),
    (3, 'Pending'),
)

class EmployeeRegisterationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    # designation = forms.ModelMultipleChoiceField(queryset=Designation.objects.all(),required=False)
    # certification = forms.ModelMultipleChoiceField(queryset=Certification.objects.all(),required=False)

    class Meta:
        model = Employee
        fields = ['username', 'first_name', 'middle_name', 'last_name', 'email', 'password', 'basic_salary','designation',
                  'certification', 'emp_img']



class DesignationForm(forms.ModelForm):
    title = forms.ChoiceField(choices=USER_TYPES)
    job_discription = forms.Textarea()
    class Meta:
        model = Designation
        fields = ['title', 'job_discription']


class EmployeeLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Employee
        fields = ['username', 'password']


class EventForm(forms.ModelForm):

    event_date = forms.DateField(widget=forms.SelectDateWidget())
    event_start_time = forms.TimeField(widget=forms.TimeInput,label='Start Time(HH:MM)')
    event_end_time = forms.TimeField(widget=forms.TimeInput,label='End Time(HH:MM)')
    class Meta:
        model = Event
        fields = ['event_title', 'event_date', 'event_start_time', 'event_end_time',]


class AttendanceForm(forms.ModelForm):

    att_type = forms.ChoiceField(choices=ATTENDANCE_TYPES)

    class Meta:
        model = Attendence
        fields = ['event', 'employee', 'att_type']


class ApplicationForm(forms.ModelForm):
    application_title = forms.ChoiceField(choices=APPLICATION_TYPES)
    reason = forms.Textarea()
    application_date = forms.DateField(widget=forms.SelectDateWidget())

    class Meta:
        model =Application
        fields = ['application_title','application_date','number_of_days','reason']


class CertificationForm(forms.ModelForm):
    cert_logo = forms.FileField()

    class Meta:
        model = Certification
        fields = ['cert_name', 'cert_logo', 'cert_organization_name']


class PaymentForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget())
    employee = forms.ModelChoiceField(queryset=Employee.objects.all())

    class Meta:
        model = Payment
        fields = ['employee', 'amount', 'date']


class ApplicationApproveForm(forms.Form):
    approve = forms.BooleanField(widget=forms.CheckboxInput)
