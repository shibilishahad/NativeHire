import base64
import json
import re
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import *
from django.contrib.auth.models import User, auth
from django.contrib.auth.hashers import check_password
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.mime.image import MIMEImage
from .forms import CityFilterForm, CountryCityForm
from twilio.rest import Client
import string
import secrets
from django.core.exceptions import ValidationError
from django.db.models import Q
from .dependencies import is_valid_password, phone_no_is_valid
from django.core.files.base import ContentFile
from django.http import JsonResponse




def if_login(request,user):
    if request.user.is_authenticated:
        return None
    else:
        return redirect('user_login')
    


class base(View):
    def get(self, request):
        return render(request, 'base.html')

class home(View):
    def get(self, request):
        return render(request, 'homepage.html')
    
class AboutUs(View):
    def get(self,request):
        return render(request,"about_us.html")

class employer_reg(SuccessMessageMixin, View):
    success_message = "User registered successfully"

    def get(self, request):
        return render(request, 'employer_reg.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')

        existing_user = User.objects.filter(Q(username=username) | Q(email=email)).first()
        if existing_user:
            if existing_user.username == username:
                messages.error(request, "User with the same username already exists. Please try with another username.")
            else:
                messages.error(request, "User with the same email already exists. Please try with another email.")
            return redirect('employer_reg')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email address. Please provide a valid email.")
            return redirect('employer_reg')

        password = request.POST.get('password')
        c_password = request.POST.get('c_password')
        if password != c_password:
            messages.error(request, "Password and confirmation password do not match.")
            return redirect('employer_reg')

        phone_no = request.POST.get('phone_no')

        if not is_valid_password(password):
            messages.error(request, "Invalid password. Password must contain at least one capital letter, small letter, number, and special character.")
            return redirect('employer_reg')

        if not phone_no_is_valid(phone_no):
            messages.error(request, "Invalid phone number. Please provide a valid 10-digit phone number.")
            return redirect('employer_reg')
        
        data = User.objects.create_user(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            username=username,
            email=email,
            password=password
        )
        data.save()

        customer = Customer(user=data,
                            phone_no=phone_no,
                            profile_pic=request.FILES.get('profile_pic'),
                            location=request.POST.get('location'),
                            user_type="employer"
                            )
        customer.save()

        employer = Employer(user=data)
        employer.save()

        messages.success(request, self.success_message)

        self.send_welcome_email(employer)
        return redirect('user_login')
    
    def send_welcome_email(self, employer):
        # message = client.messages.create(
        #     body = f" Welcome {employer.user.first_name} {employer.user.last_name} ({employer.user.username}). ThankYou for choosing our APP NativeHire.",
        #     from_ = twilio_number,
        #     to = target_number
        # )
        subject = 'Welcome to NativeHire ' + employer.user.username
        from_email = settings.EMAIL_HOST_USER
        to_email = employer.user.email

        
        message = render_to_string('welcome_employer.html', {'employer': employer})
        plain_message = strip_tags(message)

        
        email = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])

        
        with open("static/images/logo-no-background.png", "rb") as f:
            logo_data = f.read()
            email_image = MIMEImage(logo_data)
            email_image.add_header('Content-ID', '<logo>')
            email.attach(email_image)

        
        email.attach_alternative(message, "text/html")

        
        email.send()
    


class user_login(View):
    def get(self, request):
        if request.user.is_authenticated:
            try:
                customer = Customer.objects.get(user=request.user)
                if customer.user_type == 'employer':
                    return redirect('employer_home')
                elif customer.user_type == 'worker':
                    return redirect('worker_home')
                elif request.user.is_staff:
                    return redirect('Admin_app:admin_home')
            except Customer.DoesNotExist:
                pass

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
                    # worker = Worker.objects.get(user=user)
                    # hiring_requests = worker.hiring_requests.all()
                    login(request, user)
                    # workers = Worker.objects.all()
                    # customers = Customer.objects.filter(user=request.user.id).first()
                    # hiring_requests = Hiring.objects.filter(worker=worker, status='Pending')
                    # hiring_requests_count = hiring_requests.count()
                    return redirect('worker_home')
                elif customer.user_type == 'employer':
                    login(request, user)
                    # employer = customer
                    # workers = Worker.objects.all()
                    # customers = Customer.objects.all() 
                    return redirect('employer_home') 
                else:
                    messages.error(request, "Sorry, user does not exist")
                    return redirect('user_login')
            else:
                messages.error(request, "Sorry, user does not exist")
                return redirect('user_login')
        else:
            messages.error(request, "Sorry, user does not exist")
            return redirect('user_login')

def logout(request):
    auth.logout(request)
    request.session.flush()
    return redirect('home')

def jobtype(request):
    return render(request, 'jobtype.html')


def employer_hire(request, worker_id):
    if if_login(request,request.user):
            return if_login(request, request.user)
    customer = Customer.objects.all()
    worker = Worker.objects.get(id=worker_id)
    workers = Worker.objects.all()
    return render(request, 'employer_hire.html', {'worker': worker, 'customer': customer, 'workers': workers})

def worker_home(request):
    if if_login(request,request.user):
            return if_login(request, request.user)
    worker = Worker.objects.filter(user=request.user).first()
    if worker:

        hiring_requests = worker.hiring_requests.all()

        workers = Worker.objects.all()
        customers = Customer.objects.filter(user=request.user).first()
        availability = worker.availability
        hiring_requests = Hiring.objects.filter(worker=worker, status='Pending')
        hiring_requests_count = hiring_requests.count()
        context = {'worker': worker, 'workers': workers, 'customers': customers, 
                'hiring_requests': hiring_requests,
                    'hiring_requests_count': hiring_requests_count,'availability':availability}
        return render(request, 'worker_home.html', context)
    else:
        messages.error(request, 'Unauthorized user')
        return redirect('user_login')


class WorkerUpdate(View):
    
    def get(self, request, update_id):
        if if_login(request,request.user):
            return if_login(request, request.user)
        worker = Worker.objects.filter(user = request.user).first()
        customer = Customer.objects.filter(user=update_id).first()
        job_type = TypeOfJobs.objects.all()
        return render(request, 'worker_update.html', {'customer': customer,'job_types':job_type,'worker':worker})

    def post(self, request, update_id):
        update_cus = Customer.objects.filter(id=update_id).first()
        worker = Worker.objects.get(user = request.user)
        
        wage = request.POST.get('wage')
        job_type_id = request.POST.get('job_types')  

        try:
            job_type_instance = TypeOfJobs.objects.get(id=job_type_id)
        except TypeOfJobs.DoesNotExist:
            messages.error(request, 'Invalid job type')
            return redirect('worker_home')

        worker.job_types = job_type_instance
        worker.wage = wage
        worker.save()

        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')

        update_cus.location = request.POST.get('location')
        update_cus.phone_no = request.POST.get('phone_no')
        print('dsal',update_cus.phone_no)
        print('saddsa',update_cus.location)

        new_password = request.POST.get('password')
        if new_password:
            user.set_password(new_password)


        # old_profile_pic = update_cus.profile_pic
        # new_profile_pic = request.FILES.get('profile_pic')
        
        # update_cus = Customer.objects.filter(id=update_id).first()

         # Get the base64 data from the request
        base64_image = request.POST.get('cropped_image') 

        if base64_image and ';base64,' in base64_image:
            format, imgstr = base64_image.split(';base64,')
            if re.match('^[A-Za-z0-9+/]+[=]{0,2}$', imgstr): 
              
               ext = format.split('/')[-1] 
               data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext) 

               update_cus.profile_pic = data 
        update_cus.save()
        user.save()
        
        return redirect('worker_home')

 



def employer_home(request):
    if if_login(request,request.user):
            return if_login(request, request.user)
    employer = Employer.objects.filter(user=request.user).first()
    if employer:
        workers = Worker.objects.all()
        city_filter_form = CityFilterForm(request.GET)
        selected_city = None
        city_search_query = request.GET.get('city_search_query', '')

        if city_filter_form.is_valid():
            selected_city = city_filter_form.cleaned_data['city']
            if selected_city:
                workers = workers.filter(city=selected_city)
        if city_search_query:
            workers = workers.filter(city__name__icontains=city_search_query)
        worker = Worker.objects.all()
        customers = Customer.objects.all()
        customer = Customer.objects.get(user=request.user)
        employer = Employer.objects.get(user=request.user)
        hiring_requests = Hiring.objects.filter(employer=employer)
        return render(request, 'employer_home.html', {'workers': workers, 'customers': customers,'employer':employer,'customer':customer,'worker':worker,'city_filter_form': city_filter_form,
            'selected_city': selected_city,'hiring_requests':hiring_requests,'city_search_query': city_search_query,})
    
    else:
        messages.error(request, 'Unauthorized user')
        return redirect('user_login')



class EmployerUpdate(View):
    def get(self,request,update_id):
        if if_login(request,request.user):
            return if_login(request,request.user)
        customer = Customer.objects.filter(user=update_id).first()
        if customer:
            return render(request,'employer_update.html',{'customer':customer})
        else:
            messages.error(request, 'Unauthorized user')
            return redirect('user_login')
    
    def post(self,request,update_id):   
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')

        update_employer = Customer.objects.filter(user=update_id).first()
        update_employer.location = request.POST.get('location')
        update_employer.phone_no = request.POST.get('phone_no')

        
        base64_image = request.POST.get('cropped_image') 

        if base64_image and ';base64,' in base64_image:
            format, imgstr = base64_image.split(';base64,')
            if re.match('^[A-Za-z0-9+/]+[=]{0,2}$', imgstr): 
              
               ext = format.split('/')[-1] 
               data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext) 

               update_employer.profile_pic = data 

        update_employer.save()
        user.save()

        return redirect('employer_home')
    
class PasswordChangeEmp(View):
    def get(self, request):
        employer = Employer.objects.filter(user=request.user)
        return render(request, 'password_change_emp.html', {'employer': employer})

    def post(self, request):
        user = request.user
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        c_password = request.POST.get('c_password')

        if check_password(current_password, user.password):
            if current_password != new_password:
                if new_password == c_password:
                    user.set_password(new_password)
                    user.save()
                    return redirect('employer_home')
                else:
                    messages.error(request, 'New password and Confirm password do not match.')
            else:
                messages.error(request, 'Current password and new password is same. Please use another password.')
        else:
            messages.error(request, 'Current password is incorrect.')
        return redirect('password_change_emp')


    
class PasswordChange(View):
    def get(self, request):
        worker = Worker.objects.filter(user=request.user)
        return render(request, 'change_password.html', {'worker': worker})

    def post(self, request):
        user = request.user
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        c_password = request.POST.get('c_password')

        if check_password(current_password, user.password):
            if current_password != new_password:
                if new_password == c_password:
                    user.set_password(new_password)
                    user.save()
                    return redirect('worker_home')
                else:
                    messages.error(request, 'New password and Confirm password do not match.')
            else:
                messages.error(request, 'Current and new password is same. Please use another password.')
        else:
            messages.error(request, 'Current password is incorrect.')
        return redirect('password_change')



def negotiate(request, worker_id):
    if if_login(request,request.user):
            return if_login(request, request.user)
    worker = get_object_or_404(Worker, id=worker_id)
    try:
        employer = Employer.objects.get(user=request.user)
        if employer:
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            total_wage = float(request.POST.get('total_wage'))
            hiring = Hiring.objects.create(
                employer=employer,
                worker=worker,
                start_date=start_date,
                end_date=end_date,
                cost=total_wage
            )
            hiring.save()
            notification = Notification.objects.create(worker=worker, hiring=hiring, messages=f"You have received a hiring request from {employer.user.username} for total wage ₹{total_wage}. Job duration is from {hiring.start_date} to {hiring.end_date}. ",is_read = True)
            notification.save()
            message = render_to_string('hiring_sent.html',{'employer':employer,'worker':worker,'hiring':hiring})
            plain_message = strip_tags(message)

            subject = 'Hiring request from '+ employer.user.first_name +  employer.user.last_name
            from_email = settings.EMAIL_HOST_USER
            to_email = employer.user.email

            email = EmailMultiAlternatives(subject,plain_message,from_email,[to_email])
            with open("static/images/logo-no-background.png","rb") as f:
                logo_data = f.read()
                email_image = MIMEImage(logo_data)
                email_image.add_header('Content-ID', '<logo>')
                email.attach(email_image)
            email.send()
            return redirect('employer_home')
        
        else:
            messages.error(request, 'No associated employer found for the current user.')
            return redirect('user_login')
            
    except Employer.DoesNotExist:
        employer = None

def accept_hiring(request, hiring_id):
    if if_login(request,request.user):
            return if_login(request, request.user)
    hiring = get_object_or_404(Hiring, id=hiring_id)

    hiring.accept_request()
    worker = Worker.objects.get(user=request.user)
    message = render_to_string('accept_email.html',{'worker':worker,'hiring':hiring})
    plain_message = strip_tags(message)

    subject = 'Hiring accepted by ' + worker.user.username
    from_email = settings.EMAIL_HOST_USER
    to_email = worker.user.email
    
    email = EmailMultiAlternatives(subject,plain_message,from_email,[to_email])
    with open("static/images/logo-no-background.png","rb") as f:
        logo_data = f.read()
        email_image = MIMEImage(logo_data)
        email_image.add_header('Content-ID', '<logo>')
        email.attach(email_image)
    email.send()
    return redirect('worker_home')

def reject_hiring(request, hiring_id):
    if if_login(request, request.user):
        return if_login(request, request.user)
    
    hiring = get_object_or_404(Hiring, id=hiring_id)
    
    if request.method == 'POST':
        reason_text = request.POST.get('reason_text')
        
        if reason_text:
            RejectionReason.objects.create(hiring=hiring, reason_text=reason_text)
            
            hiring.reject_request()
            
            worker = Worker.objects.get(user=request.user)
            message = render_to_string('reject_email.html', {'worker': worker, 'hiring': hiring, 'reason_text': reason_text})
            plain_message = strip_tags(message)
            
            subject = 'Hiring rejected by ' + worker.user.username
            from_email = settings.EMAIL_HOST_USER
            to_email = worker.user.email
            
            email = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])
            with open("static/images/logo-no-background.png", "rb") as f:
                logo_data = f.read()
                email_image = MIMEImage(logo_data)
                email_image.add_header('Content-ID', '<logo>')
                email.attach(email_image)
            email.send()
            
            return redirect('worker_home')

    context = {'hiring': hiring}
    return render(request, 'reject_hiring.html', context)

class set_availability(View):
    def get(self, request):
        if if_login(request,request.user):
            return if_login(request, request.user)
        worker = Worker.objects.get(user=request.user)
        availability = worker.availability
        return render(request, 'set_availability.html', {'worker': worker, 'availability': availability})

    def post(self, request):
        worker = Worker.objects.get(user=request.user)
        availability = worker.availability

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



class worker_reg(View):
    success_message = "User registered successfully"

    def get(self, request):
        job_types = TypeOfJobs.objects.all()
        country_city_form = CountryCityForm()
        return render(request, 'worker_reg.html', {'job_types': job_types,'country_city_form': country_city_form})

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        user_by_username = User.objects.filter(username=username).first()
        user_by_email = User.objects.filter(email=email).first()

        if user_by_username or user_by_email:
            messages.error(request, "User with the same email/username already exists. Please try with another username/email")
            return redirect('worker_reg')
        
        try:
            validate_email(email)
        except:
            messages.error(request, "Invalid email address. Please provide a valid email.")
            return redirect('worker_reg')
        
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')
        if password != c_password:
            messages.error(request, "Password and confirmation password do not match.")
            return redirect('worker_reg')
        
        phone_no = request.POST.get('phone_no')

        if not is_valid_password(password):
            messages.error(request, "Invalid password. Password must contain at least one Capital letter, small letter, number, and special character.")
            return redirect('worker_reg')

        if not phone_no_is_valid(phone_no):
            messages.error(request, "Invalid phone number. Please provide a valid phone number.")
            return redirect('worker_reg')


        job_type = TypeOfJobs.objects.filter(id=request.POST.get('job_type')).first()

        if job_type is None:
            messages.error(request, "Please select a valid job type.")
            return redirect('worker_reg')

        data = User.objects.create_user(
            username=username,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=email,
            password=password
        )

        data.save()

        customer = Customer(
                user=data,
                phone_no=request.POST.get('phone_no'),
                profile_pic=request.FILES.get('profile_pic'),
                location=request.POST.get('location'),
                user_type="worker",
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

        country_city_form = CountryCityForm(request.POST)

        if country_city_form.is_valid():
            selected_country = country_city_form.cleaned_data['country']
            selected_city = country_city_form.cleaned_data['city']

            worker = Worker(
                user=data,
                availability=availability,
                wage=request.POST.get('wage'),
                experience=request.POST.get('experience'),
                job_types=job_type,
                country=selected_country,
                city=selected_city,
            )
            worker.save()
            messages.success(request, self.success_message)
            self.send_welcome_email(worker)
        else:
            messages.error(request, "Invalid country or city selection. Please try again.")
            return redirect('worker_reg')

        return redirect('user_login')
    
    def send_welcome_email(self, worker):

        # client = Client(account_sid,auth_token)
        # message = client.messages.create(
        #     body = f" Welcome {worker.user.first_name} {worker.user.last_name} ({worker.user.username}), ThankYou for choosing our APP NativeHire.",
        #     from_ = twilio_number,
        #     to = target_number
        # )
        subject = 'Welcome to NativeHire ' + worker.user.username
        from_email = settings.EMAIL_HOST_USER
        to_email = worker.user.email

        
        message = render_to_string('welcome_worker.html', {'worker': worker})
        plain_message = strip_tags(message)

        
        email = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])

        
        with open("static/images/logo-no-background.png", "rb") as f:
            logo_data = f.read()
            email_image = MIMEImage(logo_data)
            email_image.add_header('Content-ID', '<logo>')
            email.attach(email_image)

        
        email.attach_alternative(message, "text/html")

        
        email.send()


    


# account_sid = 'AC08b2b61f2aff54d504918f7622023e7f'
# auth_token = 'c4b2830047252f025a002bfa82cab346'

# twilio_number = '+12563644781'
# target_number = '+918547278372'

# client = Client(account_sid,auth_token)

# message = client.messages.create(
#     body = " This is a test message",
#     from_ = twilio_number,
#     to = target_number
# )




def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits

    password = ''.join(secrets.choice(characters) for o in range(length))

    return password

 
class ResetPass(View):
    def get(self,request):
        return render(request,'reset_pass.html')
    
    def post(self,request):
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            new_pass = generate_random_password()
            user.set_password(new_pass)
            user.save()
            message = render_to_string('reset_pass_email.html',{'new_pass':new_pass,'email':email})
            plain_message = strip_tags(message)

            subject = 'NativeHire Reset password'
            from_email = settings.EMAIL_HOST_USER
            to_email = email

            email = EmailMultiAlternatives(subject,plain_message, from_email, [to_email])
            with open("static/images/logo-no-background.png","rb") as f:
                logo_data = f.read()
                email_image = MIMEImage(logo_data)
                email_image.add_header('Content-ID', '<logo>')
                email.attach(email_image)
            email.send()

            return redirect('user_login')
        else:
            messages.error(request, 'No such email registered')
