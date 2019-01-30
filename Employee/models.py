from django.db import models
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
from django.conf import settings
# Create your models here.


ATTENDANCE_TYPES =(
    (1, 'ON TIME'),
    (2, 'LATE'),
    (3, 'ABSENT')
)

STATUS_TYPES =(
    (1, 'approved'),
    (2, 'pending'),
    (3 , 'Rejected')

)

class EmployeeManager(UserManager):

    def get_Directors(self):
        temp = Designation.objects.filter(title='Director')
        return self.filter(designation__in=temp)

    def get_CEO(self):
        temp = Designation.objects.filter(title='CHIEF_EXECUTIVE_OFFICER')
        return self.filter(designation__in=temp)

    def get_CFO(self):
        temp = Designation.objects.filter(title='CHIEF_FINANCE_OFFICER')
        return self.filter(designation__in=temp)

    def get_MHR(self):
        temp = Designation.objects.filter(title='MANAGER_HUMAN_RESOURCES')
        return self.filter(designation__in=temp)

    def get_CTO(self):
        temp = Designation.objects.filter(title='CHIEF_TECHNOLOGY_OFFICER')
        return self.filter(designation__in=temp)


    def get_Consultants(self):
        temp = Designation.objects.filter(title='CONS')
        return self.filter(designation__in=temp)

    def get_Developers(self):
        temp = Designation.objects.filter(title='DEV')
        return self.filter(designation__in=temp)

    def get_Internees(self):
        temp = Designation.objects.filter(title='INTERN')
        return self.filter(designation__in=temp)



class Certification(models.Model):
    cert_id = models.AutoField(primary_key=True)
    cert_name = models.CharField(max_length=50)
    cert_logo = models.FileField(default=None, blank=True, null=True,upload_to='certification')
    cert_organization_name = models.CharField(max_length=100)

    def __str__(self):
        return self.cert_name+'  Passed from  '+self.cert_organization_name


class Designation(models.Model):
    desig_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=60, unique=True)
    job_discription = models.CharField(max_length=2000)

    def __str__(self):
        return self.title


class Employee(AbstractUser):
    middle_name = models.CharField(max_length=20, blank=True,  null=True)
    basic_salary = models.FloatField(default=1)
    designation = models.ManyToManyField(Designation, default=None, blank=True,
                                         through='EmployeeDesignation')
    certification = models.ManyToManyField(Certification, default=None, null=True, blank=True,
                                            through='EmployeeCertification')
    emp_img = models.FileField(default=None,upload_to='employees')
    leaves_allowed = models.IntegerField(default=25)
    leave_balance = models.IntegerField(default=25)
    leave_count = models.IntegerField(default=0)
    objects = EmployeeManager()

    def __str__(self):
        return self.first_name+' '+self.last_name

    def is_leaves_left(self):
        if self.leave_balance > 0:
            return True
        else:
            return False


class EmployeeDesignation(models.Model):

    desig = models.ForeignKey(Designation, on_delete=models.CASCADE)
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE)



    class Meta:
        unique_together = (('emp', 'desig'),)


class EmployeeCertification(models.Model):

    certi = models.ForeignKey(Certification, on_delete=models.CASCADE)
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('certi', 'emp'),)


class Event(models.Model):
    event_title = models.CharField(max_length=30)
    event_date = models.DateField()
    event_start_time = models.TimeField()
    event_end_time = models.TimeField()


    def __str__(self):
        return  self.event_title+' '




class Attendence(models.Model):
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING)
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    att_type = models.CharField(max_length=20)

    class Meta:
        unique_together = (('event', 'employee'),)

    def __str__(self):
        return self.employee.first_name


class Application(models.Model):
    application_title = models.CharField(max_length=20)
    application_date = models.DateField()
    number_of_days = models.PositiveIntegerField()
    applicant = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    reason = models.CharField(max_length=1000)
    status = models.IntegerField(choices=STATUS_TYPES)

    def __str__(self):
        self.application_date.value_to_string(str)
        return self.application_title+' '+str


class Payment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    amount = models.FloatField(default=0)
    date = models.DateField(default=datetime.date.today)

