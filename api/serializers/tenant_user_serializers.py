import logging

from rest_framework import serializers

from api.common import exceptions, utils
from api.serializers.base_serializers import BaseModelSerializer
from api.serializers.tenant_serializers import TenantSerializer
from api.serializers.user_serializers import UserSerializer
from core import models


logger = logging.getLogger(__name__)

class TenantUserSerializer(BaseModelSerializer):
  tenant = TenantSerializer(required=False, read_only=True)
  user = UserSerializer(required=False, read_only=True)

  tenant_id = serializers.IntegerField(write_only=True)
  user_id = serializers.IntegerField(write_only=True)

  class Meta(BaseModelSerializer.Meta):
    model = models.TenantUser

  def validate(self, data):
    if self.user.id != data['user_id']:
      raise serializers.ValidationError('Request sent from invalid user.')
    if self.tenant.id != data['tenant_id']:
      raise serializers.ValidationError('Request sent across different tenant.')

    return data


class InvitedTenantUserSerializer(BaseModelSerializer):
  tenant = TenantSerializer(required=False, read_only=True)
  user = UserSerializer(required=False, read_only=True)

  tenant_id = serializers.IntegerField(write_only=True)
  user_id = serializers.IntegerField(write_only=True)
  invitation_code = serializers.CharField(write_only=True)

  class Meta(BaseModelSerializer.Meta):
    model = models.TenantUser

  def create(self, validated_data):
    validated_data = self.createrstamp(validated_data)
    validated_data.pop('invitation_code')
    return super().create(validated_data)

  def validate(self, data):
    if self.user.id != data['user_id']:
      raise serializers.ValidationError('Request sent from invalid user.')
    if self.tenant.id != data['tenant_id']:
      raise serializers.ValidationError('Request sent across different tenant.')
    models.User.objects.get(id=data['user_id'], email=self.user.email)

    invitation_code = models.TenantInvitationCode.objects.get(
        email=self.user.email, invitation_code=data['invitation_code'])
    if invitation_code.tenant_id != data['tenant_id']:
      raise serializers.ValidationError('Invitation code is not for the tenant.')
    if utils.get_utc_now() > invitation_code.valid_until:
      raise exceptions.TenantInvitationCodeExpired()

    return data
