# Generated by Django 4.1.3 on 2024-04-22 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picks_manager', '0003_player_last_checked'),
    ]

    operations = [
        migrations.AddField(
            model_name='map',
            name='image_url',
            field=models.CharField(default='no_image', max_length=100),
            preserve_default=False,
        ),
    ]