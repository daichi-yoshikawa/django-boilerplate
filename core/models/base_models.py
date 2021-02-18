from django.contrib import auth
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):
  class Meta:
    abstract = True
    ordering = ['-updated_at']

  created_by = models.CharField(
      max_length=20, unique=False, null=False, blank=False, default='system')
  updated_by = models.CharField(
      max_length=20, unique=False, null=False, blank=False, default='system')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  deleted_at = models.DateTimeField(unique=False, null=True, blank=False)


class UserManager(BaseUserManager):
  """
  This class is implemented by referring to
  django.contrib.auth.models.UserManager (django-3.1.4).
  Majorly fixing part relevant to variable "username".
  """
  use_in_migrations = True

  def _create_user(self, first_name, last_name, email, password, **extra_fields):
    email = self.normalize_email(email)
    user = self.model(
        first_name=first_name, last_name=last_name, email=email, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(
      self, first_name, last_name, email, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', False)
    extra_fields.setdefault('is_superuser', False)
    return self._create_user(
        first_name, last_name, email, password, **extra_fields)

  def create_superuser(
      self, first_name, last_name, email, password, **extra_fields):
    print('hoghoge')
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)

    if extra_fields.get('is_staff') is not True:
      raise ValueError('Superuser must have is_staff=True.')
    if extra_fields.get('is_superuser') is not True:
      raise ValueError('Superuser must have is_superuser=True.')

    return self._create_user(first_name, last_name, email, password, **extra_fields)

  def with_perm(
      self, perm, is_active=True, include_superusers=True, backend=None,
      obj=None):
    if backend is None:
      backends = auth._get_backends(return_tuples=True)
      if len(backends) == 1:
        backend, _ = backends[0]
      else:
        raise ValueError(
          'You have multiple authentication backends configured and '
          'therefore must provide the `backend` argument.'
        )
    elif not isinstance(backend, str):
      raise TypeError(
        'backend must be a dotted import path string (got %r).'
        % backend
      )
    else:
      backend = auth.load_backend(backend)
    if hasattr(backend, 'with_perm'):
      return backend.with_perm(
          perm,
          is_active=is_active,
          include_superusers=include_superusers,
          obj=obj,
      )
    return self.none()


class BaseUserModel(AbstractUser):
  class Meta:
    abstract = True
    ordering = ['-updated_at']

  username = None
  created_by = models.CharField(
      max_length=20, unique=False, null=False, blank=False, default='system')
  updated_by = models.CharField(
      max_length=20, unique=False, null=False, blank=False, default='system')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  deleted_at = models.DateTimeField(unique=False, null=True, blank=False)

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name', 'last_name',]


class BaseTenantModel(BaseModel):
  class Meta:
    abstract = True
    ordering = ['-updated_at']

  tenant = models.ForeignKey(
      'Tenant', unique=False, null=False, blank=False, on_delete=models.CASCADE)
