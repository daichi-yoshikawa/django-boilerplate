from django.core.management import call_command
from django.core.management.base import BaseCommand


class TestDataCommand(BaseCommand):
  def handle(self, *args, **options):
    if options['reset_db']:
      call_command('reset_db', '--noinput')
      call_command('migrate')
    self.insert_data()

  def add_arguments(self, parser):
    parser.add_argument(
        '--reset_db', action='store_true',
        help='delete all db tables and re-create them.')

  def reset_db(self):
    call_command('reset_db', '--noinput')
    call_command('migrate')

  def insert_data(self):
    raise NotImplementedError('TestDataCommand.insert_data must be overwritten.')
