# Generated by Django 4.0.2 on 2022-02-25 02:50

import core.models.base_models
import core.models.tenant
import core.models.user
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created_by', models.CharField(default='system', max_length=20)),
                ('updated_by', models.CharField(default='system', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('disable_promotion', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=200, unique=True)),
                ('first_name', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to=core.models.user.get_user_image_path, verbose_name='user image')),
                ('language_code', models.CharField(default='en', max_length=20)),
                ('last_name', models.CharField(max_length=200)),
                ('status', models.IntegerField(default=0)),
                ('timezone_code', models.CharField(default='America/Los_Angeles', max_length=200)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'users',
                'ordering': ['-updated_at'],
                'abstract': False,
            },
            managers=[
                ('objects', core.models.base_models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='EmailVerificationCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(default='system', max_length=20)),
                ('updated_by', models.CharField(default='system', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('email', models.EmailField(max_length=200)),
                ('verification_code', models.CharField(max_length=200, unique=True)),
                ('valid_until', models.DateTimeField()),
            ],
            options={
                'db_table': 'email_verification_codes',
                'ordering': ['-updated_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FailedLoginAttempt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(default='system', max_length=20)),
                ('updated_by', models.CharField(default='system', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('ip_address', models.CharField(blank=True, default='', max_length=200)),
                ('email', models.EmailField(max_length=200)),
                ('attempted_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'failed_login_attempts',
                'ordering': ['-updated_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PasswordResetCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(default='system', max_length=20)),
                ('updated_by', models.CharField(default='system', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('email', models.EmailField(max_length=200)),
                ('reset_code', models.CharField(max_length=200, unique=True)),
                ('valid_until', models.DateTimeField()),
            ],
            options={
                'db_table': 'password_reset_codes',
                'ordering': ['-updated_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(default='system', max_length=20)),
                ('updated_by', models.CharField(default='system', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('name', models.CharField(max_length=200)),
                ('domain', models.CharField(max_length=200, unique=True)),
                ('image', models.ImageField(blank=True, upload_to=core.models.tenant.get_tenant_image_path, verbose_name='tenant logo image')),
                ('description', models.TextField(blank=True, default='', max_length=1000)),
            ],
            options={
                'db_table': 'tenants',
                'ordering': ['-updated_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TenantUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(default='system', max_length=20)),
                ('updated_by', models.CharField(default='system', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('role_type', models.IntegerField(blank=True, default=0)),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.tenant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tenant_users',
                'ordering': ['-updated_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TenantInvitationCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(default='system', max_length=20)),
                ('updated_by', models.CharField(default='system', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('email', models.EmailField(max_length=200)),
                ('invitation_code', models.CharField(max_length=200, unique=True)),
                ('invited_at', models.DateTimeField(auto_now_add=True)),
                ('valid_until', models.DateTimeField()),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.tenant')),
                ('tenant_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.tenantuser')),
            ],
            options={
                'db_table': 'tenant_invitation_codes',
                'ordering': ['-updated_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmailChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(default='system', max_length=20)),
                ('updated_by', models.CharField(default='system', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('new_email', models.EmailField(max_length=200)),
                ('verification_code', models.CharField(max_length=200, unique=True)),
                ('valid_until', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'email_changes',
                'ordering': ['-updated_at'],
                'abstract': False,
            },
        ),
        migrations.AddConstraint(
            model_name='tenantuser',
            constraint=models.UniqueConstraint(fields=('tenant_id', 'user_id'), name='unique_tenant_user'),
        ),
    ]