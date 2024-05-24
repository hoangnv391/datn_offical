# Generated by Django 3.1.5 on 2024-05-24 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_test_db', '0042_auto_20240524_1527'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='motorbike_specs',
            name='height',
        ),
        migrations.RemoveField(
            model_name='motorbike_specs',
            name='length',
        ),
        migrations.RemoveField(
            model_name='motorbike_specs',
            name='width',
        ),
        migrations.AddField(
            model_name='motorbike_specs',
            name='length_width_height',
            field=models.TextField(blank=True, verbose_name='Dài x Rộng x Cao'),
        ),
        migrations.AlterField(
            model_name='motorbike_specs',
            name='mass_ifself',
            field=models.TextField(blank=True, verbose_name='Khối lượng bản thân'),
        ),
    ]
