import logging

from django.db import transaction
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api import serializers
from api.resources.decorators import tenant_user_api, tenant_api
from api.resources.paginator import Paginator
from core import models


logger = logging.getLogger(__name__)

class TenantUserListView(APIView):
  @tenant_user_api
  def get(self, request, tenant_user, domain):
    query = models.TenantUser.objects.filter(tenant_id=tenant_user.tenant.id)
    paginator = Paginator(query, request.query_params)
    page_objects = paginator.get_page(
        query_params=request.query_params, allow_return_all=True)

    ret = {
      'tenant_users': [],
      'page': page_objects.number,
    }
    ret.update(paginator.get_profile())

    serializer = serializers.TenantUserSerializer(tenant_user, many=True)
    ret['tenant_users'] = serializer.data
    return Response(ret, status=status.HTTP_200_OK)

  @tenant_api
  @transaction.atomic
  def post(self, request, tenant, domain):
    serializer = serializers.InvitedTenantUserSerializer(
        data=request.data, tenant=tenant, user=request.user,
        extra_request=dict(tenant_id=tenant.id))
    serializer.is_valid(raise_exception=True)
    tenant_user = serializer.save()

    self.delete_invitation_codes(tenant_user.user.email)

    serializer = serializers.TenantUserSerializer(tenant_user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

  def delete_invitation_codes(self, email):
    query = models.TenantInvitationCode.objects.filter(email=email)
    count = query.count()
    query.delete()
    logger.debug(f'Deleted {count} tenant invitation codes for {email}.')


class TenantUserView(APIView):
  @tenant_user_api
  def get(self, request, tenant_user, domain, tenant_user_id):
    where = Q(tenant_id=tenant_user.tenant.id)
    where &= Q(id=tenant_user_id) if tenant_user_id != 0 else (
        Q(user_id=request.user.id))
    tenant_user = models.TenantUser.objects.get(where)
    serializer = serializers.TenantUserSerializer(tenant_user)
    return Response(serializer.data, status=status.HTTP_200_OK)
