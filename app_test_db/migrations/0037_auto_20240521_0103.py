# Generated by Django 3.1.5 on 2024-05-20 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_test_db', '0036_auto_20240520_2318'),
    ]

    operations = [
        migrations.RenameField(
            model_name='motorbikes',
            old_name='slug',
            new_name='model_slug',
        ),
    ]