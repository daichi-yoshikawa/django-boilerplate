from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from api import serializers


class CustomTokenObtainPairView(TokenObtainPairView):
  serializer_class = serializers.CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
  serializer_class = serializers.CustomTokenRefreshSerializer


class CustomTokenVerifyView(APIView):
  permission_classes = (IsAuthenticated,)

  def post(self, request):
    return Response({}, status=status.HTTP_200_OK)


class TokenRevokeView(APIView):
  permission_classes = (IsAuthenticated,)

  def post(self, request):
    if 'refresh' not in request.data:
      raise ValidationError('refresh is required to revoke token.')

    refresh_token = request.data['refresh']
    token = RefreshToken(refresh_token)
    token.blacklist()

    ret = {'refresh': request.data['refresh']}
    return Response(ret, status=status.HTTP_200_OK)
