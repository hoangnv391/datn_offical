# Generated by Django 3.1.5 on 2024-05-29 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_test_db', '0050_auto_20240529_2057'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='total',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
