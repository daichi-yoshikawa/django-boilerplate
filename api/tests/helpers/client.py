import json

from django.test.client import Client
from rest_framework import status


class CustomClient(Client):
  def get(
      self, path, data=None, follow=False, secure=False,
      content_type='application/json', bearer_token='', check_auth_guard=False, **extra):

    if check_auth_guard:
      res = self._request(
        method='GET', path=path, data=data, follow=follow, secure=secure,
        content_type=content_type, bearer_token='', **extra)
      assert res.status_code == status.HTTP_401_UNAUTHORIZED

    return self._request(
        method='GET', path=path, data=data, follow=follow, secure=secure,
        content_type=content_type, bearer_token=bearer_token, **extra)

  def post(
      self, path, data=None, follow=False, secure=False,
      content_type='application/json', bearer_token='',
      check_auth_guard=False, **extra):

    if check_auth_guard:
      res = self._request(
        method='POST', path=path, data=data, follow=follow, secure=secure,
        content_type=content_type, bearer_token='', **extra)
      assert res.status_code == status.HTTP_401_UNAUTHORIZED

    return self._request(
        method='POST', path=path, data=data, follow=follow, secure=secure,
        content_type=content_type, bearer_token=bearer_token, **extra)

  def put(
      self, path, data='', follow=False, secure=False,
      content_type='application/json', bearer_token='',
      check_auth_guard=False, **extra):

    if check_auth_guard:
      res = self._request(
        method='PUT', path=path, data=data, follow=follow, secure=secure,
        content_type=content_type, bearer_token='', **extra)
      assert res.status_code == status.HTTP_401_UNAUTHORIZED

    res = self._request(
        method='PUT', path=path, data=data, follow=follow, secure=secure,
        content_type=content_type, bearer_token=bearer_token, **extra)
    return res

  def patch(
      self, path, data='', follow=False, secure=False,
      content_type='application/json', bearer_token='',
      check_auth_guard=False, **extra):

    if check_auth_guard:
      res = self._request(
        method='PATCH', path=path, data=data, follow=follow, secure=secure,
        content_type=content_type, bearer_token='', **extra)
      assert res.status_code == status.HTTP_401_UNAUTHORIZED

    res = self._request(
        method='PATCH', path=path, data=data, follow=follow, secure=secure,
        content_type=content_type, bearer_token=bearer_token, **extra)
    return res

  def delete(
      self, path, data='', follow=False, secure=False,
      content_type='application/json', bearer_token='',
      check_auth_guard=False, **extra):

    if check_auth_guard:
      res = self._request(
        method='DELETE', path=path, data=data, follow=follow, secure=secure,
        content_type=content_type, bearer_token='', **extra)
      assert res.status_code == status.HTTP_401_UNAUTHORIZED

    res = self._request(
        method='DELETE', path=path, data=data, follow=follow, secure=secure,
        content_type=content_type, bearer_token=bearer_token, **extra)
    return res

  def _request(
      self, method, path, data, follow, secure, content_type, bearer_token, **extra):
    args = dict(
        path=path, data=data, follow=follow, secure=secure,
        content_type=content_type)
    auth_header = {'HTTP_AUTHORIZATION': bearer_token} if bearer_token else {}

    res = None
    method = method.upper()
    if method == 'GET':
      args.pop('content_type')
      extra['CONTENT_TYPE'] = content_type
      res = super().get(**args, **auth_header, **extra)
    elif method == 'POST':
      res = super().post(**args, **auth_header, **extra)
    elif method == 'PUT':
      res = super().put(**args, **auth_header, **extra)
    elif method == 'PATCH':
      res = super().patch(**args, **auth_header, **extra)
    elif method == 'DELETE':
      res = super().delete(**args, **auth_header, **extra)
    else:
      raise ValueError(f'Unsupported HTTP request type:{method} is called.')

    return res
