from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.book, name='book'),
    path('register/', views.sign_up, name='register'),
    path('login/', views.sign_in, name='login'),
    ]