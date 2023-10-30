from django import forms

from Admin_app.models import TypeOfJobs

class TypeForm(forms.ModelForm):
    class Meta:
        model = TypeOfJobs
        fields = ['type_of_jobs']