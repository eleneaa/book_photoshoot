from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Book


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class BookingForm(forms.Form):
    user = forms.CharField(label='Имя', max_length=25)
    number = forms.CharField(label='Номер телефона\ник телеграм', max_length=25)
    description = forms.CharField(label='Описание', max_length=200)

    class Meta:
        model = Book
        fields = ['user', 'number', 'description']
