from .constants import TENANT_USERS
from .test_data_command import TestDataCommand
from core import models


class Command(TestDataCommand):
  def insert_data(self):
    for _, (user_id, tenant_id, role_type) in TENANT_USERS.items():
      req = dict(user_id=user_id, tenant_id=tenant_id, role_type=role_type)
      obj = models.TenantUser(**req)
      obj.save()
