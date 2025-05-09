from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Movie, Review


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields=["name","desc","year","img"]

class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
