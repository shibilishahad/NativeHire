from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from Admin_app.models import TypeOfJobs


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




class Employer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


# class JobType(models.Model):
#     job_types = models.ForeignKey(TypeOfJobs, on_delete=models.CASCADE)

dict ={
        "Monday": True,
        "Tuesday": True,
        "Wednesday": True,
        "Thursday": True,
        "Friday": True,
        "Saturday": True,
        "Sunday": True,
    }
class Worker(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # type = models.ForeignKey(Dummy, on_delete=models.CASCADE, null=True)
    hiring_requests = models.ManyToManyField('Hiring', related_name='workers')
    availability = models.JSONField(default=dict)
    wage = models.FloatField(null=True)
    experience = models.FloatField(null=True)
    country = models.ForeignKey('cities_light.Country', on_delete=models.SET_NULL, null=True, blank=True) 
    city = models.ForeignKey('cities_light.City', on_delete=models.SET_NULL, null=True, blank=True)
    # jobtype = models.JSONField()
    # type_of_jobs = models.ForeignKey(TypeOfJobs, on_delete=models.CASCADE)
    job_types = models.ForeignKey(TypeOfJobs, on_delete=models.CASCADE)


class HiringHistory(models.Model):
    employer_name = models.CharField(max_length=255)
    worker_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    cost = models.IntegerField()
    status = models.CharField(max_length=10)

    def __str__(self):
        return f"Hiring History ID {self.id} - {self.worker_name} hired by {self.employer_name}"


class Hiring(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    )
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE)
    worker = models.ForeignKey('Worker', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    hire_posting = models.DateTimeField(default=timezone.now)
    is_hired = models.BooleanField(default=False)
    cost = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def accept_request(self):
        self.status = 'Accepted'
        self.save()
        HiringHistory.objects.create(
            employer_name=self.employer.user.username,
            worker_name=self.worker.user.username,
            start_date=self.start_date,
            end_date=self.end_date,
            cost=self.cost,
            status='Accepted'
        )

    def reject_request(self):
        self.status = 'Rejected'
        self.save()

    def save(self, *args, **kwargs):
        if self.status == 'Accepted':
            self.is_hired = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Hiring ID {self.id} - {self.worker} hired by {self.employer}"

class Notification(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    hiring = models.ForeignKey(Hiring, on_delete=models.CASCADE)
    messages = models.TextField()
    is_read = models.BooleanField(default=False)

class RejectionReason(models.Model):
    hiring = models.ForeignKey('Hiring', on_delete=models.CASCADE)
    reason_text = models.TextField()