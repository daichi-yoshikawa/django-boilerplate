from django.contrib import admin

from core import models


class EmailVerificationCodeAdmin(admin.ModelAdmin):
  list_display = ('id', 'email', 'verification_code', 'valid_until',)
  list_display_links = list_display
  exclude = ('deleted_at', 'verification_code', 'valid_until',)
  search_fields = ('id', 'email',)
  ordering = ('id', 'valid_until',)

  def save_model(self, request, obj, form, change):
    if obj.verification_code is None or obj.verification_code == '':
      obj.set_verification_code()
    obj.save()
