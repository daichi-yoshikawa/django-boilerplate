import datetime

from django.conf import settings
from django.db import models

from api.common import utils
from core.models.base_models import BaseTenantModel


class TenantInvitationCode(BaseTenantModel):
  class Meta:
    db_table = 'tenant_invitation_codes'

  tenant_user = models.ForeignKey(
      'TenantUser', unique=False, null=False, blank=False,
      on_delete=models.CASCADE)
  email = models.EmailField(
      max_length=200, unique=False, null=False, blank=False)
  invitation_code = models.CharField(
      max_length=200, unique=True, null=False, blank=False)
  valid_until = models.DateTimeField(unique=False, null=False, blank=False)

  def set_invitation_code(self):
    self.invitation_code = utils.generate_random_letters(
        length=settings.TENANT_INVITATION_CODE_LENGTH)
    self.valid_until = utils.get_utc_now() + datetime.timedelta(
        minutes=settings.TENANT_INVITATION_CODE_LIFETIME_MINS)

  def __str__(self):
    return (f'({self.id}){self.tenant.name}, '
            f'{self.tenant_user}, '
            f'{self.email}, '
            f'{self.invitation_code[:10]}')
