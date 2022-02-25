from rest_framework import serializers

from api.serializers.base_serializers import BaseModelSerializer
from core import models


class FailedLoginAttemptSerializer(BaseModelSerializer):
  attempted_at = serializers.DateTimeField(required=False, read_only=True)

  class Meta(BaseModelSerializer.Meta):
    model = models.FailedLoginAttempt
