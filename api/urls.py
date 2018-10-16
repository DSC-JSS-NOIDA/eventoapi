from django.contrib import admin
from django.urls import path

from .views import LoginView, CreateUserView, VerificationView, CreateSocietyView, CreateTagView, CreateEventView

urlpatterns = [
    path('auth/login', LoginView.as_view(), name="login" ),
    path('auth/register', CreateUserView.as_view(), name="register" ),
    path('auth/verify', VerificationView.as_view(), name="verify" ),
    path('create/society', CreateSocietyView.as_view(), name="society" ),
    # path('create/event', CreateEventView.as_view(), name="event" ),
    path('create/tag', CreateTagView.as_view(), name="tag" ),
]