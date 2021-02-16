from django.contrib import admin

from core import models


class PasswordResetCodeAdmin(admin.ModelAdmin):
  list_display = ('id', 'email', 'reset_code', 'valid_until',)
  list_display_links = list_display
  exclude = ('deleted_at', 'reset_code', 'valid_until',)
  search_fields = ('id', 'email',)
  ordering = ('id', 'valid_until',)

  def save_model(self, request, obj, form, change):
    if obj.reset_code is None or obj.reset_code == '':
      obj.set_reset_code()
    obj.save()
