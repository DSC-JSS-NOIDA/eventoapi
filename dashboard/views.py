from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from api.models import Event

User = get_user_model()

class HomeView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    # redirect_field_name = 'redirect_to'

    model = Event
    template_name = "dashboard/home.html"

    def get_queryset(self):
        society = self.request.user.society
        return Event.objects.filter(society=society)

class CreateEventView(LoginRequiredMixin, CreateView):
    model = Event
    template_name = "dashboard/create_event.html"
    fields = ['name', 'start_day', 'end_day',
                'notes', 'image', 'contact_person', 'contact_phone',
                'society', 'session']