from .constants import N_USERS
from .test_data_command import TestDataCommand
from core import models


class Command(TestDataCommand):
  def insert_data(self):
    for i in range(1, N_USERS+1, 1):
      req = dict(
          first_name=f'F{str(i).zfill(3)}',
          last_name=f'L{str(i).zfill(3)}',
          email=f'test{str(i).zfill(3)}@test.com',
          password = 'testtest')
      user = models.User(**req)
      user.set_password(req['password'])
      user.save()
