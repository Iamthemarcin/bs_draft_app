# Generated by Django 4.1.3 on 2024-04-10 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('picks_manager', '0007_brawler_brawler_class'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brawler_Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=25)),
                ('countered_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='picks_manager.brawler_class')),
            ],
            options={
                'verbose_name_plural': 'Brawler_classes',
            },
        ),
    ]
