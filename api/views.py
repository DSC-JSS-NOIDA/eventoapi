
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from rest_framework import permissions
from rest_framework.authtoken.models import Token

from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.views import APIView

from .models import Society, Event, Tag
from .serializers import (UserSerializer, SocietySerializer, EventSerializer,
                          TagSerializer)

User = get_user_model()


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

        if not user.verified:
            return Response({'token': token.key, 'email': user.email, 'name': user.name, 'verified': False},
                            status=HTTP_200_OK)

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
        try:
            instance = User.objects.get(email=request.data.get("email"))
        except:
            return Response({'error': 'Invalid credentials'},
                            status=HTTP_400_BAD_REQUEST)
        otp = request.data.get("otp")
        if otp == "111111":
            token, _ = Token.objects.get_or_create(user=instance)
            instance.verified = True
            instance.otp = otp
            instance.save()
            return Response({'token': token.key, 'email': instance.email, 'name': instance.name, },
                            status=HTTP_200_OK)
        else:
            return Response({'error': 'Wrong OTP'},
                            status=HTTP_400_BAD_REQUEST)


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


class TagView(RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class EventListView(ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class SocietyListView(ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = Society.objects.all()
    serializer_class = SocietySerializer


# class CreateSocietyView(CreateAPIView):
#     permission_classes = [
#         permissions.IsAuthenticated
#     ]
#     serializer_class = SocietySerializer


# class CreateTagView(CreateAPIView):
#     permission_classes = [
#         permissions.IsAuthenticated
#     ]
#     serializer_class = TagSerializer


# class CreateEventView(CreateAPIView):
#     permission_classes = [
#         permissions.IsAuthenticated
#     ]
#     serializer_class = EventSerializer
