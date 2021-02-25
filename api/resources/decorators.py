import logging
from box import Box

from rest_framework.exceptions import ValidationError

from api import serializers
from core import models


logger = logging.getLogger(__name__)

def tenant_user_api(wrapped_func):
  def tenant_user_api_impl(*args, **kwargs):
    """
    args[0]: self
    args[1]: request
    args[2]: tenant_user
    """
    ret = { 'action': wrapped_func.__name__, }

    if 'domain' not in kwargs:
      raise ValidationError('domain is missing in endpoint.')
    query = models.Tenant.objects.filter(domain=kwargs['domain'])
    if not query.exists():
      raise ValidationError(
          f'Tenant({kwargs["domain"]}) not found.')
    tenant_id = query.get().id

    request = args[1]
    query = models.TenantUser.objects.filter(
        tenant_id=tenant_id, user_id=request.user.id)
    if not query.exists():
      raise ValidationError(
          f'Tenant user(user_id: {request.user.id}, '
          f'domain:{kwargs["domain"]}) not found.')
    serializer = serializers.TenantUserSerializer(query.get())
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

    if 'domain' not in kwargs:
      raise ValidationError('domain is missing in endpoint.')
    tenant = models.Tenant.objects.get(domain=kwargs['domain'])
    serializer = serializers.TenantSerializer(tenant)
    args += (Box(serializer.data),)

    return wrapped_func(*args, **kwargs)
  return tenant_api_impl
