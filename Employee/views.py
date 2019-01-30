
# Create your views here.
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Designation, Certification, Employee, EmployeeDesignation, Application, Payment
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic, View
from django.urls import reverse
from .forms import EmployeeRegisterationForm , DesignationForm,EmployeeLoginForm, AttendanceForm,EventForm,ApplicationForm , CertificationForm, PaymentForm,ApplicationApproveForm

from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from datetime import date,time, timedelta
from .models import Event


class EmployeeList(ListView):
    model = Employee
    template_name = 'test/test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        directors = Employee.objects.get_Directors()
        context['directors'] = directors
        context['CEO'] = Employee.objects.get_CEO()
        context['CFO'] = Employee.objects.get_CFO()
        context['MHR'] = Employee.objects.get_MHR()
        context['CTO'] = Employee.objects.get_CTO()
        context['DEVS'] = Employee.objects.get_Developers()
        context['INTERNEES'] = Employee.objects.get_Internees()

        return context



class EmployeeDetail(DetailView):
    model = Employee
    template_name = 'test/test.html'
    context_object_name = 'EmployeeDetail'

    def get_object(self, queryset=None):
        
        return get_object_or_404(Employee, username=self.kwargs['username'])


class EmployeeSignup(View):

    def post(self, request, username):
        if request.user.is_authenticated and request.user.username == username:
            emp = Employee.objects.get(username=username)
            set1 = Employee.objects.get_CEO()
            set2 = Employee.objects.get_MHR()
            if (emp in set1) or (emp in set2):
                form = EmployeeRegisterationForm(request.POST, request.FILES)
                if form.is_valid():


                    emptemp=form.save(commit=False)
                    designations = form.cleaned_data['designation']
                    emptemp.save()
                    for des in designations:
                        destemp = Designation.objects.get(title=des)
                        EmployeeDesignation(emp=emptemp, desig=destemp).save()

                    return HttpResponseRedirect(reverse('EmployeeListView'))
                else:
                    context = {'form': form}
                    return render(request, 'test/test.html', context)
            else:
                return render(request, '404.html', {})
        else:
            return render(request, '404.html', {})

    def get(self, request, username):
        if request.user.is_authenticated and request.user.username == username:
            emp = Employee.objects.get(username=username)
            set1 = Employee.objects.get_CEO()
            set2 = Employee.objects.get_MHR()
            if (emp in set1) or (emp in set2):
                form = EmployeeRegisterationForm()
                context = {'form': form}
                return render(request, 'test/test.html', context)
            else:
                return render(request, '404.html', {})
        else:
            return render(request, '404.html', {})


class PendingApplicationList(ListView):
    model = Application
    template_name = 'test/test.html'

    def get_context_data(self, *, object_list=None, **kwargs):

        return {'Applications', Application.objects.get(status=3)}


class MyApplicationList(ListView):
    model = Application
    template_name = 'test/test.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        emp = Employee.objects.get(username=self.kwargs['username'])
        context['Applications'] = Application.objects.get(applicant=emp)
        return context


class PaymentList(ListView):
    model = Payment
    template_name = 'test/test.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payments'] = Payment.objects.all()
        return context



class addDesignation(View):


    def post(self, request, username):

        if request.user.is_authenticated and request.user.username == username:
            emp = Employee.objects.get(username=username)
            set1 = Employee.objects.get_CEO()
            set2 = Employee.objects.get_MHR()
            if (emp in set1) or (emp in set2):


                form = DesignationForm(request.POST)

                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(reverse('EmployeeListView'))
                else:
                    context = {'form' : form}
                    return render(request, 'test/test.html', context)
            else:
                return render(request,'404.html', {})
        else:
            return render(request, '404.html', {})

    def get(self,request ,username):
        if request.user.is_authenticated and request.user.username == username:
            emp = Employee.objects.get(username=username)
            set1 = Employee.objects.get_CEO()
            set2 = Employee.objects.get_MHR()
            if (emp in set1) or (emp in set2):
                form = DesignationForm()
                context = {'form' : form}
                return render(request, 'test/test.html', context)
            else:
                return render(request, '404.html', {})
        else:
            return render(request, '404.html', {})


class emplogin(View):

   def post(self,request):
       form = EmployeeLoginForm(request.POST)
       username = request.POST['username']
       password = request.POST['password']
       emp = authenticate(username=username, password=password)

       if emp is not None:
            login(request, emp)
            return render(request, 'test/test.html', {'form': DesignationForm()})
       else:
            return render(request, 'test/test.html', {'form': DesignationForm()})

   def get(self, request):
       return render(request, 'test/test.html', {'form': EmployeeLoginForm()})



class addAttendance(View):

    def post(self, request, username):
        if request.user.is_authenticated and request.user.username == username:
            emp = Employee.objects.get(username=username)
            set1 = Employee.objects.get_CEO()
            set2 = Employee.objects.get_MHR()
            if (emp in set1) or (emp in set2):
                form = AttendanceForm(request.POST)
                if form.is_valid():

                    form.save()
                    if request.POST['att_type'] == 3:
                        employee = form.cleaned_data['employee']
                        employee =Employee.objects.get(username=employee.username)
                        employee.leave_balance -= 1
                    return HttpResponseRedirect(reverse('EmployeeListView'))

                else:
                    return render(request, 'test/test.html', {'form':form})
            else:
                return render(request, '404.html', {})
        else:
            return render(request, '404.html', {})

    def get(self, request, username):
        if request.user.is_authenticated and request.user.username == username:
            emp = Employee.objects.get(username=username)
            set1 = Employee.objects.get_CEO()
            set2 = Employee.objects.get_MHR()
            if (emp in set1) or (emp in set2):
                return render(request, 'test.html', {'form':AttendanceForm()})
            else:
                return render(request, '404.html', {})
        else:
            return render(request, '404.html', {})


class addEvent(View):

    def post(self, request, username):
        if request.user.is_authenticated and request.user.username == username:
            emp = Employee.objects.get(username=username)
            set1 = Employee.objects.get_CEO()
            set2 = Employee.objects.get_MHR()
            if (emp in set1) or (emp in set2):
                form = EventForm(request.POST)
                if form.is_valid():

                    event_title=form.cleaned_data['event_title']
                    event_date = (form.cleaned_data['event_date'])
                    event_start_time=(form.cleaned_data['event_start_time'])
                    event_end_time=(form.cleaned_data['event_end_time'])
                    Event(event_title=event_title,event_date=event_date,event_start_time=event_start_time
                    ,event_end_time=event_end_time).save()
                    return HttpResponseRedirect(reverse('EmployeeListView'))

                else:
                    return render(request, 'test/test.html', {'form': form})

        return render(request, '404.html', {})

    def get(self, request, username):
        if request.user.is_authenticated and request.user.username == username:
            emp = Employee.objects.get(username=username)
            set1 = Employee.objects.get_CEO()
            set2 = Employee.objects.get_MHR()
            if (emp in set1) or (emp in set2):
                return render(request, 'test/test.html', {'form':EventForm()})

        return render(request,'404.html', {})



class addApplication(View):

    def post(self, request, username):
        if request.user.is_authenticated and request.user.username == username:
            emp = Employee.objects.get(username=username)


            form = ApplicationForm(request.POST)

            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('Employeelogindetailview'))
            else:
                return render(request, 'test/test.html', {'form':form})
        return render(request, '404.html', {})

    def get(self, request, username):
        if request.user.is_authenticated:

            return render(request,'test/test.html', {'form' : ApplicationForm()})
        return render(request, '404.html', {})



class addCertification(View):

    def post(self, request,username):
        if request.user.is_authenticated:

            emp = get_object_or_404(Employee, username=self.kwargs['username'])
            form = CertificationForm(request.POST, request.FILES)
            des1 = Designation.objects.filter(title='Director')
            des2 = Designation.objects.filter(title='CHIEF_EXECUTIVE_OFFICER')
            set1 = Employee.objects.filter(designation__in=des1)
            set2 = Employee.objects.filter(designation__in=des2)
            if form.is_valid() and ((emp in set1) or (emp in set2)):

                form.save()

                return HttpResponseRedirect(reverse('EmployeeListView'))

            else:
                return render(request, 'test/test.html', {'form': form})


    def get(self, request,username):

        return render(request, 'test/test.html', {'form':CertificationForm()})

class addPayment(View):
    def post(self, request, username):
        if request.user.is_authenticated and request.user.username ==username:

            emp = get_object_or_404(Employee, username=self.kwargs['username'])
            form = PaymentForm(request.POST, request.FILES)
            des1 = Designation.objects.filter(title='CHIEF_EXECUTIVE_OFFICER')
            des2 = Designation.objects.filter(title='CHIEF_FINANCE_OFFICER')
            set1 = Employee.objects.filter(designation__in=des1)
            set2 = Employee.objects.filter(designation__in=des2)
            if form.is_valid() and ((emp in set1) or (emp in set2)):

                form.save()

                return HttpResponseRedirect(reverse('EmployeeListView'))

            else:
                return render(request, 'test/test.html', {'form': form})

    def get(self, request, username):

        return render(request, 'test/test.html', {'form': PaymentForm()})










