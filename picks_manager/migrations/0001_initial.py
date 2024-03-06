# Generated by Django 4.1.3 on 2024-03-05 21:15

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brawler',
            fields=[
                ('brawler_name', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('rarity', models.CharField(choices=[('LEGENDARY', 'Legendary'), ('MYTHICAL', 'Mythical'), ('EPIC', 'Epic'), ('SUPER RARE', 'Super rare'), ('RARE', 'Rare')], default='RARE', max_length=11)),
                ('image_url', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='LastPlayerChecked',
            fields=[
                ('last_player_checked', models.IntegerField(default=0, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name_plural': 'LastPlayerChecked',
            },
        ),
        migrations.CreateModel(
            name='Mode',
            fields=[
                ('mode_name', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('mode_icon', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('player_tag', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('map_name', models.CharField(max_length=30)),
                ('games_played', models.IntegerField()),
                ('mode_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='picks_manager.mode')),
            ],
        ),
    ]
