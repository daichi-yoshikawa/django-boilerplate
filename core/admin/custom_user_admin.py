from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from core import forms


class CustomUserAdmin(UserAdmin):
  fieldsets = (
    (None, {'fields': ('first_name', 'last_name', 'email', 'password', 'image',
                       'status', 'language_code', 'timezone_code',)}),
  )
  add_fieldsets = (
      (None, {
        'classes': ('wide',),
        'fields': ('first_name', 'last_name', 'email', 'password1', 'password2',
                   'image', 'status', 'language_code', 'timezone_code',),
      }),
  )
  form = forms.CustomUserChangeForm
  add_form = forms.CustomUserCreationForm
  list_display = ('id', 'first_name', 'last_name', 'email', 'image',
                  'status', 'language_code', 'timezone_code', 'is_staff',)
  list_display_links = list_display
  search_fields = ('first_name', 'last_name', 'email',)
  ordering = ('id', 'email',)
