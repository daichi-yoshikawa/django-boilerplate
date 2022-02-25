import logging

from django.contrib.postgres.search import TrigramSimilarity
from django.db import transaction
from django.db.models import Q, Value
from django.db.models.functions import Concat, Greatest

from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from api import serializers
from api.common import constants
from api.resources.decorators import (
  self_tenant_user_data_api, tenant_user_api, tenant_api)
from core import models


logger = logging.getLogger(__name__)

class TenantUserListView(APIView):
  @tenant_user_api
  def get(self, request, tenant, domain):
    query = models.TenantUser.objects.filter(tenant_id=tenant.id)

    search = request.query_params.get('search')
    if (search is not None) and (len(search.strip(' ')) > 0):
      query = self.filter_by_search_text(search, query)

    page = self.paginate_queryset(query, request)
    serializer = serializers.TenantUserSerializer(page, many=True)

    ret = dict(results=serializer.data, count=self.page.paginator.count)
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

  def filter_by_search_text(self, search, query):
    if len(search.split(' ')) > 1:
      query = self.filter_by_full_name(search, query)
    else:
      query = self.filter_by_first_or_last_name(search, query)

    query = query\
      .filter(
        Q(name_similarity__gt=constants.SEARCH_USER_SIMILARITY_THRESHOLD) |
        Q(user__email__icontains=search))\
      .order_by('name_similarity')

    return query

  def filter_by_full_name(self, search, query):
    return query\
      .annotate(
        username=Concat('user__first_name', Value(' '), 'user__last_name'))\
      .annotate(name_similarity=TrigramSimilarity('username', search))

  def filter_by_first_or_last_name(self, search, query):
    return query\
      .annotate(fn_similarity=TrigramSimilarity('user__first_name', search))\
      .annotate(ln_similarity=TrigramSimilarity('user__last_name', search))\
      .annotate(name_similarity=Greatest('fn_similarity', 'ln_similarity'))

  def filter_by_email(self, search, query):
    return query\
      .filter(user__email__icontains=search)


class TenantUserView(APIView):
  @tenant_user_api
  def get(self, request, tenant_user, domain, tenant_user_id):
    where = Q(tenant_id=tenant_user.tenant.id)
    where &= Q(id=tenant_user_id) if tenant_user_id != 0 else (
        Q(user_id=request.user.id))
    tenant_user = models.TenantUser.objects.get(where)
    serializer = serializers.TenantUserSerializer(tenant_user)
    return Response(serializer.data, status=status.HTTP_200_OK)

  @self_tenant_user_data_api
  def put(self, request, tenant_user, domain, tenant_user_id):
    tenant_user = models.Tenantuser.objects.get(pk=tenant_user_id)
    serializer = serializers.TenantUserSerializer(
        tenant_user, data=request.data, user=tenant_user.user, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

  @self_tenant_user_data_api
  def delete(self, request, tenant_user, domain, tenant_user_id):
    admin_tenant_users = models.TenantUser.objects\
        .filter(
          tenant_id=tenant_user.tenant.id,
          role_type=constants.TENANT_USER_ROLE_TYPE.ADMIN.value)\
        .exclude(pk=tenant_user_id)

    if admin_tenant_users.count() == 0:
      raise RuntimeError(
          'If the user is deleted, no other admin user is in the tenant. '\
          'Assign other user(s) to admin before deleting the user.')

    tenant_user = models.TenantUser.objects.get(
      pk=tenant_user_id, tenant_id=tenant_user.tenant.id)

    if (tenant_user_id != tenant_user.id) and (
        tenant_user.role_type != constants.TENANT_USER_ROLE_TYPE.ADMIN.value):
      raise RuntimeError(
          'Can not delete account because user is not admin.')

    serializer = serializers.TenantUserSerializer(tenant_user)
    data = serializer.data
    tenant_user.delete()
    return Response(serializer.data, status=status.HTTP_200_OK)
