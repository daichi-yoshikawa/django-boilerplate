import os

from django.conf import settings
from django.db import models

from api.common.utils import generate_random_letters, get_far_future_datetime
from core.models.base_models import BaseModel


def get_tenant_image_path(instance, filename):
  _, ext = os.path.splitext(filename)
  filename = generate_random_letters(length=24) + ext
  return f'images/tenant/{instance.id}/{filename}'


class Tenant(BaseModel):
  class Meta(BaseModel.Meta):
    db_table = 'tenants'

  name = models.CharField(
      max_length=200, unique=False, null=False, blank=False)
  domain = models.CharField(
      max_length=200, unique=True, null=False, blank=False)
  image = models.ImageField(
      verbose_name='tenant logo image', null=False, blank=True,
      upload_to=get_tenant_image_path)
  description = models.TextField(
      max_length=1000, unique=False, null=False, blank=True, default='')

  @classmethod
  def get_id_from(cls, domain):
    return cls.objects.get(domain=domain).id

  def set_domain(self):
    self.domain = generate_random_letters(
        length=settings.TENANT_DOMAIN_LENGTH)

  def __str__(self):
    return f'{self.id}){self.name}, {self.domain[:10]}...'
