from django.urls import path
from .views import (LoginView, CreateUserView, VerificationView,
                    EventListView, SocietyListView, EventView,
                    SocietyView, TagView)

urlpatterns = [
    path('auth/login', LoginView.as_view(), name="login"),
    path('auth/register', CreateUserView.as_view(), name="register"),
    path('auth/verify', VerificationView.as_view(), name="verify"),
    # path('create/society', CreateSocietyView.as_view(), name="society" ),
    # path('create/event', CreateEventView.as_view(), name="event" ),
    # path('create/tag', CreateTagView.as_view(), name="tag" ),
    path('event/<int:pk>', EventView.as_view(), name="event"),
    path('society/<int:pk>', SocietyView.as_view(), name="society"),
    path('tag/<int:pk>', TagView.as_view(), name="tag"),
    path('event', EventListView.as_view(), name="events"),
    path('society', SocietyListView.as_view(), name="societies"),
]
