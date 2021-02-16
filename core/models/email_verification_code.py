import datetime

from django.conf import settings
from django.db import models

from api.common import utils
from core.models.base_models import BaseModel


class EmailVerificationCode(BaseModel):
  class Meta:
    db_table = 'email_verification_codes'

  email = models.EmailField(
      max_length=200, unique=False, null=False, blank=False)
  verification_code = models.CharField(
      max_length=200, unique=True, null=False, blank=False)
  valid_until = models.DateTimeField(unique=False, null=False, blank=False)

  def set_verification_code(self):
    self.verification_code = utils.generate_random_letters(
        length=settings.EMAIL_VERIFICATION_CODE_LENGTH)
    self.valid_until = utils.get_utc_now() + datetime.timedelta(
        minutes=settings.EMAIL_VERIFICATION_CODE_LIFETIME_MINS)

  def __str__(self):
    return (f'({self.id}){self.email}, '
            f'{self.verification_code}')
