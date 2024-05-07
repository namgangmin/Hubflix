from django import forms
from .models import Contents, Users
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class MovieForm(forms.ModelForm):
    class Meta: 
        model = Contents
        fields = ['title', 'poster_path']
