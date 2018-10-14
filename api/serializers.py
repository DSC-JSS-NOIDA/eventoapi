from django.contrib.auth import get_user_model
from django.core import exceptions
from django.contrib.auth import password_validation
from rest_framework import serializers

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
