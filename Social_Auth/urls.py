from django.urls import path, include
from .views import *

urlpatterns = [
    path('google/', GoogleSocialAuthView.as_view(), name='google'),
    path('facebook/', FacebookSocialAuthView.as_view(), name='facebook')
]
