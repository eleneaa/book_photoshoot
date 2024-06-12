import random
from base64 import b64encode, b64decode

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from requests.auth import HTTPBasicAuth
from .constant import *
from .forms import LoginForm, RegisterForm, BookingForm, ConfirmForm
import requests
import json
from django.shortcuts import render
from django.http import HttpResponse


def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            response = send_data_to_api_server(
                form.cleaned_data['username'],
                form.cleaned_data['email'],
                form.cleaned_data['password1']
            )
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.is_active = False
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('confirm_profile',username=user.username)
        else:
            return render(request, 'register.html', {'form': form})


def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        data = {
            'username': username,
            'password': password
        }
        json_data = json.dumps(data)
        api_url = SIGN_IN_URL
        response = requests.post(api_url, data=json_data, headers={'Content-Type': 'application/json'})
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Hi {username.title()}, welcome back!')
                return redirect('profile')

        # form is not valid or user is not authenticated
        messages.error(request, f'Invalid username or password')
        return render(request, 'login.html', {'form': form})


def book(request):
    return render(request, 'book/book.html', {})


def profile(request):
    if request.method == 'GET':
        apidata_occupied = requests.get(OCCUPIED_BOOK_URL)
        apidata_confirmed = requests.get(CONFIRMED_BOOK_URL)
        apidata_last = requests.get(LAST_BOOK_URL)
        books_occupied = json.loads(apidata_occupied.content)
        books_confirmed = json.loads(apidata_confirmed.content)
        books_last = json.loads(apidata_last.content)
        user_book_occupied = []
        user_book_confirmed = []
        user_book_last = []
        user = request.user.id
        for book in books_occupied:
            if book['fields']['user'] == user:
                user_book_occupied.append(Book(get_date(book['fields']['date']), book['fields']['time'][:5],
                                               book['fields']['url'], book['pk']))
        for book in books_confirmed:
            if book['fields']['user'] == user:
                user_book_confirmed.append(Book(get_date(book['fields']['date']), book['fields']['time'][:5],
                                                book['fields']['url'], book['pk']))
        for book in books_last:
            if book['fields']['user'] == user:
                user_book_last.append(Book(get_date(book['fields']['date']), book['fields']['time'][:5],
                                           book['fields']['url'], book['pk']))
        return render(request, 'book/user_profile.html',
                      dict(user_books_last=user_book_last, user_books_confirmed=user_book_confirmed,
                           user_books_occupied=user_book_occupied, user=request.user))


def booking(request):
    if request.method == 'GET':
        apidata = requests.get(FREE_BOOK_URL)
        free_book = json.loads(apidata.content)
        free_book_to_resp_ekb = []
        free_book_to_resp_ufa = []
        for book in free_book:
            if book['fields']['city'] == "Уфа":
                free_book_to_resp_ufa.append(Book(get_date(book['fields']['date']), book['fields']['time'][:5],
                                                  book['fields']['url'], book['pk']))
            elif book['fields']['city'] == "Екатеринбург":
                free_book_to_resp_ekb.append(Book(get_date(book['fields']['date']), book['fields']['time'][:5],
                                                  book['fields']['url'], book['pk']))
        return render(request, 'book/booking.html',
                      {'books_ufa': free_book_to_resp_ufa, 'books_ekb': free_book_to_resp_ekb})


def get_date(date):
    month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                  'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    date_list = date.split('-')
    return (date_list[2] + ' ' +
            month_list[int(date_list[1]) - 1])


def contacts(request):
    return render(request, 'book/contacts.html', {})


def book_form(request, book_id):
    if request.method == 'GET':
        form = BookingForm
        return render(request, 'book_form.html', {'form': form})

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            number = request.POST.get('number')
            description = request.POST.get('description')
            username = request.user.id
            data = {
                'number': number,
                'description': description,
                'book_id': book_id,
                'username': username
            }
            json_data = json.dumps(data)
            api_url = OCCUPIED_BOOK_URL
            response = requests.post(api_url, data=json_data, headers={'Content-Type': 'application/json'})
            return redirect('booking')
        else:
            return render(request, 'book_form.html', {'form': form})


def send_data_to_api_server(username, email, password):
    url = SIGN_UP_URL
    headers = {'content-type': 'application/json'}
    api_username = 'admin'
    api_password = 'admin'
    payload = {
        "method": "register_user",
        "params": [username, email, password],
        "username": username,
        "email": email,
        "password": password,
        "jsonrpc": "2.0",
        "id": 0,
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers,
        auth=HTTPBasicAuth(api_username, api_password)  # Аутентификация
    )
    return response.json()


def cancel_book(request, book_id):
    if request.method == 'GET':
        url = ALL_BOOK_URL
        apidata = dict(id=book_id)
        json_data = json.dumps(apidata)
        response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'})
        return redirect('profile')


class Book():
    def __init__(self, date, time, url, pk):
        self.date = date
        self.time = time
        self.url = url
        self.pk = pk


def confirm_profile(request,username):
    user = User.objects.filter(username=username)[0]
    message = str(user.pk) + '/' + user.username
    message_bytes = message.encode('ascii')
    base64_bytes = b64encode(message_bytes)
    conf_code = base64_bytes.decode('ascii')
    if request.method == 'GET':
        form = ConfirmForm()
        send_mail(subject="Код подтверждения аккаунта",
                  message="Ваш код подтверждения: " + conf_code,
                  from_email = 'ltbdadchg@yandex.ru',
                  recipient_list=[user.email],
                  fail_silently=False)
        return render(request, 'confirmform.html', {'form': form})
    if request.method == 'POST':
        form = ConfirmForm(request.POST)
        if form.is_valid():
            code = request.POST.get('code')
            base64_message = code
            base64_bytes = base64_message.encode('ascii')
            message_bytes = b64decode(base64_bytes)
            message = message_bytes.decode('ascii').split('/')
            if message[0] == str(user.pk) and message[1] == user.username:
                user.is_active = True
                user.save()
                return redirect('profile')
            else:
                return render(request, 'confirmform.html', {'form': form})
        else:
            return render(request, 'confirmform.html', {'form': form})


