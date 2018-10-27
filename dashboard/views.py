from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django import forms

from api.models import Event, Society

User = get_user_model()

EVENT_FIELDS = ['name', 'start_day', 'end_day',
                'notes', 'image', 'contact_person', 'contact_number',
                'society', 'session', 'venue', 'registration_link']


class SignUpForm(UserCreationForm):
    society = forms.ModelChoiceField(
        queryset=Society.objects.all(), required=True)

    class Meta:
        model = User
        fields = ('email', 'name', 'phone', 'society',
                  'password1', 'password2', )


class SocietyAdminAccessMixin(UserPassesTestMixin):
    login_url = '/accounts/login/'

    def test_func(self):
        return self.request.user.role == "1"

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path(), self.login_url)


class HomeView(LoginRequiredMixin, SocietyAdminAccessMixin, ListView):
    model = Event
    template_name = "dashboard/home.html"

    def get_queryset(self):
        society = self.request.user.society
        return Event.objects.filter(society=society)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now()
        return context


class CreateEventView(LoginRequiredMixin, SocietyAdminAccessMixin, CreateView):
    model = Event
    template_name = "dashboard/create_event.html"
    fields = EVENT_FIELDS

    def form_valid(self, form):
        form.instance.creater = self.request.user
        return super().form_valid(form)


class UpdateEventView(LoginRequiredMixin, SocietyAdminAccessMixin, UpdateView):
    model = Event
    template_name = "dashboard/update_event.html"
    fields = EVENT_FIELDS


class CreateUserView(CreateView):
    template_name = "registration/signup.html"
    form_class = SignUpForm
    success_url = "/"

    def form_valid(self, form):
        form.instance.role = '1'
        return super().form_valid(form)
