from django.conf import settings
from rest_framework import serializers

from api.serializers.base_serializers import BaseModelSerializer
from core import models


class EmailVerificationCodeSerializer(BaseModelSerializer):
  class Meta(BaseModelSerializer.Meta):
    model = models.EmailVerificationCode
    read_only_fields = ('valid_until', 'verification_code',) + BaseModelSerializer.Meta.read_only_fields

  def create(self, validated_data):
    validated_data = self.createrstamp(validated_data)
    email_verification_code = models.EmailVerificationCode(**validated_data)
    email_verification_code.set_verification_code()
    email_verification_code.save()
    return email_verification_code


class EmailVerificationSerializer(BaseModelSerializer):
  verification_code = serializers.CharField()

  class Meta(BaseModelSerializer.Meta):
    model = models.EmailVerificationCode
    read_only_fields = ('valid_until',) + BaseModelSerializer.Meta.read_only_fields
