from .models import User
from django import forms
from .models import Employer


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = '__all__'
