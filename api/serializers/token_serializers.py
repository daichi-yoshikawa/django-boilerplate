from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.settings import api_settings

from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from core import models


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
  username_field = models.User.EMAIL_FIELD

  @classmethod
  def get_token(cls, user):
    return super().get_token(user)

  def validate(self, data):
    data = super().validate(data)

    access_expires_in = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
    refresh_expires_in = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()
    data['access_expires_in'] = int(access_expires_in)
    data['refresh_expires_in'] = int(refresh_expires_in)

    return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
  @classmethod
  def get_token(cls, user):
    token = super().get_token(user)
    return token

  def validate(self, data):
    data = super().validate(data)

    access_expires_in = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
    data['access_expires_in'] = int(access_expires_in)

    return data
