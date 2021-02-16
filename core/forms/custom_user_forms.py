from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from core import models


class CustomUserCreationForm(UserCreationForm):
  class Meta(UserCreationForm.Meta):
    model = models.User
    fields = ('first_name', 'last_name', 'email', 'status',
              'language_code', 'timezone_code',)
    field_classes = None


class CustomUserChangeForm(UserChangeForm):
  class Meta(UserChangeForm.Meta):
    model = models.User
    fields = ('first_name', 'last_name', 'email', 'image', 'status',
              'language_code', 'timezone_code',)
    field_classes = None
