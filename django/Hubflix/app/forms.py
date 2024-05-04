from django import forms
from .models import Contents

class MovieForm(forms.ModelForm):
    class Meta: 
        model = Contents
        fields = ['title', 'poster_path']