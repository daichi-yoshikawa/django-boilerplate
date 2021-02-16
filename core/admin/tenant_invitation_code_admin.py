from django.contrib import admin

from core import models


class TenantInvitationCodeAdmin(admin.ModelAdmin):
  list_display = ('id', 'tenant_user_id', 'email', 'invitation_code',
                  'valid_until',)
  list_display_links = list_display
  exclude = ('deleted_at', 'invitation_code', 'valid_until',)
  search_fields = ('id', 'email',)
  ordering = ('id', 'valid_until',)

  def save_model(self, request, obj, form, change):
    if obj.invitation_code is None or obj.invitation_code == '':
      obj.set_invitation_code()
    obj.save()
