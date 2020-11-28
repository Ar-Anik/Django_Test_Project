from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class reg_form(UserCreationForm) :
    class Meta :
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class Profile_form(forms.ModelForm) :
    class Meta :
        model = Profile
        fields = ('picture', 'address', 'contact_num')