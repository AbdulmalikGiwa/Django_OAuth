from rest_framework.views import *
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from .models import *
from .utils import *
from smtplib import SMTPException
from Bankless.settings import SECRET_KEY
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import jwt


# Create your views here.

# RegisterView to register new users
class RegisterView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user_for_token = User.objects.get(email=serializer.data['email'])
        token = RefreshToken.for_user(user_for_token).access_token
        user_data['token'] = str(token)
        # To catch any error that occurs while sending verification email
        try:
            data = {'email_subject': 'Bankless E-Mail Verification',
                    'email_body': 'Please verify your email with the following link: http://Bankless.com/verify-email',
                    'recipient': [user_for_token.email]}
            Util.send_email(data)
        except SMTPException as e:
            print("An error occurred while sending email: ", e)
            # For test, regardless of error in sending email, token is still returned,
            # Please don't leave this in Production!!!!
            return Response({"message": "There was an error sending email",
                             "token": str(token)})

        return Response(user_data, status=status.HTTP_201_CREATED)


# VerifyEmail class verifies user email and changes "is_verified" field to True
# It decodes token returned upon registration
class VerifyEmail(APIView):
    serializer_class = EmailVerificationSerializer

    # This decorator modifies the swagger endpoint to match te view
    @swagger_auto_schema(request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                     required=['token'],
                                                     properties={
                                                         'token': openapi.Schema(type=openapi.TYPE_STRING)
                                                     },
                                                     ),
                         operation_description='Email Verification Token')
    def post(self, request):
        token = request.data['token']
        try:
            decode_token = jwt.decode(token, options={"verify_signature": False})
            user = User.objects.get(id=decode_token['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({"message": "Email Verification Successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "The following error occurred: {}".format(e)},
                            status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



