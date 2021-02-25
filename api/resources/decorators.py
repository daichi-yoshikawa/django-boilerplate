import logging
from box import Box

from rest_framework.exceptions import ValidationError

from api import serializers
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
