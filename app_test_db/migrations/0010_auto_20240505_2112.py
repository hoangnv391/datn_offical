# Generated by Django 3.1.5 on 2024-05-05 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_test_db', '0009_library_images'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='library_images',
            options={'verbose_name_plural': 'library_images'},
        ),
        migrations.RemoveField(
            model_name='library_images',
            name='motorbike',
        ),
    ]
