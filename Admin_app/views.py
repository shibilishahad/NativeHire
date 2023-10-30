from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from Admin_app.models import TypeOfJobs
from django.contrib.auth.models import User, auth
from NativeApp.models import Customer, Employer, Hiring, Worker
from django.urls import reverse

class AdminHome(View):
    def get(self, request):
        total = Hiring.objects.filter(status='Accepted')
        total1 = Hiring.objects.filter(status='Pending')
        worker = Worker.objects.all()
        employer = Employer.objects.all()
        return render(request, 'admin_home.html', {'worker': worker, 'employer': employer, 'total': total, 'total1': total1})

class AdminEmp(View):
    def get(self, request):
        emp = Customer.objects.all()
        return render(request, 'admin_emp.html', {'emp': emp})

class AdminWorker(View):
    def get(self, request):
        emp = Customer.objects.all()
        return render(request, 'admin_worker.html', {'emp': emp})

class Type(View):
    def get(self, request):
        job_types = TypeOfJobs.objects.all()
        return render(request, 'admin_job_types.html', {'job_types': job_types})

    def post(self, request):
        if 'add_type' in request.POST:
            type_of_jobs = request.POST.get('type_of_jobs')
            if type_of_jobs:
                TypeOfJobs.objects.create(type_of_jobs=type_of_jobs)
        elif 'delete_type' in request.POST:
            type_id = request.POST.get('type_id')
            if type_id:
                TypeOfJobs.objects.filter(pk=type_id).delete()
        return redirect(reverse('Admin_app:TypeView'))

class DeleteEmployer(View):
    def get(self, request):
        employer = Employer.objects.all()
        return render(request, 'delete_employer.html', {'employer': employer})

class DeleteEmp(View):
    def post(self, request, user_id):
        employer = Employer.objects.filter(user=user_id).first()
        employer1 = Customer.objects.filter(user=user_id).first()
        employer2 = User.objects.filter(id=user_id).first()
        employer2.delete()
        employer.delete()
        employer1.delete()
        return redirect(reverse('Admin_app:admin_home'))

class DeleteWorker(View):
    def get(self, request):
        worker = Worker.objects.all()
        return render(request, 'delete_worker.html', {'worker': worker})

class DeleteWork(View):
    def post(self, request, user_id):
        worker = Worker.objects.filter(user=user_id).first()
        worker1 = Customer.objects.filter(user=user_id).first()
        worker2 = User.objects.filter(id=user_id).first()
        worker.delete()
        worker1.delete()
        worker2.delete()
        return redirect(reverse('Admin_app:admin_home'))

class LogoutAdmin(View):
    def get(self, request):
        auth.logout(request)
        return redirect('user_login')

class Notifications(View):
    def get(self, request, worker_id):
        employer = Employer.objects.all()
        customer = Customer.objects.all()
        worker = get_object_or_404(Worker, id=worker_id)
        return render(request, 'index.html', {'worker': worker, 'employer': employer, 'customer': customer})
