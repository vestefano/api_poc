"""
Initial migration for the accounts app.

This migration defines the initial set of models and their fields for the accounts app.
"""

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    """
    Migration class for creating the initial database schema for the accounts app.
    """

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(
                    default=False,
                    help_text='Designates that this user has all permissions without explicitly assigning them.',
                    verbose_name='superuser status')
                 ),
                ('username', models.CharField(
                    error_messages={'unique': 'A user with that username already exists.'},
                    help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                    max_length=150,
                    unique=True,
                    validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                    verbose_name='username')
                 ),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(
                    default=False,
                    help_text='Designates whether the user can log into this admin site.',
                    verbose_name='staff status')
                 ),
                ('is_active', models.BooleanField(
                    default=True,
                    help_text=(
                        'Designates whether this user should be treated as active. '
                        'Unselect this instead of deleting accounts.'
                    ),
                    verbose_name='active')
                 ),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(
                    blank=True,
                    help_text=(
                        'The groups this user belongs to. '
                        'A user will get all permissions granted to each of their groups.'
                    ),
                    related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')
                 ),
                ('user_permissions', models.ManyToManyField(
                    blank=True,
                    help_text='Specific permissions for this user.',
                    related_name='user_set', related_query_name='user',
                    to='auth.permission',
                    verbose_name='user permissions')
                 ),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, help_text='Phone field', max_length=15, null=True, unique=True)),
                ('address', models.CharField(blank=True, help_text='Address field', max_length=100, null=True)),
                ('city', models.CharField(blank=True, help_text='City field', max_length=100, null=True)),
                ('state', models.CharField(blank=True, help_text='State field', max_length=2, null=True)),
                ('zipcode', models.CharField(blank=True, help_text='Zipcode field', max_length=10, null=True)),
                ('available', models.BooleanField(default=True, help_text='User is available')),
                ('img', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.OneToOneField(
                    help_text='Related user',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='profile',
                    to=settings.AUTH_USER_MODEL)
                 ),
            ],
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_friend_of', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='is_friend_of',
                    to=settings.AUTH_USER_MODEL)
                 ),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='user',
                    to=settings.AUTH_USER_MODEL)
                 ),
            ],
            options={
                'unique_together': {('user', 'is_friend_of')},
            },
        ),
    ]
