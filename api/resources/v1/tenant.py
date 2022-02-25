import logging

from django.conf import settings
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api import serializers
from api.common import constants
from api.resources.decorators import tenant_admin_api, tenant_user_api
from core import models


logger = logging.getLogger(__name__)

class TenantListView(APIView):
  @transaction.atomic
  def post(self, request):
    serializer = serializers.TenantSerializer(
        data=request.data, user=request.user)
    serializer.is_valid(raise_exception=True)
    tenant = serializer.save()
    ret = serializer.data

    data = {
      'user_id': request.user.id,
      'role_type': constants.TENANT_USER_ROLE_TYPE.ADMIN.value,
    }
    serializer = serializers.TenantUserSerializer(
        data=data, user=request.user, tenant=tenant,
        extra_request=dict(tenant_id=tenant.id))
    serializer.is_valid(raise_exception=True)
    tenant_user = serializer.save()
    tenant_user.role_type = constants.TENANT_USER_ROLE_TYPE.ADMIN.value
    tenant_user.save()

    return Response(ret, status=status.HTTP_200_OK)


class TenantView(APIView):
  @tenant_user_api
  def get(self, request, tenant_user, domain):
    tenant = models.Tenant.objects.get(domain=domain)
    serializer = serializers.TenantSerializer(tenant)
    return Response(serializer.data, status=status.HTTP_200_OK)

  @tenant_admin_api
  def put(self, request, tenant_user, domain):
    tenant = models.Tenant.objects.get(pk=tenant_user.tenant.id, domain=domain)
    serializer = serializers.TenantSerializer(
      tenant, data=request.data, tenant_user=tenant_user, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_200_OK)
