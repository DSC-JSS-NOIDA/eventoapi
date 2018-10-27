from django.urls import path, include
from .views import HomeView, CreateEventView

app_name = 'dashboard'

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('create/event', CreateEventView.as_view(), name="create_event"),
    path('accounts/', include('django.contrib.auth.urls')),
]
