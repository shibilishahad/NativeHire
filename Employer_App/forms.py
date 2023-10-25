from django import forms
from Employer_App.models import Employer
from NativeApp.models import User

class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = '__all__'
