from django.db import models
from django.contrib.auth.models import PermissionsMixin,  AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.core.validators import RegexValidator


phone_regex = RegexValidator(regex=r'^\d{10}$', message="Invalid phone number.")

class AccountManager(BaseUserManager):
    def create_user(self, email, name, password, phone):
        user = self.model(email=self.normalize_email(email),
                          name=name, password=password, phone=phone)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password, phone):
        user = self.create_user(email=self.normalize_email(
            email), name=name, password=password, phone=phone)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email_):
        print(email_)
        return self.get(email=email_)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=40, blank=False, null=False)
    otp = models.IntegerField(null=True, blank=True)
    otp_expiry = models.DateTimeField(default=timezone.now, null=True, blank=True)
    verified = models.BooleanField(default=False, null=False, blank=True)
    role = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(
        validators=[phone_regex], unique=True, null=True, max_length=10)
    status = models.IntegerField(null=True, blank=True)
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
    name = models.CharField(max_length=100, unique=True, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    logo = models.ImageField(upload_to='', blank=True)
    department_name = models.CharField(max_length=120, null=False)
    phone = models.CharField(
        validators=[phone_regex], null=True, blank=True, max_length=10)
    email = models.EmailField(null=True, blank=True)

    def publish(self):
        self.published_date = timezone.now
        self.save()

    def __str__(self):
        return self.name


class Event(models.Model): #not working, fix foreign key field
    name = models.CharField(max_length=80, null=False)
    start_day = models.DateTimeField(
        u'Start day of the event', help_text='Start day of the event')
    end_day = models.DateTimeField(
        u'End day of the event', help_text='End day of the event')
    start_time = models.TimeField('Starting time', help_text='Starting time')
    end_time = models.TimeField('Ending time', help_text='Ending time')
    notes = models.TextField(
        u'Textual field', help_text='Textual field', blank=True, null=True)
    image = models.ImageField(upload_to='', blank=True)
    contact_person = models.CharField(null=True, blank=True, max_length=30)
    phone = models.CharField(
        validators=[phone_regex], null=True, blank=True, max_length=10)
    society = models.ForeignKey(
        Society, related_name='event', on_delete=models.CASCADE)
    creater = models.ForeignKey(
        User, related_name='event', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, null=False)
    events = models.ManyToManyField(Event, related_name="tags", blank=True)

    def __str__(self):
        return self.name
