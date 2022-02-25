from django.db import migrations
from django.contrib.postgres.operations import TrigramExtension


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_create_initial_tables'),
    ]

    operations = [
        TrigramExtension(),
        migrations.RunSQL(
            'CREATE EXTENSION IF NOT EXISTS pg_trgm;'
        ),
    ]

