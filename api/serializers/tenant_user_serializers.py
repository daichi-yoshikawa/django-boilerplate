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
    validated_data.pop('invitation_code')
    return super().create(validated_data)

  def validate(self, data):
    if self.user.id != data['user_id']:
      raise serializers.ValidationError('Request sent from invalid user.')
    models.User.objects.get(id=data['user_id'], email=self.user.email)

    invitation_code = models.TenantInvitationCode.objects.get(
        email=self.user.email, invitation_code=data['invitation_code'])
    if invitation_code.tenant_id != data['tenant_id']:
      raise serializers.ValidationError('Invitation code is not for the tenant.')
    if utils.get_utc_now() > invitation_code.valid_until:
      raise exceptions.TenantInvitationCodeExpired()

    return data


class TenantUserRoleTypeSerializer(BaseModelSerializer):
  tenant = TenantSerializer(required=False, read_only=True)
  user = UserSerializer(required=False, read_only=True)

  tenant_user_id = serializers.IntegerField()
  role_type = serializers.IntegerField()

  class Meta(BaseModelSerializer.Meta):
    model = models.TenantUser

  def validate(self, data):
    admin_role_type = constants.TENANT_USER_ROLE_TYPE.ADMIN.value
    if self.tenant_user.role_type != admin_role_type:
      raise serializers.ValidationError('General user can not edit role type.')

    if self.tenant_user.id == data['tenant_user_id']:
      raise serializers.ValidationError('Can\'t edit self role type.')

    if data['role_type'] == constants.TENANT_USER_ROLE_TYPE.GENERAL.value:
      query = models.TenantUser.objects\
          .filter(
            tenant_id=self.tenant_user.tenant.id,
            role_type=constants.TENANT_USER_ROLE_TYPE.ADMIN.value)\
          .exclude(
            pk=data['tenant_user_id'])
      if query.count() == 0:
        raise serializers.ValidationError(
            'If the tenant user is assigned to general user, '\
            'no admin user is in the tenant.')

    return data
