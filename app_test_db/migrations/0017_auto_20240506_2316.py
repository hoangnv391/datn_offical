# Generated by Django 3.1.5 on 2024-05-06 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_test_db', '0016_auto_20240506_2305'),
    ]

    operations = [
        migrations.RenameField(
            model_name='motorbikes',
            old_name='default_image',
            new_name='image',
        ),
    ]
