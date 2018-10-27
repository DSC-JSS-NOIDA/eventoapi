from django.urls import path
from .views import (LoginView, CreateUserView, VerificationView,
                    EventListView, SocietyListView, EventView,
                    SocietyView, TagEventsView, TagListView, SocietyEventsView,
                    UpcomingEventListView, PastEventListView, ResendOTPView)

app_name = 'api'

urlpatterns = [
    path('auth/login', LoginView.as_view(), name="login"),
    path('auth/register', CreateUserView.as_view(), name="register"),
    path('auth/verify', VerificationView.as_view(), name="verify"),
    path('auth/resend', ResendOTPView.as_view(), name="resend"),
    path('event/<int:pk>', EventView.as_view(), name="event"),
    path('society/<int:pk>', SocietyView.as_view(), name="society"),
    path('tag/<int:pk>/events', TagEventsView.as_view(),
         {"current": False}, name="tag_events"),
    path('tag/<int:pk>/events/current', TagEventsView.as_view(),
         {"current": True}, name="tag_events_current"),
    path('society/<int:pk>/events', SocietyEventsView.as_view(),
         {"period": ""}, name="society_events"),
    path('society/<int:pk>/events/current', SocietyEventsView.as_view(),
         {"period": "current"}, name="society_events_current"),
    path('society/<int:pk>/events/past', SocietyEventsView.as_view(),
         {"period": "past"}, name="society_events_past"),
    path('society/<int:pk>/events/upcoming', SocietyEventsView.as_view(),
         {"period": "upcoming"}, name="society_events_upcoming"),
    path('events/past', PastEventListView.as_view(), name="events_past"),
    path('events/upcoming', UpcomingEventListView.as_view(),
         {"limit": None}, name="events_upcoming"),
    path('events/upcoming/<int:limit>',
         UpcomingEventListView.as_view(), name="events_upcoming_limit"),
    path('events', EventListView.as_view(), name="events"),
    path('societys', SocietyListView.as_view(), name="societies"),
    path('tags', TagListView.as_view(), name="tags"),
]
