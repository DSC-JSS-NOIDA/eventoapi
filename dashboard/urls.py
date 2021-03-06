from django.urls import path, include
from .views import HomeView, UpdateEventView, CreateUserView, CreateEventView, SendNotificationView, NotificationSuccessView

app_name = 'dashboard'

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('event/create', CreateEventView.as_view(), name="create_event"),
    path('event/update/<int:pk>', UpdateEventView.as_view(), name="update_event"),
    path('notification', SendNotificationView.as_view(), name="notification"),
    path('notification/success', NotificationSuccessView.as_view(),
         name="success_notification"),
    path('accounts/signup', CreateUserView.as_view(), name="signup"),
]
