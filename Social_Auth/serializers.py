from decouple import config
from rest_framework import serializers, status
from rest_framework.response import Response
from . import google, facebook, twitter
from .register import register_social_user
from rest_framework.exceptions import AuthenticationFailed
from users.models import User


class GoogleSocialAuthSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField()

    class Meta:
        fields = ['auth_token']
        model = User

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except Exception:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        # Uncomment in Production and add GOOGLE_CLIENT_ID to settings.py
        """
        
        if user_data['aud'] != config('GOOGLE_CLIENT_ID'):
            # Feel free to change message to something less cheesy
            raise AuthenticationFailed('This Application is Unknown, Who Are you? :(')
            
        """

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'Google'

        registered_user = register_social_user(provider=provider, user_id=user_id,
                                               email=email, name=name)

        return Response(registered_user, status=status.HTTP_200_OK)


class FacebookAuthSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField()

    class Meta:
        fields = ['auth_token']
        model = User

    def validate_auth_token(self, auth_token):
        user_data = facebook.Facebook.validate(auth_token)
        try:
            user_id = user_data['id']
            email = user_data['email']
            name = user_data['name']
            provider = 'Facebook'
            register_social_user(
                provider=provider,
                user_id=user_id,
                email=email,
                name=name
            )
        except Exception:
            return serializers.ValidationError(
                "Token Invalid or Expired, please login again"
            )
