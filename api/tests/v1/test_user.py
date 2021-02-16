import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'helpers'))

import pytest
from rest_framework import status

from core import models
from helpers.utils import *


@pytest.mark.order(1)
@pytest.mark.django_db
@pytest.mark.usefixtures('django_db_setup')
class TestUserSignUp:
  @pytest.mark.parametrize('req, expected', [
    (dict(data=dict(email=email_from(1))), dict(status=200)),
  ])
  def test_email_verification(self, client, base_url, req, expected, settings):
    # Preprocess
    model = models.EmailVerificationCode
    n_data = model.objects.all().count()

    # Execution
    res = client.post(f'{base_url}/email/signup/verification/', req['data'])
    assert res.status_code == expected['status']

    # Common postprocess
    query = model.objects.filter(email=req['data']['email'])

    # If status is error...
    if not is_ok(res.status_code):
      assert n_data == model.objects.all().count()
      assert query.count() == 0
      return

    # If status is ok...
    assert n_data + 1 == model.objects.all().count()
    assert query.count() > 0
    assert res.data['email'] == req['data']['email']
    assert len(res.data['verification_code']) > 0
    assert len(res.data['verification_code']) == settings.EMAIL_VERIFICATION_CODE_LENGTH

  @pytest.mark.parametrize('req, expected', [
    (dict(seed=1, data=signup_data(seed=1)), dict(status=201)),
    (dict(seed=2, data=signup_data(seed=2), not_verified=True),
     dict(status=400)),
  ])
  def test_signup_user(
      self, client, base_url, req, expected, email_verification_code):
    # Preprocess
    model = models.User
    n_data = model.objects.all().count()
    if not 'not_verified' in req:
      req['data']['verification_code'] = (
          email_verification_code(email_from(req['seed'])))

    # Execution
    res = client.post(f'{base_url}/users/', req['data'])
    assert res.status_code == expected['status']

    # Common postprocess
    query = model.objects.filter(
        first_name=req['data']['first_name'], last_name=req['data']['last_name'],
        email=req['data']['email'])

    # If status is error...
    if not is_ok(res.status_code):
      assert n_data == model.objects.all().count()
      assert query.count() == 0
      return

    assert n_data + 1 == model.objects.all().count()
    assert query.count() == 1
    assert 'password' not in res
    for field in ['first_name', 'last_name', 'email']:
      assert res.data[field] == req['data'][field]

  def test_signup_duplicate_user(
      self, client, base_url, email_verification_code):
    # Preprocess
    model = models.User
    n_users = model.objects.all().count()
    req = dict(data=signup_data(1))

    # Execution and check
    for i in range(2):
      req['data']['verification_code'] = email_verification_code(email_from(1))
      res = client.post(f'{base_url}/users/', req['data'])
      expected = 201 if i == 0 else 400
      assert res.status_code == expected


@pytest.mark.order(2)
@pytest.mark.django_db(transaction=True)
@pytest.mark.usefixtures('django_db_setup', 'setup_users')
class TestUser:
  @pytest.mark.parametrize('req, expected', [
    (dict(data=login_data(seed=1)), dict(status=200)),
    (dict(data=login_data(seed=1, overwrite={ 'password': 'abcdabcd' })),
     dict(status=500)),
    (dict(data=login_data(seed=999)), dict(status=500)),
  ])
  def test_login(self, client, base_url, req, expected):
    # Execution
    res = client.post(f'{base_url}/token/', req['data'])
    assert res.status_code == expected['status']

    # If status is error...
    if not is_ok(res.status_code):
      return

    # If status is ok...
    for key in ['access', 'refresh']:
      assert key in res.data
      assert len(res.data[key]) > 0
    for key in ['access_expires_in', 'refresh_expires_in']:
      assert key in res.data
      assert int(res.data[key]) > 0

  @pytest.mark.parametrize('req, expected', [
    (dict(my_seed=2, tgt_seed=2), dict(status=200)),
    (dict(my_seed=2, tgt_seed=1), dict(status=403)),
  ])
  def test_retrieve_user(self, client, bearer_token, base_url, req, expected):
    # Execution
    res = client.get(
        f'{base_url}/users/{req["tgt_seed"]}/',
        bearer_token=bearer_token(email_from(req['my_seed'])),
        check_auth_guard=is_ok(expected['status']))
    assert res.status_code == expected['status']

    # If status is error...
    if not is_ok(res.status_code):
      for field in ['email', 'first_name', 'last_name']:
        assert field not in res.data
      return

    # If status is ok...
    assert email_from(req['my_seed']) == res.data['email']
    assert first_name_from(req['my_seed']) == res.data['first_name']
    assert last_name_from(req['my_seed']) == res.data['last_name']

  @pytest.mark.parametrize('req, expected', [
    (dict(my_seed=2, tgt_seed=1, data=dict(
        first_name='f002', last_name='l002', email='a002@a.com')),
     dict(status=403)),
    (dict(my_seed=2, tgt_seed=2, data=dict(
        first_name='f002', last_name='l002', email='a002@a.com')),
     dict(status=200)),
  ])
  def test_update_user(self, client, bearer_token, base_url, req, expected):
    # Execution
    res = client.put(
        f'{base_url}/users/{req["tgt_seed"]}/', req['data'],
        bearer_token=bearer_token(email_from(req['my_seed'])),
        check_auth_guard=is_ok(expected['status']))
    assert res.status_code == expected['status']

    # If status is error...
    if not is_ok(res.status_code):
      return

    # If status is ok...
    for field in ['email', 'first_name', 'last_name']:
      assert res.data[field] == req['data'][field]

  @pytest.mark.parametrize('req, expected', [
    (dict(my_seed=1, tgt_seed=1, data=dict(
        password='wrong_password', new_password='new_password')),
     dict(status=400)),
    (dict(my_seed=1, tgt_seed=3, data=dict(
        password=default_password(), new_password='new_password')),
     dict(status=403)),
    (dict(my_seed=1, tgt_seed=1, data=dict(
        password=default_password(), new_password='new_password')),
     dict(status=200)),
  ])
  def test_update_user_password(
      self, client, bearer_token, base_url, req, expected):
    # Execution
    res = client.put(
        f'{base_url}/users/{req["tgt_seed"]}/password/', req['data'],
        bearer_token=bearer_token(email_from(req['my_seed'])),
        check_auth_guard=is_ok(expected['status']))
    assert res.status_code == expected['status']

    # If status is error...
    if not is_ok(res.status_code):
      res = client.post(f'{base_url}/token/', login_data(req['my_seed']))
      assert res.status_code == status.HTTP_200_OK
      res = client.post(f'{base_url}/token/', login_data(req['tgt_seed']))
      assert res.status_code == status.HTTP_200_OK
      return

    # If status is ok...
    res = client.post(f'{base_url}/token/', login_data(req['my_seed']))
    assert res.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    new_password = req['data']['new_password']
    req = dict(data=login_data(req['tgt_seed']))
    req['data'].update(dict(password=new_password))
    res = client.post(f'{base_url}/token/', req['data'])
    assert res.status_code == status.HTTP_200_OK

  @pytest.mark.parametrize('req, expected', [
    (dict(my_seed=3, tgt_seed=1), dict(status=403)),
    (dict(my_seed=3, tgt_seed=3), dict(status=200)),
  ])
  def test_delete_user(self, client, bearer_token, base_url, req, expected):
    model = models.User
    n_data = model.objects.all().count()

    # Execution
    res = client.delete(
        f'{base_url}/users/{req["tgt_seed"]}/',
        bearer_token=bearer_token(email_from(req['my_seed'])),
        check_auth_guard=is_ok(expected['status']))
    assert res.status_code == expected['status']

    # Common postprocess
    query = model.objects.filter(email=email_from(req['tgt_seed']))

    # if status is error...
    if not is_ok(res.status_code):
      assert n_data == model.objects.all().count()
      assert query.exists()
      return

    # if status is ok...
    assert n_data - 1 == model.objects.all().count()
    assert not query.exists()

@pytest.mark.order(3)
@pytest.mark.django_db(transaction=True)
@pytest.mark.usefixtures('django_db_setup', 'setup_users')
class TestPasswordReset:
  @pytest.mark.parametrize('req, expected', [
    (dict(data=dict(email=email_from(seed=1))), dict(status=200)),
    (dict(data=dict(email=email_from(seed=2))), dict(status=200)),
  ])
  def test_create_password_reset_code(self, client, base_url, req, expected):
    # Preprocess
    model = models.PasswordResetCode
    n_data = model.objects.all().count()

    # Execution
    res = client.post(f'{base_url}/password/reset-code/', req['data'])
    assert res.status_code == expected['status']

    # Common postprocess
    query = model.objects.filter(email=req['data']['email'])

    # if status is error...
    if not is_ok(res.status_code):
      assert n_data == model.objects.all().count()
      assert not query.exists()
      return

    # if status is ok...
    assert n_data + 1 == model.objects.all().count()
    assert query.exists()

  @pytest.mark.parametrize('req, expected', [
    (dict(user_id=1, email_to_get_reset_code=email_from(seed=2),
          data=dict(email=email_from(seed=1), password='reset_password')),
     dict(status=400)),
    (dict(user_id=1, email_to_get_reset_code=email_from(seed=1),
          data=dict(email=email_from(seed=1), password='reset_password')),
     dict(status=200)),
  ])
  def test_reset_password(self, client, base_url, req, expected):
    # Preprocess
    model = models.PasswordResetCode
    query = model.objects.filter(email=req['email_to_get_reset_code'])
    reset_code = query.get().reset_code
    n_data = model.objects.all().count()
    req['data']['reset_code'] = reset_code

    # Execution
    res = client.post(f'{base_url}/password/reset/', req['data'])
    assert res.status_code == expected['status']

    # Common postprocess
    req_login = dict(data=dict(
        email=req['email_to_get_reset_code'], password=req['data']['password']))
    res_login = client.post(f'{base_url}/token/', req_login['data'])

    # if status is error...
    if not is_ok(res.status_code):
      assert n_data == model.objects.all().count()
      assert query.exists()
      assert not is_ok(res_login.status_code)
      return

    # if status is ok...
    assert n_data - 1 == model.objects.all().count()
    assert not query.exists()
    assert is_ok(res_login.status_code)

