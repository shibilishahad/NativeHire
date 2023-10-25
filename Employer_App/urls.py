from django.urls import path
from . import views

app_name = 'Employer_App'

urlpatterns = [
    path('',views.employer_reg, name='employer_reg')
]
