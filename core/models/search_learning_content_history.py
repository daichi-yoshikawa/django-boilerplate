from django.db import models

from core.models.base_models import BaseTenantModel


class SearchLearningContentHistory(BaseTenantModel):
  class Meta:
    db_table = 'search_learning_content_histories'

  by_tenant_user = models.ForeignKey(
      'TenantUser', unique=False, null=True, blank=False,
      on_delete=models.SET_NULL)
  search_text = models.CharField(
      max_length=1000, unique=False, null=False, blank=False)

  def __str__(self):
    return (f'({self.id}){self.tenant.name}, '
            f'{self.by_tenant_user}, '
            f'{self.search_text}')
