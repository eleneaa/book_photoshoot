from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.book, name='book'),
    path('register/', views.sign_up, name='register'),
    path('login/', views.sign_in, name='login'),
    path('booking/', views.booking, name='booking'),
    path('contacts/', views.contacts, name='contacts'),
    path('booking/form/<int:book_id>/', views.book_form, name='form'),
    path('booking/form/', views.book_form, name='form'),
    path('profile/', views.profile, name='profile'),
    path('profile/cancel/<int:book_id>/', views.cancel_book, name='cancel'),
    path('profile/cancel/', views.cancel_book, name='cancel'),
    path('register/<str:username>/', views.confirm_profile, name='confirm_profile'),
    path('price/', views.price, name='price'),
    #path('profile/pay', views.pay, name='pay'),
    path('profile/pay/sucsess', views.success_pay, name='success'),
    path('profile/pay/fail', views.fail_pay, name='fail'),
    path('profile/pay/result', views.result_pay, name='result'),
]