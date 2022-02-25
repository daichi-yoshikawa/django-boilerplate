import logging

from django.conf import settings
from rest_framework import serializers

from api.common import exceptions
from api.serializers.base_serializers import BaseModelSerializer
from api.serializers.tenant_serializers import TenantSerializer
from api.serializers.tenant_user_serializers import TenantUserSerializer
from core import models


logger = logging.getLogger(__name__)

class TenantInvitationCodeListSerializer(serializers.ListSerializer):
  def validate(self, data):
    if len(data) > settings.TENANT_INVITATION_CODE_REQUEST_MAX_SIZE:
      raise exceptions.RequestSizeError(
          'List size must be <= '
          f'{settings.TENANT_INVITATION_CODE_REQUEST_MAX_SIZE}.')

    if len(set([d['tenant_id'] for d in data])) > 1:
      raise serializers.ValidationError('Multiple tenant ids are contained.')

    if len(set([d['tenant_user_id'] for d in data])) > 1:
      raise serializers.ValidationError('Multiple tenant user ids are contained.')

    if len(set([d['email'] for d in data])) != len(data):
      raise serializers.ValidationError('Duplicated emails are in request.')

    return data


class TenantInvitationCodeSerializer(BaseModelSerializer):
  tenant = TenantSerializer(required=False, read_only=True)
  tenant_user = TenantUserSerializer(required=False, read_only=True)
  invited_at = serializers.DateTimeField(required=False, read_only=True)

  tenant_id = serializers.IntegerField(write_only=True)
  tenant_user_id = serializers.IntegerField(write_only=True)

  class Meta(BaseModelSerializer.Meta):
    list_serializer_class = TenantInvitationCodeListSerializer
    model = models.TenantInvitationCode
    read_only_fields = ('invitation_code', 'valid_until',) + BaseModelSerializer.Meta.read_only_fields

  def create(self, validated_data):
    validated_data = self.createrstamp(validated_data)
    tenant_invitation_code = models.TenantInvitationCode(**validated_data)
    tenant_invitation_code.set_invitation_code()
    tenant_invitation_code.save()
    return tenant_invitation_code

  def validate(self, data):
    if self.partial:
      data = self.fill_missing_fields_by_instance(data)

    if self.tenant_user is None:
      raise serializers.ValidationError('tenant_user is missing.')

    if self.tenant_user.id != data['tenant_user_id']:
      raise serializers.ValidationError('Invalid tenant_user_id.')

    return data


class InvitedTenantSerializer(BaseModelSerializer):
  invitation_code = serializers.CharField(
      max_length=settings.TENANT_INVITATION_CODE_LENGTH)
  tenant = TenantSerializer(required=False, read_only=True)

  class Meta(BaseModelSerializer.Meta):
    model = models.TenantInvitationCode
    read_only_fields = (('tenant', 'tenant_user', 'valid_until',) +
                        BaseModelSerializer.Meta.read_only_fields)

  def validate(self, data):
    if len(data['invitation_code']) != settings.TENANT_INVITATION_CODE_LENGTH:
      raise serializers.ValidationError('Invalid tenant invitation code.')

    query = models.TenantInvitationCode.objects.filter(
        invitation_code=data['invitation_code'])
    if not query.exists():
      raise serializers.ValidationError('Invalid tenant invitation code.')

    return data
