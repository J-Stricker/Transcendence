# Generated by Django 4.2.9 on 2024-01-30 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_match_paddle1_pos_match_paddle2_pos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='game_room',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
