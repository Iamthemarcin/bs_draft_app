# Generated by Django 4.1.3 on 2024-05-17 14:32

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BrawlerClass',
            fields=[
                ('class_name', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('countered_by', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Brawler classes',
            },
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
                ('mode_color', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('player_tag', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('last_checked', models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('map_name', models.CharField(max_length=30)),
                ('games_played', models.IntegerField()),
                ('image_url', models.CharField(max_length=100)),
                ('mode_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='picks_manager.mode')),
            ],
        ),
        migrations.CreateModel(
            name='Brawler',
            fields=[
                ('brawler_name', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('rarity', models.CharField(choices=[('LEGENDARY', 'Legendary'), ('MYTHICAL', 'Mythical'), ('EPIC', 'Epic'), ('SUPER RARE', 'Super rare'), ('RARE', 'Rare')], default='RARE', max_length=11)),
                ('image_url', models.CharField(max_length=200)),
                ('brawler_class', models.ForeignKey(max_length=25, on_delete=django.db.models.deletion.DO_NOTHING, to='picks_manager.brawlerclass')),
            ],
        ),
        migrations.CreateModel(
            name='WinRate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('use_rate', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('games_played', models.IntegerField()),
                ('games_won', models.IntegerField()),
                ('brawler_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='picks_manager.brawler')),
                ('map_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='picks_manager.map')),
            ],
            options={
                'unique_together': {('brawler_name', 'map_name')},
            },
        ),
    ]
