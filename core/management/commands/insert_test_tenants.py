from .constants import N_TENANTS
from .test_data_command import TestDataCommand
from core import models


class Command(TestDataCommand):
  def insert_data(self):
    for tenant_id in range(1, N_TENANTS+1, 1):
      req = dict(name=f'Tenant{str(tenant_id).zfill(3)}')
      tenant = models.Tenant(**req)
      tenant.set_domain()
      tenant.save()
