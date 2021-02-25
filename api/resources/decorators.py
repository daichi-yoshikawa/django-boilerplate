import logging
from box import Box
from functools import partial, wraps

from rest_framework.exceptions import ValidationError

from api import serializers
from api.common import exceptions
from core import models


logger = logging.getLogger(__name__)


def get_tenant_from_domain(**kwargs):
  if 'domain' not in kwargs:
    raise ValidationError('domain is missing in endpoint.')
  query = models.Tenant.objects.filter(domain=kwargs['domain'])
  if not query.exists():
    raise ValidationError(f'Tenant({kwargs["domain"]}) not found.')
  return query.get()

def get_tenant_user_from_request_and_tenant(request, tenant):
  query = models.TenantUser.objects.filter(
      tenant_id=tenant.id, user_id=request.user.id)
  if not query.exists():
    raise ValidationError(
        f'Tenant user(user_id: {request.user.id}, '
        f'domain:{tenant.domain}) not found.')
  return query.get()

def tenant_user_api(wrapped_func):
  def tenant_user_api_impl(*args, **kwargs):
    """
    args[0]: self
    args[1]: request
    args[2]: tenant_user
    """
    ret = { 'action': wrapped_func.__name__, }

    tenant = get_tenant_from_domain(**kwargs)
    tenant_user = get_tenant_user_from_request_and_tenant(
        request=args[1], tenant=tenant)
    serializer = serializers.TenantUserSerializer(tenant_user)
    args += (Box(serializer.data),)

    return wrapped_func(*args, **kwargs)
  return tenant_user_api_impl

def tenant_api(wrapped_func):
  def tenant_api_impl(*args, **kwargs):
    """
    args[0]: self
    args[1]: request
    args[2]: tenant
    """
    ret = { 'action': wrapped_func.__name__, }

    tenant = get_tenant_from_domain(**kwargs)
    serializer = serializers.TenantSerializer(tenant)
    args += (Box(serializer.data),)

    return wrapped_func(*args, **kwargs)
  return tenant_api_impl

def _user_data_api(wrapped_func, allow_pk_is_zero):
  @wraps(wrapped_func)
  def user_data_api_impl(*args, **kwargs):
    """
    args[0]: self
    args[1]: request
    """
    ret = { 'action': wrapped_func.__name__, }

    if 'pk' not in kwargs:
      raise ValidationError('pk is missing in endpoint.')
    pk = kwargs['pk']
    request = args[1]

    if pk == 0:
      if not allow_pk_is_zero:
        raise ValidationError('Invalid primary key.')
    elif pk != request.user.id:
      raise exceptions.OwnershipError(
          'Given pk and sender\'s user id not the same.')

    return wrapped_func(*args, **kwargs)
  return user_data_api_impl

user_data_api = partial(_user_data_api, allow_pk_is_zero=True)
strict_user_data_api = partial(_user_data_api, allow_pk_is_zero=False)
