import csv
import os

from django.core.management.base import BaseCommand

from core import models


DATA_PATH = 'core/management/data'

class Command(BaseCommand):
  help = 'Drop all tables in DB specified in settings.py.'

  def handle(self, *args, **kwargs):
    self.insert_users()
    self.insert_tenants()
    self.insert_tenant_users()

  def read_csv_data(self, filename, dtypes=dict()):
    rows = []

    with open(os.path.join(DATA_PATH, filename), newline='') as f:
      reader = csv.DictReader(f, delimiter=',', quotechar='|')
      for row in reader:
        rows.append(row)

    for col, dtype in dtypes.items():
      if (row[col] is None) | (row[col] == ''):
        continue
      row[col] = dtype(row[col])

    return rows

  def insert_users(self):
    print('Insert users.')
    rows = self.read_csv_data('users.csv')
    for row in rows:
      if models.User.objects.filter(email=row['email']).exists():
        continue
      user = models.User(**row)
      user.set_password(row['password'])
      user.save()
    print(f'users count: {len(rows)}')

  def insert_tenants(self):
    print('Insert tenants.')
    rows = self.read_csv_data('tenants.csv')
    for i, row in enumerate(rows):
      pk = i + 1
      if models.Tenant.objects.filter(pk=pk).exists():
        continue
      tenant = models.Tenant(**row)
      tenant.set_domain()
      tenant.save()
    print(f'tenants count: {len(rows)}')

  def insert_tenant_users(self):
    print('Insert tenant_users.')
    rows = self.read_csv_data(
        'tenant_users.csv', {'tenant_id': int, 'user_id': int})
    for i, row in enumerate(rows):
      pk = i + 1
      if models.TenantUser.objects.filter(pk=pk).exists():
        continue
      tenant_user = models.TenantUser(**row)
      tenant_user.save()
    print(f'tenant_users count: {len(rows)}')
