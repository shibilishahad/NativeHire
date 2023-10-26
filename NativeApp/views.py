from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login
from .models import *
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage


def base(request):
    return render(request, 'base.html')

def home(request):
    return render(request, 'homepage.html')

class employer_reg(View):
    def get(self, request):
        return render(request, 'employer_reg.html')

    def post(self, request):
        
        data = User.objects.create_user(
            first_name =request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            username= request.POST.get('username'),
            email=request.POST.get('email'),
            password=request.POST.get('password')
        )
        data.save()

        customer = Customer(user=data,
                            phone_no=request.POST.get('phone_no'),
                            profile_pic=request.FILES.get('profile_pic'),
                            location=request.POST.get('location'),
                            user_type=request.POST.get('user_type')
                            )
        customer.save()

        employer = Employer(user=data)
        employer.save()



        return redirect('/')

class user_login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user_name_or_email = request.POST.get('user_name_or_email')
        password = request.POST.get('password')

        user = None

        if '@' in user_name_or_email:
            user = User.objects.filter(email=user_name_or_email).first()
            if user:
                user = authenticate(username=user.username, password=password)
                if not user.check_password(password):
                    user = None
        else:
            user = User.objects.filter(username=user_name_or_email).first()
            if user:
                authenticated_user = authenticate(username=user.username, password=password)
                if not authenticated_user.check_password(password):
                    user = None

        if user is not None:
            if user.is_staff:
                login(request, user)
                return render(request, 'admin_home.html')
            customer = Customer.objects.filter(user=user).first()
            if customer:
                if customer.user_type == 'worker':
                    worker = Worker.objects.get(user=user)
                    hiring_requests = worker.hiring_requests.all()
                    login(request, user)
                    workers = Worker.objects.all()
                    customers = Customer.objects.filter(user=request.user.id).first()
                    print("User details ",request.user)
                    print("prof pic ",customers.profile_pic.url)
                    hiring_requests = Hiring.objects.filter(worker=worker)
                    hiring_requests_count = hiring_requests.count()
                    return render(request, 'worker_home.html', {'worker': worker, 'workers': workers, 'customers': customers, 'hiring_requests': hiring_requests, 'hiring_requests_count': hiring_requests_count})
                elif customer.user_type == 'employer':
                    login(request, user)
                    employer = customer
                    workers = Worker.objects.all()
                    customers = Customer.objects.all() 
                    availability = Availability.objects.all()
                    return render(request, 'employer_home.html', {'employer': employer, 'workers': workers,'availability':availability,'customers':customers})
            else:
                return HttpResponse("Sorry, user does not exist")
        else:
            return HttpResponse("Sorry, user does not exist")


def nav(request):
    return render(request, 'admin_home.html')

def type(request):
    return render(request, 'type.html')

def w_base(request, user_name):
    worker = Customer.objects.get(user__username=user_name)
    availability = worker.worker.availability
    return render(request, 'worker_home.html', {'worker': worker, 'availability': availability})

# def e_home(request, user_name):
#     employer = Customer.objects.get(user__username=user_name)
#     workers = Worker.objects.all()
#     customers = Customer.objects.all()
#     return render(request, 'employer_home.html', {'employer': employer, 'workers': workers, 'customers': customers})

def admin_emp(request):
    emp = Customer.objects.all()
    return render(request, 'admin_emp.html', {'emp': emp})

class worker_reg(View):
    def get(self, request):
        return render(request, 'worker_reg.html')

    def post(self, request):
        data = User.objects.create_user(
                                    username=request.POST.get('username'),
                                    first_name=request.POST.get('first_name'),
                                    last_name=request.POST.get('last_name'),
                                    email=request.POST.get('email'),
                                    password=request.POST.get('password')
                                    )
        data.save()
    
        customer = Customer(user=data,
                            phone_no=request.POST.get('phone_no'),
                            profile_pic=request.FILES.get('profile_pic'),
                            location=request.POST.get('location'),
                            user_type=request.POST.get('user_type')
                            )
        customer.save()

        monday = request.POST.get('monday', False) == 'on'
        tuesday = request.POST.get('tuesday', False) == 'on'
        wednesday = request.POST.get('wednesday', False) == 'on'
        thursday = request.POST.get('thursday', False) == 'on'
        friday = request.POST.get('friday', False) == 'on'
        saturday = request.POST.get('saturday', False) == 'on'
        sunday = request.POST.get('sunday', False) == 'on'

        availability = Availability(
            monday=monday,
            tuesday=tuesday,
            wednesday=wednesday,
            thursday=thursday,
            friday=friday,
            saturday=saturday,
            sunday=sunday,
        )
        availability.save()

        job_type = Type(job_type=request.POST.get('job_type'))
        job_type.save()

        worker = Worker(
            user=data,
            type=job_type,
            availability=availability,
            wage=request.POST.get('wage'),
            experience=request.POST.get('experience')
        )
        worker.save()

        return redirect('/')

def employer_hire(request, worker_id):
    customer = Customer.objects.all()
    worker = get_object_or_404(Worker, id=worker_id)
    return render(request, 'employer_hire.html', {'worker': worker,'customer':customer})

def negotiate(request, worker_id):
    worker = get_object_or_404(Worker, id=worker_id)
    print('worker is ',worker)
    employer = request.user.employer_set.first()
    print('employer is ',employer)
    if employer:
        wage = request.POST.get('wage')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        hiring = Hiring.objects.create(
            employer=employer,
            worker=worker,
            start_date=start_date,
            end_date=end_date,
            cost=wage
        )
        hiring.save()
        message = f"You have received a hiring request from {employer.user.username}."
        notification = Notification.objects.create(worker=worker, hiring=hiring, message=message)
        notification.save()
        return HttpResponse('Worker booked')
    else:
        return HttpResponse('No associated employer found for the current user.')

def accept_hiring(request, hiring_id):
    hiring = get_object_or_404(Hiring, id=hiring_id)

    hiring.accept_request()
    return redirect('worker_home')

def reject_hiring(request, hiring_id):
    hiring = get_object_or_404(Hiring, id=hiring_id)


    hiring.reject_request()
    return redirect('worker_home')

