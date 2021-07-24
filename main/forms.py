from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Person



class UserResgisterForm(UserCreationForm):
    email = forms.EmailField()
    Tel = forms.IntegerField()
    password1 = forms.PasswordInput()
    password2=forms.PasswordInput()
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'username',
                  'email','Tel', 'password1', 'password2']
