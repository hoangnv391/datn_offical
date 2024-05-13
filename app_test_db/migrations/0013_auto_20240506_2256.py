# Generated by Django 3.1.5 on 2024-05-06 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_test_db', '0012_auto_20240505_2218'),
    ]

    operations = [
        migrations.AddField(
            model_name='motorbike_skus',
            name='sku_image',
            field=models.ImageField(null=True, upload_to='sku_images'),
        ),
        migrations.AddField(
            model_name='motorbikes',
            name='default_image',
            field=models.ImageField(null=True, upload_to='default_images'),
        ),
    ]
