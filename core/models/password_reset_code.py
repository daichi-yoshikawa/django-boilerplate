import datetime

from django.conf import settings
from django.db import models

from api.common import utils
from core.models.base_models import BaseModel


class PasswordResetCode(BaseModel):
  class Meta(BaseModel.Meta):
    db_table = 'password_reset_codes'

  email = models.EmailField(
      max_length=200, unique=False, null=False, blank=False)
  reset_code = models.CharField(
      max_length=200, unique=True, null=False, blank=False)
  valid_until = models.DateTimeField(unique=False, null=False, blank=False)

  def set_reset_code(self):
    self.reset_code = utils.generate_random_letters(
        length=settings.PASSWORD_RESET_CODE_LENGTH)
    self.valid_until = utils.get_utc_now() + datetime.timedelta(
        minutes=settings.PASSWORD_RESET_CODE_LIFETIME_MINS)

  def __str__(self):
    return (f'({self.id}){self.email}, '
            f'{self.reset_code}')
