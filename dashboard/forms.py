
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django import forms
from api.models import Event, Society
from .firebase import send_notification_to_user, send_notification_to_all
User = get_user_model()


EVENT_FIELDS = ['name', 'start_day', 'end_day',
                'notes', 'image', 'contact_person', 'contact_number',
                'session', 'venue', 'registration_link']


class SignUpForm(UserCreationForm):
    society = forms.ModelChoiceField(
        queryset=Society.objects.all(), required=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'phone', 'society',
                  'password1', 'password2']


class EventForm(forms.ModelForm):
    start_day = forms.SplitDateTimeField(
        widget=forms.SplitDateTimeWidget(
            date_attrs={'type': 'date', 'class': 'form-control'},
            time_attrs={'type': 'time', 'class': 'form-control'}
        )
    )
    end_day = forms.SplitDateTimeField(
        widget=forms.SplitDateTimeWidget(
            date_attrs={'type': 'date', 'class': 'form-control'},
            time_attrs={'type': 'time', 'class': 'form-control'}
        )
    )

    class Meta:
        model = Event
        fields = EVENT_FIELDS
        labels = {
            "image": "Poster",
            "start_day": "Start Date and Time",
            "end_day": "End Date and Time"
        }

class NotificationForm(forms.Form):
    # recipient = forms.CharField(label='Send to', max_length=100)
    title = forms.CharField(label='Title', max_length=30)
    message = forms.CharField(widget=forms.Textarea, label='Message', max_length=100)

    def send_notification(self):
        # user = User.objects.get(email=self.cleaned_data["recipient"])
        send_notification_to_all(self.cleaned_data)
