from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import fields
from django.utils.translation import gettext as _

from phonenumber_field.formfields import PhoneNumberField

from .models import City, Person,Product,Category, Product_Image



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    Tel = PhoneNumberField(label=_('Phone Number'))
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'username',
                  'email','Tel', 'password1', 'password2']


class AddProductForm(forms.ModelForm):
    c=[
       (0,'Sale'),
       (1,'Request'),
    ]
    
    category = forms.ModelChoiceField(queryset=Category.objects.all(),empty_label=None,)
    city = forms.ModelChoiceField(queryset=City.objects.all(),empty_label=None)
    name = forms.CharField()
    price = forms.FloatField()
    TS = forms.ChoiceField(choices=c)

    class Meta:
        model = Product
        fields = ['name','category','city','price','TS']

class AddImageForm(forms.ModelForm):
    class Meta:
        model = Product_Image
        fields = ['image']