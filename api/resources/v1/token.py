from ipware import get_client_ip
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

  def post(self, request, *args, **kwargs):
    class Request:
      data = dict()

    ip_address, is_routable = get_client_ip(request)

    request_ = Request()
    request_.data = {
      **dict(request.data),
      'ip_address': ip_address,
    }

    return super().post(request_, *args, **kwargs)


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
