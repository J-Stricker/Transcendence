# Generated by Django 4.2.10 on 2024-02-11 12:28

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
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
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('pseudo', models.CharField(max_length=16)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('user_is_connected', models.BooleanField(default=False)),
                ('user_is_looking_game', models.BooleanField(default=False)),
                ('user_is_looking_tournament', models.BooleanField(default=False)),
                ('user_is_in_game', models.BooleanField(default=False)),
                ('channel_name', models.CharField(blank=True, max_length=255, null=True)),
                ('logged_with_42', models.BooleanField(default=False)),
                ('status_2fa', models.BooleanField(default=False)),
                ('qrcode', models.TextField(default=None, null=True)),
                ('friendlist', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
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
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player1_username', models.CharField(max_length=150)),
                ('player2_username', models.CharField(max_length=150)),
                ('active_game', models.BooleanField(default=True)),
                ('date', models.DateTimeField()),
                ('p1_score', models.PositiveIntegerField(default=0)),
                ('p2_score', models.PositiveIntegerField(default=0)),
                ('win_lose', models.PositiveIntegerField(default=0)),
                ('player1_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player1_matches', to=settings.AUTH_USER_MODEL)),
                ('player2_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player2_matches', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('final', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='final', to='api.match')),
                ('match_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_1', to='api.match')),
                ('match_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_2', to='api.match')),
            ],
        ),
    ]
