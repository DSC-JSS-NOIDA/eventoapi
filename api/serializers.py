from django.contrib.auth import get_user_model
from django.core import exceptions
from django.contrib.auth import password_validation
from rest_framework import serializers
from .models import Society, Event, Tag
from .sns import send_otp

USER = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER
        fields = (
            'email',
            'phone',
            'password',
            'name',
            'fcm_token'
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_password(self, value):
        try:
            password_validation.validate_password(value)
        except exceptions.ValidationError as exc:
            raise serializers.ValidationError(exc.messages)
        return value

    def create(self, validated_data):
        user = USER.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            fcm_token=validated_data['fcm_token']
        )
        user.set_password(validated_data['password'])
        user.save()
        send_otp(user.phone, user.otp)
        return user


class SocietySerializer(serializers.ModelSerializer):
    class Meta:
        model = Society
        fields = ('name', 'created_at', 'logo', 'department_name',
                  'phone', 'email', 'id', 'type')
        extra_kwargs = {
            'id': {'read_only': True},
        }


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'id')
        extra_kwargs = {
            'id': {'read_only': True},
        }


class EventSerializer(serializers.ModelSerializer):
    society_name = serializers.CharField(source='society.name')
    society_logo = serializers.ImageField(source='society.logo')

    class Meta:
        model = Event
        fields = ('name', 'start_day', 'end_day', 'venue', 'registration_link',
                  'notes', 'image', 'contact_person', 'contact_number',
                  'society', 'society_name', 'society_logo', 'id', 'session')
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def create(self, request, obj):
        obj.creater = request.user
        obj.save()
