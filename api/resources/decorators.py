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
    raise ValidationError(f'Tenant not found.')
  return query.get()


def get_tenant_user_from_request_and_tenant(request, tenant):
  query = models.TenantUser.objects.filter(
      tenant_id=tenant.id, user_id=request.user.id)
  if not query.exists():
    raise ValidationError('Tenant user in the domain not found.')
  return query.get()


def get_tenant_user_from_request_and_tenant_and_tenant_user_id(
    request, tenant, **kwargs):
  if 'tenant_user_id' not in kwargs:
    raise ValidationError('tenant_user_id is missing in endpoint.')
  tenant_user_id = kwargs['tenant_user_id']

  query = models.TenantUser.objects.filter(
      pk=tenant_user_id, tenant_id=tenant.id, user_id=request.user.id)
  if not query.exists():
    raise ValidationError(
        'Tenant user with the user id and the domain not found.')
  return query.get()


def get_tenant_user_from_tenant_and_url_param(tenant, **kwargs):
  if 'tenant_user_id' not in kwargs:
    raise ValidationError('tenant_user_id is missing in endpoint.')
  tenant_user_id = kwargs['tenant_user_id']

  query = models.TenantUser.objects.filter(
      pk=tenant_user_id, tenant_id=tenant.id)
  if not query.exists():
    raise ValidationError('Tenant user in the domain not found.')
  return query.get()


def tenant_user_data_api(wrapped_func):
  """
  API will have arguments as below.
  @shared_tenant_user_data_api
  def get(self, request, tenant_user, domain, tenant_user_id, xxx),
  where tenant_user is derived from request.user.id and domain,
  and tenant_user_id is derived from endpoint.
  """
  def tenant_user_data_api_impl(*args, **kwargs):
    """
    args[0]: self
    args[1]: request
    args[2]: tenant_user
    """
    ret = { 'action': wrapped_func.__name__, }

    tenant = get_tenant_from_domain(**kwargs)
    tenant_user = get_tenant_user_from_request_and_tenant(
        request=args[1], tenant=tenant)
    _ = get_tenant_user_from_tenant_and_url_param(
        tenant=tenant, **kwargs)
    serializer = serializers.TenantUserSerializer(tenant_user)
    args += (Box(serializer.data),)

    return wrapped_func(*args, **kwargs)
  return tenant_user_data_api_impl


def self_tenant_user_data_api(wrapped_func):
  def self_tenant_user_data_api_impl(*args, **kwargs):
    """
    args[0]: self
    args[1]: request
    args[2]: tenant_user
    """
    ret = { 'action': wrapped_func.__name__, }

    tenant = get_tenant_from_domain(**kwargs)
    tenant_user = get_tenant_user_from_request_and_tenant_and_tenant_user_id(
        request=args[1], tenant=tenant, **kwargs)
    serializer = serializers.TenantUserSerializer(tenant_user)
    args += (Box(serializer.data),)

    return wrapped_func(*args, **kwargs)
  return self_tenant_user_data_api_impl


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


def tenant_admin_api(wrapped_func):
  def tenant_admin_api_impl(*args, **kwargs):
    """
    args[0]: self
    args[1]: request
    args[2]: tenant_user
    """
    ret = { 'action': wrapped_func.__name__, }

    tenant = get_tenant_from_domain(**kwargs)
    tenant_user = get_tenant_user_from_request_and_tenant(
        request=args[1], tenant=tenant)
    if tenant_user.role_type != constants.TENANT_USER_ROLE_TYPE.ADMIN.value:
      raise PermissionDenied('Operation is only allowed by tenant admin.')

    serializer = serializers.TenantUserSerializer(tenant_user)
    args += (Box(serializer.data),)

    return wrapped_func(*args, **kwargs)
  return tenant_admin_api_impl


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


def _user_data_api(wrapped_func, allow_user_id_is_zero):
  @wraps(wrapped_func)
  def user_data_api_impl(*args, **kwargs):
    """
    args[0]: self
    args[1]: request
    """
    ret = { 'action': wrapped_func.__name__, }

    if 'user_id' not in kwargs:
      raise ValidationError('user_id is missing in endpoint.')
    user_id = kwargs['user_id']
    request = args[1]

    if user_id == 0:
      if not allow_user_id_is_zero:
        raise ValidationError('Invalid primary key.')
    elif user_id != request.user.id:
      raise exceptions.OwnershipError(
          'Given user_id and sender\'s user id not the same.')

    return wrapped_func(*args, **kwargs)
  return user_data_api_impl

soft_user_data_api = partial(_user_data_api, allow_user_id_is_zero=True)
user_data_api = partial(_user_data_api, allow_user_id_is_zero=False)
