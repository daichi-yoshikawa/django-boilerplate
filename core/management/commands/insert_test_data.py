from django.core.management import call_command

from .test_data_command import TestDataCommand


class Command(TestDataCommand):
  RESOURCES = [
    'users', 'tenants', 'tenant_users',
  ]

  def insert_data(self):
    for resource in self.RESOURCES:
      call_command(f'insert_test_{resource}')
