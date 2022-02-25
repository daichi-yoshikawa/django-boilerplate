from enum import Enum


class BUILTIN_USER(Enum):
  SYSTEM = 'system'
  ANONYMOUS = 'anonymous'


class TENANT_USER_ROLE_TYPE(Enum):
  GENERAL = 0
  ADMIN = 100


SEARCH_USER_SIMILARITY_THRESHOLD = 0.8
