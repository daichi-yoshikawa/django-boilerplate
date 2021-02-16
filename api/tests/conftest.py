import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'helpers'))

import pytest
from django.core.management import call_command
from django.db import connection
from pytest_django.lazy_django import skip_if_no_django

from rest_framework import status

from api import serializers
from core import models
from helpers.utils import *


@pytest.fixture()
def client():
  skip_if_no_django()
  from helpers.client import CustomClient
  return CustomClient()

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
  with django_db_blocker.unblock():
    call_command('reset_db', '--noinput')
    call_command('migrate')

@pytest.fixture()
def base_url():
  return os.path.join(os.environ['APP_DOMAIN'], '/api/v1')

@pytest.fixture(scope='class')
def reset_sequence(django_db_setup, django_db_blocker):
  def _reset_sequence(*args, **kwargs):
    model = args[0]
    with connection.cursor() as cursor:
      db_table = model._meta.db_table
      return cursor.execute(f'ALTER SEQUENCE {db_table}_id_seq RESTART WITH 1')
  return _reset_sequence

@pytest.fixture(scope='function')
def token(django_db_setup, client, base_url):
  def _token(*args, **kwargs):
    email = args[0]
    password = default_password() if len(args) == 1 else args[1]

    query = models.User.objects.filter(email=email)
    if query.count() == 0:
      raise RuntimeError(
          f'User(email) must be properly prepared before using client.')

    req = dict(data=dict(email=email, password=password))
    res = client.post(f'{base_url}/token/', req['data'])
    if res.status_code != status.HTTP_200_OK:
      raise RuntimeError(f'Failed to get token for user({email}).')

    if 'access' not in res.data:
      raise RuntimeError(f'Access token not found in response.')

    return res.data['access']
  return _token

@pytest.fixture(scope='function')
def bearer_token(token):
  def _bearer_token(*args, **kwargs):
    return f'Bearer {token(*args, **kwargs)}'
  return _bearer_token

@pytest.fixture(scope='function')
def email_verification_code(client, base_url):
  def _email_verification_code(*args, **kwargs):
    res = client.post(
        f'{base_url}/email/signup/verification/', { 'email': args[0] })
    if res.status_code != 200:
      raise RuntimeError(f'get_verification_code({args[0]}) failed.')
    return res.data['verification_code']
  return _email_verification_code

@pytest.fixture(scope='class')
def setup_users(django_db_blocker, reset_sequence):
  """Use this with non-transactional db"""
  with django_db_blocker.unblock():
    model = models.User
    model.objects.all().delete()
    reset_sequence(model)
    for seed in range(1, 11, 1):
      req = dict(data=signup_data(seed))
      user = model.objects.create(**req['data'])
      user.set_password(user.password)
      user.save()

@pytest.fixture(scope='class')
def setup_tenants(django_db_blocker, reset_sequence):
  with django_db_blocker.unblock():
    model = models.Tenant
    model.objects.all().delete()
    reset_sequence(model)
    for seed in range(1, 6, 1):
      req = dict(data=dict(name=tenant_name_from(seed)))
      tenant = model.objects.create(**req['data'])
      tenant.set_domain()
      tenant.save()

@pytest.fixture(scope='class')
def setup_tenant_users(django_db_blocker, setup_users, setup_tenants, reset_sequence):
  with django_db_blocker.unblock():
    model = models.TenantUser
    model.objects.all().delete()
    reset_sequence(model)

    requests = [
      dict(data=dict(tenant_id=1, user_id=1)),
      dict(data=dict(tenant_id=5, user_id=1)),
      dict(data=dict(tenant_id=2, user_id=2)),
      dict(data=dict(tenant_id=1, user_id=3)),
      dict(data=dict(tenant_id=3, user_id=3)),
    ]
    for req in requests:
      tenant_user = model.objects.create(**req['data'])
      tenant_user.save()
