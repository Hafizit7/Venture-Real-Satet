from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(validators =[RegexValidator('^[^\W\d_]+$',message="Only Alphabets")])
    password1 = forms.CharField(validators =[RegexValidator('^(\w+\d+|\d+\w+)+$',message="Only Alphabets and number")],label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(validators =[RegexValidator('^(\w+\d+|\d+\w+)+$',message="Only Alphabets and number")],label='Confirm-Password', widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username','password1','password2']


class UserUpdateForm(UserChangeForm):
    username = forms.CharField(validators =[RegexValidator('^[^\W\d_]+$',message="Only Alphabets")])
    class Meta:
        model = User
        fields = ['username',]
        # fields = '__all__' # all use mean show all field from django default dashboard system

class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(validators =[RegexValidator('^(\w+\d+|\d+\w+)+$',message="Only Alphabets and number")],label='Password', widget=forms.PasswordInput())
    new_password1 = forms.CharField(validators =[RegexValidator('^(\w+\d+|\d+\w+)+$',message="Only Alphabets and number")],label='Password', widget=forms.PasswordInput())
    new_password2 = forms.CharField(validators =[RegexValidator('^(\w+\d+|\d+\w+)+$',message="Only Alphabets and number")],label='Confirme-Password', widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = '__all__'
