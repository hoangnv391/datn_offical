# Generated by Django 3.1.5 on 2024-05-20 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_test_db', '0037_auto_20240521_0103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='motorbikes',
            name='model_slug',
            field=models.SlugField(blank=True, default='', null=True),
        ),
    ]