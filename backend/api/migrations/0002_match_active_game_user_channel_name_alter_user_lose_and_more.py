# Generated by Django 4.2.9 on 2024-02-02 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='active_game',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='channel_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='lose',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='win',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
