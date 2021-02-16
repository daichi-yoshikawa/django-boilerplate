from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.common import exceptions, utils
from api.serializers.base_serializers import BaseModelSerializer
from core import models


class PasswordResetCodeSerializer(BaseModelSerializer):
  class Meta(BaseModelSerializer.Meta):
    model = models.PasswordResetCode
    read_only_fields = (('reset_code', 'valid_until',) +
                        BaseModelSerializer.Meta.read_only_fields)

  def create(self, validated_data):
    validated_data = self.createrstamp(validated_data)
    password_reset_code = models.PasswordResetCode(**validated_data)
    password_reset_code.set_reset_code()
    return password_reset_code

  def validate(self, data):
    if not models.User.objects.filter(email=data['email']).exists():
      raise exceptions.EmailNotRegistered(f'{data["email"]} is not signed up.')
    return data


class PasswordResetSerializer(BaseModelSerializer):
  reset_code = serializers.CharField()

  class Meta(BaseModelSerializer.Meta):
    model = models.User
    exclude = None
    fields = ('email', 'password', 'reset_code',)
    extra_kwargs = {
      **BaseModelSerializer.Meta.extra_kwargs,
      **{
        'password': { 'write_only': True },
      },
    }

  def update(self, instance, validated_data):
    validated_data = self.updaterstamp(validated_data)
    instance = super().update(instance, validated_data)
    instance.set_password(validated_data['password'])
    instance.save()
    return instance

  def validate(self, data):
    if not models.User.objects.filter(email=data['email']).exists():
      raise exceptions.EmailNotRegistered(f'{data["email"]} is not signed up.')

    query = models.PasswordResetCode.objects.filter(
        email=data['email'], reset_code=data['reset_code'])
    if query.count() == 0:
      raise ValidationError(f'Reset code for {data["email"]} is invalid.')

    password_reset_code = query.get()
    if utils.get_utc_now() > password_reset_code.valid_until:
      raise exceptions.PasswordResetCodeExpired()

    return data
