from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils import timezone
from django.contrib.auth.models import User

class Customer(models.Model):
    USER_TYPES = (
        ('employer', 'employer'),
        ('worker', 'worker')
    )   
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=10)
    profile_pic = models.ImageField(upload_to='pics', blank=True)
    location = models.TextField(max_length=250)
    user_type = models.CharField(max_length=8, choices=USER_TYPES)
    def __str__(self):
        return self.user.username
        
class Type(models.Model):
    id = models.AutoField(primary_key=True)
    job_type = models.CharField(max_length=50)

class Availability(models.Model):
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)

class Employer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Worker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True)
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE, null=True)
    wage = models.IntegerField(null=True)
    experience = models.IntegerField(null=True)

class Hiring(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    hire_posting = models.DateTimeField(default=timezone.now)
    is_hired = models.BooleanField(default=False)
    cost = models.IntegerField()
