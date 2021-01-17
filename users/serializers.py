from django.contrib.auth import authenticate
from rest_framework.serializers import *
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from .models import User


class RegisterSerializer(ModelSerializer):
    password = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    # Modify create method to use custom create_user
    def create(self, validated_data):
        email = validated_data.pop('email')
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()
        return user


class EmailVerificationSerializer(ModelSerializer):
    token = serializers.CharField()

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=255, min_length=3)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username']

    def validate(self, attr):
        email = attr.get('email')
        password = attr.get('password')
        filtered_user_by_email = User.objects.filter(email=email)

        user = authenticate(email=email, password=password)

        if filtered_user_by_email[0].auth_provider != 'Email':
            raise AuthenticationFailed(detail='Please Continue your login with' +
                                              filtered_user_by_email[0].auth_provider)

        if not user:
            raise AuthenticationFailed('Invalid Login Parameters')
        if not user.is_active:
            raise AuthenticationFailed('Account has been disabled, please contact us for more info')
        if not user.is_verified:
            raise AuthenticationFailed('User is not verified')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.get_tokens()
        }
