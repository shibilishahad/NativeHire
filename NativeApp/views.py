import json
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re






def base(request):
    return render(request, 'base.html')

def home(request):
    return render(request, 'homepage.html')

class employer_reg(SuccessMessageMixin, View):
    success_message = "User registered successfully"

    def get(self, request):
        return render(request, 'employer_reg.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')

        user = User.objects.filter(username=username, email=email).first()
        if user:
            messages.error(request, "User with the same email/username already exists. Please try with another username/email")
            return redirect('employer_reg')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email address. Please provide a valid email.")
            return redirect('employer_reg')

        password = request.POST.get('password')
        if not self.is_valid_password(password):
            messages.error(request, "Invalid password. Password must contain atleast one Capital letter, small letter , number and special character.")
            return redirect('employer_reg')

        phone_no = request.POST.get('phone_no')
        if not self.phone_no_is_valid(phone_no):
            messages.error(request, "Invalid phone number. Please provide a valid 10-digit phone number.")
            return redirect('employer_reg')

        data = User.objects.create_user(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            username=request.POST.get('username'),
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

        messages.success(request, self.success_message)
        return redirect('user_login')

    def is_valid_password(self, password):
        password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W).{8,}"
        return bool(re.match(password_pattern, password))

    def phone_no_is_valid(self, phone_no):
        return phone_no.isdigit() and len(phone_no) == 10

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
                if not user or not user.check_password(password):
                    messages.error(request, "Invalid email or password")
                    return redirect('user_login')
                
        else:
            user = User.objects.filter(username=user_name_or_email).first()
            if user:
                authenticated_user = authenticate(username=user.username, password=password)
                if not authenticated_user or not authenticated_user.check_password(password):
                    messages.error(request, "Invalid username or password")
                    return redirect('user_login')
            else:
                    messages.error(request, "Invalid username or password")
                    return redirect('user_login')

        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('Admin_app:admin_home')
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
                    hiring_requests = Hiring.objects.filter(worker=worker, status = 'Pending')
                    hiring_requests_count = hiring_requests.count()
                    return render(request, 'worker_home.html', {'worker': worker, 'workers': workers, 'customers': customers, 'hiring_requests': hiring_requests, 'hiring_requests_count': hiring_requests_count})
                elif customer.user_type == 'employer':
                    login(request, user)
                    employer = customer
                    workers = Worker.objects.all()
                    customers = Customer.objects.all() 
                    return render(request, 'employer_home.html', {'employer': employer, 'workers': workers,'customers':customers}) 
                else:
                    messages.error(request, "Sorry, user does not exist")
                    return redirect('user_login')
            else:
                messages.error(request, "Sorry, user does not exist")
                return redirect('user_login')
        else:
            messages.error(request, "Sorry, user does not exist")
            return redirect('user_login')
        
def logout_worker(request):
    auth.logout(request)
    print('logged out ',logout)
    return redirect('user_login')
        
def logout_employer(request):
    auth.logout(request)
    print('logged out employer',logout)
    return redirect('user_login')

def nav(request):
    return render(request, 'admin_home.html')

def type(request):
    return render(request, 'type.html')

# def w_base(request, user_name):
#     worker = Customer.objects.get(user__username=user_name)
#     availability = worker.worker.availability
#     return render(request, 'worker_home.html', {'worker': worker, 'availability': availability})

# def e_home(request, user_name):
#     employer = Customer.objects.get(user__username=user_name)
#     workers = Worker.objects.all()
#     customers = Customer.objects.all()
#     return render(request, 'employer_home.html', {'employer': employer, 'workers': workers, 'customers': customers})

def admin_emp(request):
    emp = Customer.objects.all()
    return render(request, 'admin_emp.html', {'emp': emp})

class worker_reg(SuccessMessageMixin, View):
    success_message = "User registered successfully"

    def get(self, request):
        job_types = TypeOfJobs.objects.all()
        return render(request, 'worker_reg.html', {'job_types': job_types})

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        user = User.objects.filter(username=username, email=email).first()

        if user:
            messages.error(request, "User with the same email/username already exists. Please try with another username/email")
            return redirect('worker_reg')
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request,"Invalid email address. Please provide a valid email.")
            return redirect('worker_reg')
        
        password = request.POST.get('password')
        if not self.is_valid_password(password):
            messages.error(request, "Invalid password. Password must contain atleast one Capital letter, small letter , number and special character.")
            return redirect('worker_reg')
        
        phone_no = request.POST.get('phone_no')
        if not self.phone_no_is_valid(phone_no):
            messages.error(request, "Invalid phone number. Please provide a valid 10-digit phone number.")
            return redirect('worker_reg')
        
        
        job_type_id = request.POST.get('job_type')
        job_type = TypeOfJobs.objects.filter(id=job_type_id).first()

        if job_type is None:
            messages.error(request, "Please select a valid job type.")
            return redirect('worker_reg')

        data = User.objects.create_user(
            username=username,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=email,
            password=request.POST.get('password')
        )
        

        data.save()

        customer = Customer(
            user=data,
            phone_no=request.POST.get('phone_no'),
            profile_pic=request.FILES.get('profile_pic'),
            location=request.POST.get('location'),
            user_type=request.POST.get('user_type')
        )
        customer.save()

        availability = {
            "Monday": request.POST.get('monday') == 'on',
            "Tuesday": request.POST.get('tuesday') == 'on',
            "Wednesday": request.POST.get('wednesday') == 'on',
            "Thursday": request.POST.get('thursday') == 'on',
            "Friday": request.POST.get('friday') == 'on',
            "Saturday": request.POST.get('saturday') == 'on',
            "Sunday": request.POST.get('sunday') == 'on',
        }
        availability = json.dumps(availability)

        worker = Worker(
            user=data,
            availability=availability,
            wage=request.POST.get('wage'),
            experience=request.POST.get('experience'),
            job_types=job_type
        )
        worker.save()

        messages.success(request, self.success_message)
        return redirect('user_login')
    def is_valid_password(self, password):
        password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W).{8,}"
        return bool(re.match(password_pattern, password))
    
    def phone_no_is_valid(self,phone_no):
        return phone_no.isdigit() and len(phone_no) == 10



def employer_hire(request, worker_id):
    customer = Customer.objects.all()
    worker = get_object_or_404(Worker, id=worker_id)
    workers= Worker.objects.all()
    return render(request, 'employer_hire.html', {'worker': worker,'customer':customer,'workers':workers})

def worker_home(request):
    worker = Worker.objects.get(user=request.user)
    hiring_requests = worker.hiring_requests.all()
    workers = Worker.objects.all()
    customers = Customer.objects.filter(user=request.user.id).first()
    print("User details ",request.user)
    print("prof pic ",customers.profile_pic.url)
    hiring_requests = Hiring.objects.filter(worker=worker, status = 'Pending')
    hiring_requests_count = hiring_requests.count()
    return render(request, 'worker_home.html', {'worker': worker, 'workers': workers, 'customers': customers, 'hiring_requests': hiring_requests, 'hiring_requests_count': hiring_requests_count})

def employer_home(request):
    workers = Worker.objects.all()
    customers = Customer.objects.all() 
    return render(request, 'employer_home.html', {'workers': workers,'customers':customers}) 

def negotiate(request, worker_id):
    worker = get_object_or_404(Worker, id=worker_id)
    print('worker is ',worker)
    try:
        employer = Employer.objects.get(user=request.user)
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
            messages = f'You have received a hiring request from {employer.user.username}.'
            message = f"You have received a hiring request from {employer.user.username} for wage ${wage}. Job duration is from {hiring.start_date} to {hiring.end_date}. Please log on to your account to accept/reject. Thank you "
            notification = Notification.objects.create(worker=worker, hiring=hiring, messages=messages,is_read = True)
            notification.save()
            subject = 'Hiring request from ' + employer.user.username
            message_body = 'Company: {}\nEmail: {}\nMessage: {}'.format(employer.user.username, employer.user.email, message)
            recipient = worker.user.email  

            send_mail(subject, message_body, settings.EMAIL_HOST_USER, [recipient],
                  fail_silently=False) 
            employer_home_url = reverse('employer_home')
            return HttpResponseRedirect(employer_home_url)
        else:
            return HttpResponse('No associated employer found for the current user.')
    except Employer.DoesNotExist:
        employer = None
    

def accept_hiring(request, hiring_id):
    hiring = get_object_or_404(Hiring, id=hiring_id)
    print('hiring id ',hiring_id)

    hiring.accept_request()
    worker = Worker.objects.get(user=request.user)
    message = f"{worker.user.username} have accepted hiring request. Job duration is from {hiring.start_date} to {hiring.end_date}. Thank you "
    subject = 'Hiring accepted by ' + worker.user.username
    message_body = 'Company: {}\nEmail: {}\nMessage: {}'.format(worker.user.username, worker.user.email, message)
    recipient = worker.user.email  

    send_mail(subject, message_body, settings.EMAIL_HOST_USER, [recipient],
                  fail_silently=False) 
    return redirect('worker_home')

def reject_hiring(request, hiring_id):
    hiring = get_object_or_404(Hiring, id=hiring_id)


    hiring.reject_request()
    return redirect('worker_home')


class set_availability(View):
    def get(self, request):
        worker = Worker.objects.get(user=request.user)
        availability = worker.availability
        return render(request, 'set_availability.html', {'worker': worker, 'availability': availability})

    def post(self, request):
        worker = Worker.objects.get(user=request.user)
        availability = worker.availability

        # Update the availability based on the form data
        availability = {
            "Monday": 'availability[Monday]' in request.POST,
            "Tuesday": 'availability[Tuesday]' in request.POST,
            "Wednesday": 'availability[Wednesday]' in request.POST,
            "Thursday": 'availability[Thursday]' in request.POST,
            "Friday": 'availability[Friday]' in request.POST,
            "Saturday": 'availability[Saturday]' in request.POST,
            "Sunday": 'availability[Sunday]' in request.POST,
        }

        worker.availability = availability
        worker.save()

        return redirect('worker_home')