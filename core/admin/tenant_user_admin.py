from django.contrib import admin

from core import models


class TenantUserAdmin(admin.ModelAdmin):
  list_display = ('id', 'tenant_id', 'user_id', 'role_type', 'description',)
  list_display_links = list_display
  exclude = ('deleted_at',)
  search_fields = ('id', 'name',)
  ordering = ('id', 'tenant_id', 'user_id',)
