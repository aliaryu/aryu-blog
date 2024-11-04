# Generated by Django 5.1.1 on 2024-11-03 15:12

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

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
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_deleted', models.BooleanField(blank=True, default=False, verbose_name='is deleted')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='deleted at')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email')),
                ('is_active', models.BooleanField(default=False, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(blank=True, default=False, verbose_name='is deleted')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='deleted at')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='create at')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='update at')),
                ('biography', models.TextField(blank=True, null=True, verbose_name='biography')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1, null=True, verbose_name='gender')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='birth date')),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, verbose_name='phone number')),
                ('image', models.ImageField(blank=True, null=True, upload_to='profile_image/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('jpg', 'png'))], verbose_name='image')),
                ('profile_view', models.PositiveIntegerField(default=1, verbose_name='profile view')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'profile',
                'verbose_name_plural': 'profiles',
            },
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.ForeignKey(help_text='the one who follows', on_delete=django.db.models.deletion.DO_NOTHING, related_name='followings', to=settings.AUTH_USER_MODEL, verbose_name='follower')),
                ('following', models.ForeignKey(help_text='the one who is followed', on_delete=django.db.models.deletion.DO_NOTHING, related_name='followers', to=settings.AUTH_USER_MODEL, verbose_name='following')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('follower', 'following'), name='unique_follow'), models.CheckConstraint(condition=models.Q(('follower', models.F('following')), _negated=True), name='same_follower_following')],
            },
        ),
    ]