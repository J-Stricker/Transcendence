# Generated by Django 4.2.9 on 2024-01-31 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='player1_channel',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='player2_channel',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
