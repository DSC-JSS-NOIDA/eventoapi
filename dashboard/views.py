from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django import forms

from api.models import Event, Society

User = get_user_model()

EVENT_FIELDS = ['name', 'start_day', 'end_day',
                'notes', 'image', 'contact_person', 'contact_number',
                'society', 'session', 'venue', 'registration_link']


class SignUpForm(UserCreationForm):
    society = forms.ModelChoiceField(
        queryset=Society.objects.all(), required=True)

    society.widget.attrs.update({'class': 'select'})

    class Meta:
        model = User
        fields = ('name', 'email', 'phone', 'society',
                  'password1', 'password2', )


class HomeView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    # redirect_field_name = 'redirect_to'

    model = Event
    template_name = "dashboard/home.html"

    def get_queryset(self):
        society = self.request.user.society
        return Event.objects.filter(society=society)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now()
        return context


class CreateEventView(LoginRequiredMixin, CreateView):
    model = Event
    template_name = "dashboard/create_event.html"
    fields = EVENT_FIELDS


class UpdateEventView(LoginRequiredMixin, UpdateView):
    model = Event
    template_name = "dashboard/update_event.html"
    fields = EVENT_FIELDS


class CreateUserView(CreateView):
    template_name = "registration/signup.html"
    form_class = SignUpForm
