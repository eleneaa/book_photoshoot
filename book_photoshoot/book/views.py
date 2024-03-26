from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, RegisterForm, BookingForm


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
    return render(request, 'book/booking.html', {})


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