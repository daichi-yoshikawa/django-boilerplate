from django.db import models

from core.models.base_models import BaseModel


class FailedLoginAttempt(BaseModel):
  class Meta(BaseModel.Meta):
    db_table = 'failed_login_attempts'

  ip_address = models.CharField(
      max_length=200, unique=False, null=False, blank=True, default='')
  email = models.EmailField(
      max_length=200, unique=False, null=False, blank=False)
  attempted_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'({self.id}){self.ip_address}, {email}, {attempted_at}'
