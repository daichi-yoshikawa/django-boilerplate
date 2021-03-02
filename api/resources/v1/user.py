import logging

from django.conf import settings
from django.db import transaction
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api import serializers
from api.resources.decorators import strict_user_data_api, user_data_api
from api.resources.paginator import Paginator
from core import models


logger = logging.getLogger(__name__)

class UserListView(APIView):
  permission_classes = (AllowAny,)

  @transaction.atomic
  def post(self, request):
    serializer = serializers.NewUserSerializer(
        data=request.data, user=request.user)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    self.delete_email_verification_codes(email=user.email)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

  def delete_email_verification_codes(self, email):
    query = models.EmailVerificationCode.objects.filter(email=email)
    count = query.count()
    query.delete()
    logger.debug(f'Deleted {count} email verification codes for {email}.')


class UserView(APIView):
  @user_data_api
  def get(self, request, user_id):
    user = models.User.objects.get(pk=request.user.id if user_id == 0 else user_id)
    serializer = serializers.UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

  @strict_user_data_api
  def put(self, request, user_id):
    user = models.User.objects.get(pk=request.user.id)
    serializer = serializers.UserSerializer(
        user, data=request.data, user=request.user, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_200_OK)

  @strict_user_data_api
  def delete(self, request, user_id):
    user = models.User.objects.get(pk=request.user.id)
    serializer = serializers.UserSerializer(user)
    ret = serializer.data
    user.delete()

    return Response(ret, status=status.HTTP_200_OK)


class UserPasswordView(APIView):
  @strict_user_data_api
  def put(self, request, user_id):
    user = models.User.objects.get(pk=user_id)
    serializer = serializers.UserPasswordSerializer(
        user, data=request.data, user=request.user)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_200_OK)


class UserTenantListView(APIView):
  @strict_user_data_api
  def get(self, request, user_id):
    query = models.TenantUser.objects.filter(user_id=request.user.id)
    query = query.order_by('-created_at')
    paginator = Paginator(query, request.query_params)
    page_objects = paginator.get_page(request.query_params)

    ret = {
      'tenants': [],
      'page': page_objects.number,
    }
    ret.update(paginator.get_profile())

    for tenant_user in page_objects:
      tenant = models.Tenant.objects.get(pk=tenant_user.tenant_id)
      serializer = serializers.TenantSerializer(tenant)
      ret['tenants'].append(serializer.data)

    return Response(ret, status=status.HTTP_200_OK)
