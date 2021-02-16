import logging

from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.common import exceptions, utils
from api.serializers.base_serializers import BaseModelSerializer
from core import models


logger = logging.getLogger(__name__)

class NewUserSerializer(BaseModelSerializer):
  invitation_code = serializers.CharField(required=False, write_only=True)
  verification_code = serializers.CharField(required=False, write_only=True)

  class Meta(BaseModelSerializer.Meta):
    model = models.User
    read_only_fields = (('status',) +
                        BaseModelSerializer.Meta.read_only_fields)
    extra_kwargs = {
      **BaseModelSerializer.Meta.extra_kwargs,
      **{
        'password': { 'write_only': True },
      },
    }

  def create(self, validated_data):
    validated_data = self.createrstamp(validated_data)
    if ('invitation_code' not in validated_data) and\
       ('verification_code' not in validated_data):
      raise ValidationError(
          'Invitation code or verification code is needed to create ')

    if 'invitation_code' in validated_data:
      validated_data.pop('invitation_code')
    if 'verification_code' in validated_data:
      validated_data.pop('verification_code')

    user = models.User(**validated_data)
    user.set_password(validated_data['password'])
    return user

  def validate(self, data):
    if 'invitation_code' in data:
      invitation_code = models.TenantInvitationCode.objects.get(
          email=data['email'], invitation_code=data['invitation_code'])
      if utils.get_utc_now() > invitation_code.valid_until:
        raise exceptions.TenantInvitationCodeExpired()
    if 'verification_code' in data:
      verification_code = models.EmailVerificationCode.objects.get(
          email=data['email'], verification_code=data['verification_code'])
      if utils.get_utc_now() > verification_code.valid_until:
        raise exceptions.EmailVerificationCodeExpired()

    """
    Set blank to groups and user_permissions if they're empty.
    If not, error like "Direct assignment to the forward side of a many-to-many
    set is prohibited. User xxxx.set() instead." occurs when executing pytest.
    """
    data = self.set_blank_explicitly(data, fields=['groups', 'user_permissions'])

    return data


class UserSerializer(BaseModelSerializer):
  class Meta(BaseModelSerializer.Meta):
    model = models.User
    read_only_fields = (('status',) +
                        BaseModelSerializer.Meta.read_only_fields)
    exclude = ('password',) + BaseModelSerializer.Meta.exclude

  def get_image(self, obj):
    request = self.context.get('request')
    image = models.User.image.url
    return request.build_absolute_url(image)

  def create(self, validated_data):
    validated_data = self.createrstamp(validated_data)
    user = models.User(**validated_data)
    user.set_password(validated_data['password'])
    return user

  def update(self, instance, validated_data):
    validated_data = self.updaterstamp(validated_data)

    instance = super().update(instance, validated_data)

    if 'password' in validated_data:
      instance.set_password(validated_data['password'])
    instance.save()
    return instance


class UserPasswordSerializer(BaseModelSerializer):
  password = serializers.CharField(max_length=200, min_length=8)
  new_password = serializers.CharField(required=False, max_length=200, min_length=8)

  class Meta:
    model = models.User
    exclude = None
    fields = ('password', 'new_password',)

  def update(self, instance, validated_data):
    validated_data = self.updaterstamp(validated_data)
    validated_data['password'] = validated_data['new_password']
    validated_data.pop('new_password')

    instance = super().update(instance, validated_data)
    instance.set_password(validated_data['password'])
    instance.save()
    return instance

  def validate(self, data):
    user = models.User.objects.get(pk=self.user.id)

    if not user.check_password(data['password']):
      raise ValidationError('Current password is wrong.')

    if data['password'] == data['new_password']:
      raise ValidationError('New password is the same as current password.')

    return data
