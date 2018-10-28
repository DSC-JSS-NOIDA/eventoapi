
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django import forms
from api.models import Event, Society

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
            date_attrs={'type': 'date', 'class': 'form-control',
                        'min': timezone.now().date},
            time_attrs={'type': 'time', 'class': 'form-control'}
        )
    )
    end_day = forms.SplitDateTimeField(
        widget=forms.SplitDateTimeWidget(
            date_attrs={'type': 'date', 'class': 'form-control',
                        'min': timezone.now().date},
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
    message = forms.CharField(widget=forms.Textarea, label='Message', max_length=100)