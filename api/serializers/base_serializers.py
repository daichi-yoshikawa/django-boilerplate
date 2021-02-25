from rest_framework import serializers
from rest_framework.fields import empty

from api.common import constants
from core import models


class BaseModelSerializer(serializers.ModelSerializer):
  """
  How to create derived class
  1. Inherit BaseModelSerializer.
     Eg.)class XXXSerializer(BaseModelSerializer)
  2. Inherit Meta class as well.
     Eg.)class Meta(BaseModelSerializer.Model)
  3. If extends exclude, do as below.
     Eg.)exclude = ('xxx', 'yyy',) + BaseModelSerializer.Meta.exclude
  4. If extends read_only_fields, do as below.
     Eg.)read_only_fields = ('xxx',) + BaseModelSerializer.Meta.read_only_fields
  5. If foreign key is used, define the corresponding 2 members as below.
     (Assume that user = models.ForeignKey(...) is defined in User model)
     Eg.)user = UserSerializer(required=False, read_only=True)
         user_id = serializers.IntegerField(write_only=True)
     You may add required=True to user_id's argument.
  6. If need to extends create method, you can override it but
     do not forget to call self.createrstamp method and save method of model
     in case of that you don't use super().create in it.
     Eg1.)def create(self, validated_date):
            validated_data = self.createrstamp(validated_data) # <- Call this!
            user = models.User(**validated_data)
            user.set_password(user.password)
            user.save() # <- Call this!
            return user
     Eg2.)def create(self, validated_date):
            validated_data.pop('unused_field')
            return super().create(validated_data)
     Note: In super().create, self.createrstamp and save method are called.
  7. If need to extends update method, you can override it but
     do not forget to call self.updaterstamp method and save method of model
     in case of that you don't use super().update in it.
     Eg.1)def update(self, instance, validated_data):
            validated_data = self.updaterstamp(validated_data) # <- Call this!
            if 'password' in validated_data:
              instance.set_password(validated_data['password']:
            instance.save() # <- Call this!
            return instance
     Eg.2)def update(self, instance, validated_data):
            validated_data['code'] = generate_code(length=10)
            instance = super().update(instance, validated_data)
            return instance
     Note: In super().update, self.updaterstamp and save method are called.
  8. If need to implement validate method, define validate method.
     You can use self.tenant_user or self.user if these are given
     to the constructor. Here, tenant_user is given by tenant_user_api decorator.
     For more details, see api.resouces.decorators module.
     Eg.)serializer = serializer.XXXSerializer(
             data=request.data, tenant_user=tenant_user)
         # If you instantiate serializer like above, you can use tenant_user
           for validation.
         serializer = serializer.XXXSerializer(
             data=request.data, user=request.data)
         # If you instantiate serializer like above, you can use user
           for validation.
  """
  class Meta:
    """
    If the following parameters need to be extended in derived class,
    do as follows.

    class Meta(BaseModelSerializer.Meta):
      exclude = ('xxx', 'yyy',) + BaseModelSerializer.Meta.exclude
      read_only_fields = ('zzz',) + BaseModelSerializer.Meta.read_only_fields
    """
    exclude = ('created_at', 'updated_at', 'deleted_at',)
    read_only_fields = ('id',)
    extra_kwargs = {
      'created_by': { 'write_only': True },
      'updated_by': { 'write_only': True },
    }

  def __init__(
      self, instance=None, data=empty, tenant=None, tenant_user=None, user=None,
      extra_request=None, **kwargs):
    super().__init__(instance=instance, data=data, **kwargs)
    self.tenant = tenant
    self.tenant_user = tenant_user
    self.user = user

  def create(self, validated_data):
    validated_data = self.createrstamp(validated_data)
    return super().create(validated_data)

  def update(self, instance, validated_data):
    validated_data = self.updaterstamp(validated_data)
    return super().update(instance, validated_data)

  def _get_creater(self):
    creater = constants.BUILTIN_USER.SYSTEM.value
    if self.tenant_user is not None:
      creater = str(self.tenant_user.user.id)
    elif self.user is not None:
      creater = (constants.BUILTIN_USER.ANONYMOUS.value
                 if self.user.id is None else str(self.user.id))
    return creater

  def _get_updater(self):
    updater = constants.BUILTIN_USER.SYSTEM.value
    if self.tenant_user is not None:
      updater = str(self.tenant_user.user.id)
    elif self.user is not None:
      updater = (constants.BUILTIN_USER.ANONYMOUS.value
                 if self.user.id is None else str(self.user.id))
    return updater

  def createrstamp(self, validated_data):
    creater = self._get_creater()
    validated_data['created_by'] = creater
    validated_data['updated_by'] = creater
    return validated_data

  def updaterstamp(self, validated_data):
    updater = self._get_updater()
    validated_data['updated_by'] = updater
    return validated_data

  def fill_missing_fields_by_instance(self, data):
    if self.instance is None:
      return data

    writable_fields = tuple(field.field_name for field in self._writable_fields)

    for field in writable_fields:
      if field not in data:
        data[field] = self.instance._meta.get_field(
            field).value_from_object(self.instance)

    return data

  def set_blank_explicitly(self, data, fields):
    for field in fields:
      if field not in data:
        continue

      if data[field] is None:
        data.pop(field)
      elif isinstance(data[field], str) and data[field] == '':
        data.pop(field)
      elif isinstance(data[field], list) and len(data[field]) == 0:
        data.pop(field)
      elif isinstance(data[field], dict) and len(data[field]) == 0:
        data.pop(field)

    return data
