from django.contrib import admin
from django.urls import path

from .views import login, register

urlpatterns = [
    path('auth/login', login, name="login" ),
    path('auth/register', register, name="register" ),
]