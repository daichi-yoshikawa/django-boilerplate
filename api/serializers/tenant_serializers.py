from django.conf import settings

from api.common import utils
from api.serializers.base_serializers import BaseModelSerializer
from core import models


class TenantSerializer(BaseModelSerializer):
  class Meta(BaseModelSerializer.Meta):
    model = models.Tenant
    read_only_fields = ('domain',) + BaseModelSerializer.Meta.read_only_fields

  def get_image(self, obj):
    request = self.context.get('request')
    image = models.User.image.url
    return request.build_absolute_url(image)

  def create(self, validated_data):
    validated_data = self.createrstamp(validated_data)
    validated_data['domain'] = utils.generate_random_letters(
        length=settings.TENANT_DOMAIN_LENGTH)
    tenant = models.Tenant(**validated_data)
    return tenant
