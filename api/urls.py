from django.urls import path
from .views import (LoginView, CreateUserView, VerificationView,
                    EventListView, SocietyListView, EventView,
                    SocietyView, TagEventsView, TagListView, SocietyEventsView,
                    UpcomingEventListView)

app_name = 'api'

urlpatterns = [
    path('auth/login', LoginView.as_view(), name="login"),
    path('auth/register', CreateUserView.as_view(), name="register"),
    path('auth/verify', VerificationView.as_view(), name="verify"),
    path('event/<int:pk>', EventView.as_view(), name="event"),
    path('society/<int:pk>', SocietyView.as_view(), name="society"),
    path('tag/<int:pk>/events', TagEventsView.as_view(), {"current" : False}, name="tag_events"),
    path('tag/<int:pk>/events/current', TagEventsView.as_view(), {"current" : True}, name="tag_events_current"),
    path('society/<int:pk>/events', SocietyEventsView.as_view(), {"current" : False}, name="society_events"),
    path('society/<int:pk>/events/current', SocietyEventsView.as_view(), {"current" : True}, name="society_events_current"),
    path('events/upcoming', UpcomingEventListView.as_view(), {"limit" : False}, name="events_upcoming"),
    path('events/upcoming/10', UpcomingEventListView.as_view(), {"limit" : True}, name="events_upcoming_10", ),
    path('events', EventListView.as_view(), name="events"),
    path('societys', SocietyListView.as_view(), name="societies"),
    path('tags', TagListView.as_view(), name="tags"),
]