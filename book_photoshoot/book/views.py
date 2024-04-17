from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, RegisterForm, BookingForm
import requests
import json


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
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('book')
        else:
            return render(request, 'register.html', {'form': form})


def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Hi {username.title()}, welcome back!')
                return redirect('book')

        # form is not valid or user is not authenticated
        messages.error(request, f'Invalid username or password')
        return render(request, 'login.html', {'form': form})


def book(request):
    return render(request, 'book/book.html', {})


def booking(request):
    if request.method == 'GET':
        apidata = requests.get("http://127.0.0.1:5000/books/free")
        free_book = json.loads(apidata.content)
        free_book_to_resp_ekb = []
        free_book_to_resp_ufa = []
        for book in free_book:
            if book['fields']['city'] == "Уфа":
                free_book_to_resp_ufa.append(Book(get_date(book['fields']['date']), book['fields']['time'][:5]))
            elif book['fields']['city'] == "Екатеринбург":
                free_book_to_resp_ekb.append(Book(get_date(book['fields']['date']), book['fields']['time'][:5]))
        return render(request, 'book/booking.html', {'books_ufa': free_book_to_resp_ufa, 'books_ekb': free_book_to_resp_ekb})

def get_date(date):
    month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
           'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    date_list = date.split('-')
    return (date_list[2] + ' ' +
        month_list[int(date_list[1]) - 1])

def contacts(request):
    return render(request, 'book/contacts.html', {})


def book_form(request):
    if request.method == 'GET':
        form = BookingForm
        return render(request, 'book_form.html', {'form': form})

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            return redirect('booking')
        else:
            return render(request, 'book_form.html', {'form': form})


# def api_mock(request):
#     if request.method == 'GET':
#         apidata = requests.get("http://127.0.0.1:5000/users/")
#         users = json.loads(apidata.content)
#         users_to_resp = []
#         for u in users:
#             users_to_resp.append(User(u['fields']['first_name'], u['fields']['last_name']))
#         return render(request, 'book/mock_cum.html', {'users': users_to_resp})

class Book():
    def __init__(self, date, time):
        self.date = date
        self.time = time
