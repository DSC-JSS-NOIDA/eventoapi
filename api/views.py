
from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.password_validation import validate_password

from rest_framework import permissions, filters
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.throttling import AnonRateThrottle
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_503_SERVICE_UNAVAILABLE
)

from .sns import send_otp
from .models import Society, Event, Tag
from .serializers import (UserSerializer, SocietySerializer, EventSerializer,
                          TagSerializer)


User = get_user_model()
CURRENT_SESSION = settings.CURRENT_SESSION


class LoginView(APIView):
    permission_classes = [
        permissions.AllowAny
    ]

    def post(self, request):
        username = request.data.get("email")
        if username is None:
            username = request.data.get("phone")

        password = request.data.get("password")
        if username is None or password is None:
            return Response({'error': 'Please provide both email/phone and password'},
                            status=HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=HTTP_404_NOT_FOUND)

        token, _ = Token.objects.get_or_create(user=user)

        fcm_token = request.data.get("fcm_token")        
        if fcm_token is not None:
            user.fcm_token = fcm_token
            user.save()

        if not user.verified:
            return Response({'token': token.key, 'email': user.email, 'name': user.name,
                            'verified': False}, status=HTTP_200_OK)

        return Response({'token': token.key, 'email': user.email, 'name': user.name, },
                        status=HTTP_200_OK)


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer


class VerificationView(APIView):
    permission_classes = [
        permissions.AllowAny
    ]

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        if email is None or otp is None:
            return Response({'error': 'Request must include email and OTP.'},
                            status=HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)            
        except User.DoesNotExist:
            return Response({'error': 'No user with the given email exists.'},
                            status=HTTP_404_NOT_FOUND)

        if user.verified:
            return Response({'error': 'User already verified.'},
                        status=HTTP_400_BAD_REQUEST)

        if otp == str(user.otp):
            token, _ = Token.objects.get_or_create(user=user)
            user.verified = True
            user.save()
            return Response({'token': token.key, 'email': user.email, 'name': user.name, },
                            status=HTTP_200_OK)

        return Response({'error': 'Wrong OTP'},
                        status=HTTP_400_BAD_REQUEST)


class ResendOTPView(APIView, AnonRateThrottle):
    permission_classes = [
        permissions.AllowAny
    ]

    rate = '3/hour'

    def post(self, request):
        email = request.data.get("email")

        if email is None:
            return Response({'error': 'Request must include email.'},
                            status=HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)            
        except User.DoesNotExist:
            return Response({'error': 'No user with the given email exists.'},
                            status=HTTP_404_NOT_FOUND)

        reset = request.data.get("reset")
        if  reset is not None and reset == "true":
            send_otp(user.phone, user.otp, True)
        else:            
            send_otp(user.phone, user.otp)
        
        return Response({}, status=HTTP_200_OK)


class ForgotView(APIView):
    permission_classes = [
        permissions.AllowAny
    ]

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")
        password = request.data.get("password")

        if email is None or otp is None or password is None:
            return Response({'error': 'Request must include email, OTP and password.'},
                            status=HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)            
        except User.DoesNotExist:
            return Response({'error': 'No user with the given email exists.'},
                            status=HTTP_404_NOT_FOUND)

        if otp != str(user.otp):
            return Response({'error': 'Wrong OTP'},
                            status=HTTP_400_BAD_REQUEST)
        try :
            validate_password(password)
        except:
            return Response({'error': 'Invalid password.'},
                            status=HTTP_200_OK)         

        user.set_password(password)
        user.save()
        return Response({'email': user.email},
                            status=HTTP_200_OK)


class EventView(RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class SocietyView(RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = Society.objects.all()
    serializer_class = SocietySerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('name',)
    ordering = ('name',)


class TagEventsView(ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = EventSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('name', 'start_day')
    ordering = ('start_day',)

    def get_queryset(self):
        current = self.kwargs['current']
        pk = self.kwargs['pk']
        if current:
            queryset = Tag.objects.get(pk=pk).event_set.filter(
                session=CURRENT_SESSION)
        else:
            queryset = Tag.objects.get(pk=pk).event_set.all()
        return queryset


class EventListView(ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('name', 'start_day')
    ordering = ('start_day',)


class UpcomingEventListView(ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = EventSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('name', 'start_day')
    ordering = ('start_day',)

    def get_queryset(self):
        limit = self.kwargs['limit']
        if limit is not None:
            queryset = Event.objects.filter(
                end_day__gte=timezone.now())[:limit]
        else:
            queryset = Event.objects.filter(end_day__gte=timezone.now())
        return queryset


class PastEventListView(ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = EventSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('name', 'end_day')
    ordering = ('-end_day',)

    def get_queryset(self):
        queryset = Event.objects.filter(end_day__lte=timezone.now())
        return queryset


class SocietyListView(ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = Society.objects.all()
    serializer_class = SocietySerializer


class TagListView(ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class SocietyEventsView(ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = EventSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('name', 'start_day')
    ordering = ('start_day',)

    def get_queryset(self):
        period = self.kwargs['period']
        pk = self.kwargs['pk']
        if period == "current":
            queryset = Society.objects.get(
                pk=pk).event_set.filter(session=CURRENT_SESSION)
        elif period == "upcoming":
            queryset = Society.objects.get(pk=pk).event_set.all().filter(
                end_day__gte=timezone.now())
        else:
            queryset = Society.objects.get(pk=pk).event_set.all()

        return queryset



class SocietyPastEventsView(ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = EventSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('name', 'end_day')
    ordering = ('-end_day',)

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = Society.objects.get(pk=pk).event_set.all().filter(
                end_day__lte=timezone.now())

        return queryset
