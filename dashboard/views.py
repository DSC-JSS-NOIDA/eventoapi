
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.utils import timezone

from api.models import Event, Society
from .forms import SignUpForm, EventForm, NotificationForm


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
        return Event.objects.filter(society=society).order_by('-start_day')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now()
        return context


class CreateEventView(LoginRequiredMixin, SocietyAdminAccessMixin, CreateView):
    model = Event
    template_name = "dashboard/create_event.html"
    form_class = EventForm
    success_url = "/"

    def form_valid(self, form):
        form.instance.creater = self.request.user
        form.instance.society = self.request.user.society
        return super().form_valid(form)


class UpdateEventView(LoginRequiredMixin, SocietyAdminAccessMixin, UpdateView):
    model = Event
    template_name = "dashboard/update_event.html"
    form_class = EventForm
    success_url = "/"


class CreateUserView(CreateView):
    template_name = "registration/signup.html"
    form_class = SignUpForm
    success_url = "/"

    def form_valid(self, form):
        form.instance.role = '1'
        return super().form_valid(form)


class SendNotificationView(LoginRequiredMixin, SocietyAdminAccessMixin, FormView):
    template_name = "dashboard/notification.html"
    form_class = NotificationForm
    success_url = "/notification/success"

    def form_valid(self, form):
        # form.send_notification()
        return super().form_valid(form)


class NotificationSuccessView(TemplateView):
    template_name = "dashboard/not_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
