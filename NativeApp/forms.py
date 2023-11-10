from django import forms
from cities_light.models import Country, City

class CountryCityForm(forms.Form):
    country = forms.ModelChoiceField(queryset=Country.objects.filter(name='India'), empty_label="Select a country")
    
    city = forms.ModelChoiceField(queryset=City.objects.filter(country__name='India'), empty_label="Select a city")

class CityFilterForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.filter(country__name='India'), empty_label="All Cities")    