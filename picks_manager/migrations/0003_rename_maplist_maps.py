# Generated by Django 4.1.3 on 2024-02-25 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('picks_manager', '0002_brawlers_modes_alter_maplist_mode_name_winrate'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MapList',
            new_name='Maps',
        ),
    ]