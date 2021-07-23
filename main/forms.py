from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

from phonenumber_field.formfields import PhoneNumberField

from .models import Person



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    Tel = PhoneNumberField(label=_('Phone Number'))
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'username',
                  'email','Tel', 'password1', 'password2']