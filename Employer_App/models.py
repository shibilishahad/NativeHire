from django.db import models
from NativeApp.models import User  # Import the User model from the NativeApp app

class Employer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)