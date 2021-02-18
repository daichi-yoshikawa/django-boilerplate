from enum import Enum


class BUILTIN_USER(Enum):
  SYSTEM = 'system'
  ANONYMOUS = 'anonymous'


class TENANT_USER_ROLE_TYPE(Enum):
  GENERAL = 0
  ADMIN = 100
