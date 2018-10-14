from django.contrib import admin
from django.urls import path

from .views import LoginView, CreateUserView, VerificationView

urlpatterns = [
    path('auth/login', LoginView.as_view(), name="login" ),
    path('auth/register', CreateUserView.as_view(), name="register" ),
    path('auth/verify', VerificationView.as_view(), name="verify" ),
]