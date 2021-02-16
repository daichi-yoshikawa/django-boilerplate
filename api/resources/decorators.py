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
    tenant_id = models.Tenant.objects.get(domain=kwargs['domain']).id

    request = args[1]
    tenant_user = models.TenantUser.objects.get(
        tenant_id=tenant_id, user_id=request.user.id)
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

    if 'domain' not in kwargs:
      raise ValidationError('domain is missing in endpoint.')
    tenant = models.Tenant.objects.get(domain=kwargs['domain'])
    serializer = serializers.TenantSerializer(tenant)
    args += (Box(serializer.data),)

    return wrapped_func(*args, **kwargs)
  return tenant_api_impl
