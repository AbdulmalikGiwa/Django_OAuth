from rest_framework import status
from .serializers import *
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView


# Create your views here.

# GoogleSocialAuthView handles auth with Google
class GoogleSocialAuthView(GenericAPIView):
    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as received from Google to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data['auth_token'])
        return Response(data, status=status.HTTP_200_OK)


class FacebookSocialAuthView(GenericAPIView):
    serializer_class = FacebookAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send a token as received from Facebook to get user information
        """
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data['auth_token'])
        return Response(data, status=status.HTTP_200_OK)