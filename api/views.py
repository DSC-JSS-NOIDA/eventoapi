
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from datetime import datetime


from django.contrib.auth import get_user_model
User = get_user_model()


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None or password is None:
        return Response({'error': 'Please provide both email and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(email=email, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token = Token.objects.create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def register(request):
    email = request.data.get("email")
    name = request.data.get("name")
    password = request.data.get("password")
    if email is None or password is None or name is None:
        return Response({'error': 'Please provide credentials'},
                        status=HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(
        email=email,
        name=name,
        password=password
    )
    user.save()

    return Response({'name': name},
                    status=HTTP_200_OK)
