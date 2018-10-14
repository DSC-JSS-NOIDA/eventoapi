from django.db import models
from django.contrib.auth.models import PermissionsMixin,  AbstractBaseUser, BaseUserManager
from django.utils import timezone

# from django.core.exceptions import ValidationError
# from django.core.urlresolvers import reverse


class AccountManager(BaseUserManager):
    def create_user(self, email, name, password):
        user = self.model(email=email, name=name, password=password)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email=email, name=name, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

    def get_by_natural_key(self, email_):
        print(email_)
        return self.get(email=email_)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=40, blank=False, null=False)
    otp = models.IntegerField(null=True)
    otp_expiry = models.DateTimeField(default=timezone.now, null=True)
    verified = models.BooleanField(default=False, null=False)
    role = models.CharField(max_length=20, null=True)
    phone = models.IntegerField(unique=True, null=True)
    status = models.IntegerField(null=True)
    email = models.EmailField(unique=True, null=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', ]
    objects = AccountManager()

    def get_short_name(self):
        return self.email

    def natural_key(self):
        return self.email

    def __str__(self):
        return self.email


class Society(models.Model):
    name = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    logo = models.ImageField(upload_to='', blank=True)
    department_name = models.CharField(max_length=120, null=False)
    phone = models.IntegerField(null=False)
    email = models.TextField(max_length=100, null=False)

    def publish(self):
        self.published_date = timezone.now
        self.save()

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.TextField(max_length=150, null=False)
    start_day = models.DateTimeField(
        u'Start day of the event', help_text=u'Start day of the event')
    end_day = models.DateTimeField(
        u'End day of the event', help_text=u'End day of the event')
    start_time = models.TimeField(u'Starting time', help_text=u'Starting time')
    end_time = models.TimeField(u'Ending time', help_text=u'Ending time')
    notes = models.TextField(
        u'Textual field', help_text=u'Textual field', blank=True, null=True)
    image = models.ImageField(upload_to='', blank=True)
    contact_person = models.IntegerField(null=False)
    contact_person = models.IntegerField(null=False)
    society = models.ForeignKey(
        Society, related_name='event', on_delete=models.CASCADE)
    creater = models.ForeignKey(
        User, related_name='event', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
