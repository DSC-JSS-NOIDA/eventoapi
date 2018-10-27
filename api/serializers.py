from django.contrib.auth import get_user_model
from django.core import exceptions
from django.contrib.auth import password_validation
from rest_framework import serializers
from .models import Society, Event, Tag
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'phone',
            'password',
            'name'
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
        user = User.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            phone=validated_data['phone']
        )
        user.set_password(validated_data['password'])
        user.save()

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

    class Meta:
        model = Event
        fields = ('name', 'start_day', 'end_day',
                  'notes', 'image', 'contact_person', 'contact_number',
                  'society', 'society_name', 'id', 'session')
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def create(self, request, obj):
        obj.creater = request.user
        obj.save()
