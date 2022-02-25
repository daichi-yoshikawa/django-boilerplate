import logging
import os

from django.conf import settings
from django.core.mail import EmailMessage
from django.db import transaction
from ipware import get_client_ip
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api import serializers
from api.common import exceptions, utils
from core import models


logger = logging.getLogger(__name__)

class PasswordResetCodeView(APIView):
  permission_classes = (AllowAny,)
  BASE_URL = os.path.join(settings.APP_DOMAIN, 'auth/password/reset/')

  @transaction.atomic
  def post(self, request):
    serializer = serializers.PasswordResetCodeSerializer(
        data=request.data, user=request.user)
    serializer.is_valid(raise_exception=True)
    reset_code = serializer.save()

    self.send_reset_code(
        email=reset_code.email, reset_code=reset_code.reset_code)

    return Response(serializer.data, status=status.HTTP_200_OK)

  def send_reset_code(self, email, reset_code):
    url = self.BASE_URL.rstrip('/') + f'/{reset_code}'
    subject = 'Reset your password'
    body = (f'Thank you for using {settings.APP_NAME}.\n\n'
            f'Please take a second to reset your password '
            f'from the following URL.\n{url}\n\n'
            f'Note that the above link expires in '
            f'{settings.PASSWORD_RESET_CODE_LIFETIME_MINS} minutes.\n')
    email = EmailMessage(subject=subject, body=body, to=[email])
    email.send()


class PasswordResetView(APIView):
  permission_classes = (AllowAny,)

  @transaction.atomic
  def post(self, request):
    user = models.User.objects.get(email=request.data['email'])
    serializer = serializers.PasswordResetSerializer(
        user, data=request.data, user=request.user)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    self.delete_password_reset_codes(email=user.email)
    self.delete_failed_login_attempts(request=request, email=user.email)

    return Response(serializer.data, status=status.HTTP_200_OK)

  def delete_password_reset_codes(self, email):
    query = models.PasswordResetCode.objects.filter(email=email)
    count = query.count()
    query.delete()
    logger.debug(f'Deleted {count} password reset codes for {email}.')

  def delete_failed_login_attempts(self, request, email):
    ip_address, is_routable = get_client_ip(request)

    if ip_address is None:
      return

    query = models.FailedLoginAttempt.objects.filter(
        email=email, ip_address=ip_address)
    failed_login_attempts = query.all()
    if failed_login_attempts:
      failed_login_attempts.delete()


class PasswordResetEmailView(APIView):
  permission_classes = (AllowAny,)

  def post(self, request):
    serializer = serializers.PasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
