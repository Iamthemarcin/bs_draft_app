# Generated by Django 4.1.3 on 2024-04-10 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picks_manager', '0009_alter_brawler_class_countered_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brawler_class',
            name='countered_by',
            field=models.CharField(max_length=100),
        ),
    ]
