from django.forms import ModelForm, TextInput
from .models import City

class Cityform(ModelForm):
    class Meta:
        model= City
        fields = ['name']
        widgets= {'name':TextInput(attrs={'class': 'input', 'placeholder':'Choose a City'})}