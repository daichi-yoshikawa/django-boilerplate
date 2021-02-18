from django.db import models

from core.models.base_models import BaseModel


class EmailChange(BaseModel):
  class Meta(BaseModel.Meta):
    db_table = 'email_changes'

  user = models.ForeignKey(
      'User', unique=False, null=False, blank=False,
      on_delete=models.CASCADE)
  new_email = models.EmailField(
      max_length=200, unique=False, null=False, blank=False)
  verification_code = models.CharField(
      max_length=200, unique=True, null=False, blank=False)
  valid_until = models.DateTimeField(unique=False, null=False, blank=False)

  def __str__(self):
    return (f'({self.id}){self.user.email}, '
            f'{self.new_email}, '
            f'{self.verification_code}')
