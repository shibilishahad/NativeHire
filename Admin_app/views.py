from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from Admin_app.models import TypeOfJobs
from django.contrib.auth.models import User, auth
from NativeApp.models import Customer, Employer, Hiring, HiringHistory, Worker
from django.urls import reverse



def if_login(request,user):
    if request.user.is_authenticated:
        return None
    else:
        return redirect('user_login')
    

class AdminHome(View):
    def get(self, request):
        if if_login(request,request.user):
            return if_login(request, request.user)
        # total_yy = Hiring.objects.all()
        # total = total_yy.filter(status='Accepted')
        total = Hiring.objects.filter(status='Accepted')
        total1 = Hiring.objects.filter(status='Pending')
        worker = Worker.objects.all()
        customer = Customer.objects.all()
        hiring_history = HiringHistory.objects.all()
        # print('workreeeeeeeeee picc',worker.customer.profile_pic)
        employer = Employer.objects.all()
        return render(request, 'admin_home.html', {'worker': worker, 'employer': employer, 'total': total, 'total1': total1,'customer':customer,'hiring_history':hiring_history})

class AdminEmp(View):
    def get(self, request):
        if if_login(request,request.user):
            return if_login(request, request.user)
        worker = Worker.objects.all()
        customer = Customer.objects.all()
        emp = Customer.objects.all()
        employer = Employer.objects.all()

        return render(request, 'admin_emp.html', {'emp': emp,'worker':worker,'customer':customer,'employer':employer})

class AdminWorker(View):
    def get(self, request):
        if if_login(request,request.user):
            return if_login(request, request.user)
        emp = Customer.objects.all()
        worker = Worker.objects.all()
        customer = Customer.objects.all()
        employer = Employer.objects.all()
        return render(request, 'admin_worker.html', {'emp': emp,'worker':worker,'customer':customer,'employer':employer})

class Type(View):
    def get(self, request):
        if if_login(request, request.user):
            return if_login(request, request.user)
        job_types = TypeOfJobs.objects.all()
        worker = Worker.objects.all()
        customer = Customer.objects.all()
        employer = Employer.objects.all()
        return render(request, 'admin_job_types.html', {'job_types': job_types,'worker':worker,'customer':customer,'employer':employer})

    def post(self, request):
        if 'add_type' in request.POST:
            type_of_jobs = request.POST.get('type_of_jobs')
            if type_of_jobs:
                TypeOfJobs.objects.create(type_of_jobs=type_of_jobs)
        elif 'delete_type' in request.POST:
            type_id = request.POST.get('type_id')
            if type_id:
                TypeOfJobs.objects.filter(id=type_id).delete()
        elif 'update_type' in request.POST:
            type_id = request.POST.get('type_id')
            new_type_name = request.POST.get('new_type_name')
            if type_id and new_type_name:
                try:
                    job_type = TypeOfJobs.objects.get(id=type_id)
                    job_type.type_of_jobs = new_type_name
                    job_type.save()
                except TypeOfJobs.DoesNotExist:
                    pass

        return redirect(reverse('Admin_app:TypeView'))

class DeleteEmployer(View):
    def get(self, request):
        if if_login(request,request.user):
            return if_login(request, request.user)
        employer = Employer.objects.all()
        return render(request, 'delete_employer.html', {'employer': employer})

class DeleteEmp(View):
    def post(self, request, user_id):
        if if_login(request,request.user):
            return if_login(request, request.user)
        employer = Employer.objects.filter(user=user_id).first()
        employer1 = Customer.objects.filter(user=user_id).first()
        employer2 = User.objects.filter(id=user_id).first()
        employer2.delete()
        employer.delete()
        employer1.delete()
        return redirect(reverse('Admin_app:admin_emp'))

class DeleteWorker(View):
    def get(self, request):
        if if_login(request,request.user):
            return if_login(request, request.user)
        worker = Worker.objects.all()
        return render(request, 'delete_worker.html', {'worker': worker})

class DeleteWork(View):
    def post(self, request, user_id):
        if if_login(request,request.user):
            return if_login(request, request.user)
        worker = Worker.objects.filter(user=user_id).first()
        worker1 = Customer.objects.filter(user=user_id).first()
        worker2 = User.objects.filter(id=user_id).first()
        worker.delete()
        worker1.delete()
        worker2.delete()
        return redirect(reverse('Admin_app:admin_worker'))

class Notifications(View):
    def get(self, request, worker_id):
        if if_login(request,request.user):
            return if_login(request, request.user)
        employer = Employer.objects.all()
        customer = Customer.objects.all()
        worker = get_object_or_404(Worker, id=worker_id)
        workers = Worker.objects.all()
        return render(request, 'index.html', {'worker': worker, 'employer': employer, 'customer': customer,'workers':workers})
