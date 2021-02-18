import logging
import os
import urllib.parse

from django.conf import settings
from django.core.mail import send_mass_mail
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api import serializers
from api.resources.decorators import tenant_user_api
from core import models


logger = logging.getLogger(__name__)

class TenantInvitationCodeListView(APIView):
  BASE_URL = os.path.join(settings.APP_DOMAIN, 'auth/invite/')

  @tenant_user_api
  @transaction.atomic
  def post(self, request, tenant_user, domain):
    serializer = serializers.TenantInvitationCodeSerializer(
        data=request.data, tenant_user=tenant_user, many=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    self.send_invitation_code(
        tenant=tenant_user.tenant, sender=tenant_user,
        data=serializer.data)

    return Response(serializer.data, status=status.HTTP_200_OK)

  def send_invitation_code(self, tenant, sender, data):
    emails = [d['email'] for d in data]
    codes = [d['invitation_code'] for d in data]
    emails, codes = self.drop_existing_tenant_users(
        tenant_id=tenant.id, emails=emails, codes=codes)
    mass_messages = tuple()
    for email, code in zip(emails, codes):
      mass_messages = mass_messages + (self.get_email_message(
          tenant=tenant, sender=sender, email=email, code=code),)

    send_mass_mail(mass_messages, fail_silently=False)

  def get_email_message(self, tenant, sender, email, code):
    query_params = urllib.parse.urlencode({ 'email': email })
    url = self.BASE_URL.rstrip('/') + f'/{code}?{query_params}'
    subject = (f'{sender.user.first_name} {sender.user.last_name} '
               f'has invited you to join the workspace in '
               f'{settings.APP_NAME}')
    body = (f'{sender.user.first_name} {sender.user.last_name}'
            f'({sender.user.email}) has invited you({email}) to join '
            f'{tenant.name} in {settings.APP_NAME}.\n'
            f'If you accept the request, click the following URL.\n\n'
            f'{url}\n\n'
            f'Note that the above invitation link expires in '
            f'{settings.TENANT_INVITATION_CODE_LIFETIME_MINS} minutes.\n')
    from_email = settings.EMAIL_HOST_USER
    return (subject, body, from_email, [email],)

  def drop_existing_tenant_users(self, tenant_id, emails, codes):
    filtered_emails = []
    filtered_codes = []
    for email, code in zip(emails, codes):
      query = models.TenantUser.objects.filter(
          tenant_id=tenant_id, user__email=email)
      if not query.exists():
        filtered_emails.append(email)
        filtered_codes.append(code)

    return filtered_emails, filtered_codes


class InvitedTenantView(APIView):
  def post(self, request):
    serializer = serializers.InvitedTenantSerializer(
        data=request.data, user=request.user)
    serializer.is_valid(raise_exception=True)

    tenant_invitation_code = models.TenantInvitationCode.objects.get(
        invitation_code=serializer.data['invitation_code'],
        email=serializer.data['email'])
    tenant_id = tenant_invitation_code.tenant.id

    tenant = models.Tenant.objects.get(pk=tenant_id)
    serializer = serializers.TenantSerializer(tenant)
    return Response(serializer.data, status=status.HTTP_200_OK)
