import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'helpers'))

import json
import pytest
from rest_framework import status

from api.common import constants
from core import models
from helpers.utils import *


@pytest.mark.order(3)
@pytest.mark.django_db(transaction=True)
@pytest.mark.usefixtures(
    'django_db_setup', 'setup_users', 'setup_tenants', 'setup_tenant_users')
class TestTenant:
  @pytest.mark.parametrize('req, expected', [
    (dict(user_id=1), dict(tenants=[dict(id=1), dict(id=5)], status=200)),
    (dict(user_id=5), dict(tenants=[], status=200)),
  ])
  def test_get_user_tenants(self, client, base_url, bearer_token, req, expected):
    # Execution
    res = client.get(
        f'{base_url}/users/{req["user_id"]}/tenants/',
        bearer_token=bearer_token(email_from(req['user_id'])),
        check_auth_guard=is_ok(expected['status']))
    assert res.status_code == expected['status']

    # if status is error...
    if not is_ok(res.status_code):
      return

    # if status is ok...
    assert len(res.data['tenants']) == len(expected['tenants'])
    if len(expected['tenants']) > 0:
      expected_tenant_ids = [tenant['id'] for tenant in expected['tenants']]
      for tenant in res.data['tenants']:
        assert tenant['id'] in expected_tenant_ids

  @pytest.mark.parametrize('req, expected', [
    (dict(user_id=1, data=dict(name=tenant_name_from(101))), dict(status=200)),
    (dict(user_id=1, data=dict(name=tenant_name_from(102))), dict(status=200)),
    (dict(user_id=1, data=dict(name=tenant_name_from(103))), dict(status=200)),
  ])
  def test_create_tenant(self, client, bearer_token, base_url, req, expected):
    # Preprocess
    model = models.Tenant
    n_data = model.objects.all().count()

    # Execution
    res = client.post(
        f'{base_url}/tenants/', req['data'],
        bearer_token=bearer_token(email_from(req['user_id'])),
        check_auth_guard=is_ok(expected['status']))
    assert res.status_code == expected['status']

    # Common postprocess
    query = model.objects.filter(name=req['data']['name'])

    # If status is error...
    if not is_ok(res.status_code):
      assert n_data == model.objects.all().count()
      assert not query.exists()
      return

    # If status is ok...
    assert n_data + 1 == model.objects.all().count()
    assert query.exists()
    tenant_id = model.objects.get(name=req['data']['name']).id
    query = models.TenantUser.objects.filter(
        tenant_id=tenant_id, user_id=req['user_id'])
    assert query.exists()
    assert query.get().role_type == constants.TENANT_USER_ROLE_TYPE.ADMIN.value

  @pytest.mark.parametrize('req, expected', [
    (dict(data=dict(user_id=1, tenant_id=1)), dict(status=200)),
    (dict(data=dict(user_id=1, tenant_id=2)), dict(status=500)),
  ])
  def test_get_tenant(self, client, base_url, bearer_token, req, expected):
    # Preprocess
    domain = get_domain(pk=req['data']['tenant_id'])

    # Execution
    res = client.get(
        f'{base_url}/tenants/{domain}/',
        bearer_token=bearer_token(email_from(req['data']['user_id'])),
        check_auth_guard=is_ok(expected['status']))
    assert res.status_code == expected['status']

    # if status is error...
    if not is_ok(res.status_code):
      return

    # if status is ok...
    assert res.data['name'] == tenant_name_from(req['data']['tenant_id'])

  @pytest.mark.parametrize('req, expected', [
    (dict(user_id=1, tenant_id=1, tgt_tenant_id=1, data=[dict(
        tenant_id=1, email=email_from(seed=4))]),
     dict(status=200)),
    (dict(user_id=1, tenant_id=1, tgt_tenant_id=2, data=[dict(
        tenant_id=2, email=email_from(seed=5))]),
     dict(status=500)),
  ])
  def test_create_tenant_invitation_code(
      self, client, base_url, bearer_token, req, expected, settings):
    # Preprocess
    model = models.TenantInvitationCode
    n_data = model.objects.all().count()
    domain = get_domain(req['tgt_tenant_id'])

    # Execution
    req['data'][0]['tenant_user_id'] = get_tenant_user_id(
        tenant_id=req['tenant_id'], user_id=req['user_id'])
    res = client.post(
        f'{base_url}/tenants/{domain}/invitation_codes/', req['data'],
        bearer_token=bearer_token(email_from(req['user_id'])),
        check_auth_guard=is_ok(expected['status']))
    assert res.status_code == expected['status']

    # Common postprocess
    query = model.objects.filter(email=req['data'][0]['email'])

    # if status is error...
    if not is_ok(res.status_code):
      assert n_data == model.objects.all().count()
      assert not query.exists()
      return

    # if status is ok...
    assert n_data + 1 == model.objects.all().count()
    assert query.exists()
    assert len(query.get().invitation_code) == (
        settings.TENANT_INVITATION_CODE_LENGTH)

  @pytest.mark.parametrize('req, expected', [
    (dict(user_id=5, tenant_id=1, data=dict(email=email_from(seed=4))),
     dict(status=403)),
    (dict(user_id=4, tenant_id=1, data=dict(email=email_from(seed=4))),
     dict(status=200)),
  ])
  def test_retrieve_invited_tenant(
      self, client, base_url, bearer_token, req, expected):
    # Preprocess
    bearer_token = bearer_token(email_from(seed=req['user_id']))
    email = seed=req['data']['email']
    query = models.TenantInvitationCode.objects.filter(email=email)
    req['data']['invitation_code'] = query.get().invitation_code

    # Execution
    res = client.post(
        f'{base_url}/tenants/invited/', req['data'],
        bearer_token=bearer_token,
        check_auth_guard=is_ok(expected['status']))
    assert res.status_code == expected['status']

    # if status is error...
    if not is_ok(res.status_code):
      return

    # if status is ok...
    assert res.data['id'] == req['tenant_id']

  @pytest.mark.parametrize('req, expected', [
    (dict(user_id=4, tenant_id=2, user_id_to_get_invitation_code=4),
     dict(status=400)),
    (dict(user_id=5, tenant_id=1, user_id_to_get_invitation_code=4),
     dict(status=500)),
    (dict(user_id=4, tenant_id=1, user_id_to_get_invitation_code=4),
     dict(status=201)),
  ])
  def test_create_tenant_user(self, client, base_url, bearer_token, req, expected):
    # Preprocess
    model = models.TenantUser
    n_data = model.objects.all().count()
    domain = get_domain(req['tenant_id'])
    email = email_from(req['user_id_to_get_invitation_code'])
    query = models.TenantInvitationCode.objects.filter(email=email)
    invitation_code = query.get().invitation_code
    req['data'] = dict(
        tenant_id=req['tenant_id'], user_id=req['user_id'],
        invitation_code=invitation_code)

    # Execution
    res = client.post(
        f'{base_url}/tenants/{domain}/users/', req['data'],
        bearer_token=bearer_token(email_from(req['user_id'])),
        check_auth_guard=is_ok(expected['status']))
    assert res.status_code == expected['status']

    # Common postprocess
    query = model.objects.filter(
        tenant_id=req['data']['tenant_id'], user_id=req['data']['user_id'])

    # if status is error...
    if not is_ok(res.status_code):
      assert n_data == model.objects.all().count()
      assert not query.exists()
      return

    # if status is ok...
    assert n_data + 1 == model.objects.all().count()
    assert query.exists()
    assert res.data['tenant']['id'] == req['data']['tenant_id']
    assert res.data['user']['id'] == req['data']['user_id']

  @pytest.mark.parametrize('req, expected', [
    (dict(user_id=1, tenant_id=1, tgt_tenant_user_id=1), dict(status=200)),
    (dict(user_id=1, tenant_id=5, tgt_tenant_user_id=1), dict(status=500)),
    (dict(user_id=1, tenant_id=5, tgt_tenant_user_id=3), dict(status=500)),
  ])
  def test_get_tenant_user(self, client, base_url, bearer_token, req, expected):
    # Preprocess
    domain = get_domain(req['tenant_id'])

    # Execution
    res = client.get(
        f'{base_url}/tenants/{domain}/users/{req["tgt_tenant_user_id"]}/',
        bearer_token=bearer_token(email_from(req['user_id'])),
        check_auth_guard=is_ok(expected['status']))
    assert res.status_code == expected['status']

    # if status is error...
    if not is_ok(res.status_code):
      return

    # if status is ok...
    assert res.data['tenant']['id'] == req['tenant_id']
    assert res.data['user']['id'] == req['user_id']
    assert res.data['id'] == req['tgt_tenant_user_id']
