from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.core.validators import RegexValidator
from django.utils.crypto import get_random_string

PHONE_REGEX = RegexValidator(
    regex=r'^\d{10}$', message="Invalid phone number.")


class AccountManager(BaseUserManager):
    def create_user(self, email, name, password, phone):
        user = self.model(email=self.normalize_email(email),
                          name=name, password=password, phone=phone)
        user.set_password(password)
        user.is_active = True
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


class Society(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(null=True, blank=True)
    logo = models.ImageField(upload_to='', blank=True)
    department_name = models.CharField(max_length=40, null=False)
    phone = models.CharField(
        validators=[PHONE_REGEX], null=True, blank=True, max_length=10)
    email = models.EmailField(null=True, blank=True)
    type = models.CharField(max_length=30, blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now
        self.save()

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    USER_CHOICES = (('0', 'Regular'), ('1', 'Admin'))

    name = models.CharField(max_length=40, blank=False, null=False)
    otp = models.IntegerField(null=True, blank=True, default=get_random_string(length=6, allowed_chars='0123456789')) 
    otp_expiry = models.DateTimeField(
        default=timezone.now, null=True, blank=True)  # unnecessary field?
    verified = models.BooleanField(default=False, null=True, blank=True)
    phone = models.CharField(
        validators=[PHONE_REGEX], unique=True, null=True, max_length=10)
    role = models.CharField(choices=USER_CHOICES, max_length=1, default='0')
    email = models.EmailField(unique=True, null=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    society = models.ForeignKey(
        Society, null=True, blank=True, on_delete=models.CASCADE)
    fcm_token = models.CharField(null=True, blank=True, max_length=200)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone', ]
    objects = AccountManager()

    def get_short_name(self):
        return self.email

    def natural_key(self):
        return self.email

    def __str__(self):
        return self.email


class Tag(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class Event(models.Model):
    SESSION_CHOICES = (  # Make this dynamic
        ('18', '2018-2019'),
        ('19', '2019-2020')
    )

    name = models.CharField(max_length=80, null=False)
    start_day = models.DateTimeField(
        u'Start date and time', help_text='Time Format: HH:MM:SS')
    end_day = models.DateTimeField(
        u'End date and time')
    notes = models.TextField(
        u'Description', blank=True, null=True)
    image = models.ImageField(upload_to='', blank=True)
    contact_person = models.CharField(null=True, blank=True, max_length=30)
    contact_number = models.CharField(
        validators=[PHONE_REGEX], null=True, blank=True, max_length=10)
    registration_link = models.URLField(null=True, blank=True)
    venue = models.CharField(max_length=50, null=True, blank=True)
    society = models.ForeignKey(
        Society, on_delete=models.CASCADE)
    creater = models.ForeignKey(
        User, related_name='event', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    session = models.CharField(
        max_length=2, blank=True, null=True, choices=SESSION_CHOICES)

    def __str__(self):
        return self.name
