# Generated by Django 4.2.9 on 2024-01-30 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_user_friends'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='channel_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
