from django.contrib import admin
from .models import Designation, Employee, Certification,EmployeeDesignation,EmployeeCertification,Attendence,Event,Application
# Register your models here.

admin.site.register(Designation)
admin.site.register(Employee)
admin.site.register(Certification)
admin.site.register(EmployeeDesignation)
admin.site.register(EmployeeCertification)
admin.site.register(Event)
admin.site.register(Attendence)
admin.site.register(Application)
