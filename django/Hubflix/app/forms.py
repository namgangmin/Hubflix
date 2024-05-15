from django import forms
from .models import Contents, Users
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class MovieForm(forms.ModelForm):
    class Meta: 
        model = Contents
        fields = '__all__'
            #['title', 'poster_path','contents_id']
