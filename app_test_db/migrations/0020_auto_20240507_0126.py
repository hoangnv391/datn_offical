# Generated by Django 3.1.5 on 2024-05-06 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_test_db', '0019_auto_20240507_0102'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='cart_items',
            table='cart_items',
        ),
        migrations.AlterModelTable(
            name='carts',
            table='carts',
        ),
        migrations.AlterModelTable(
            name='library_images',
            table='library_images',
        ),
        migrations.AlterModelTable(
            name='motorbike_attributes',
            table='motorbike_attributes',
        ),
        migrations.AlterModelTable(
            name='motorbike_feature_images',
            table='motorbike_feature_images',
        ),
        migrations.AlterModelTable(
            name='motorbike_features',
            table='motorbike_features',
        ),
        migrations.AlterModelTable(
            name='motorbike_skus',
            table='motorbike_skus',
        ),
        migrations.AlterModelTable(
            name='motorbike_specs',
            table='motorbike_specs',
        ),
        migrations.AlterModelTable(
            name='motorbikes',
            table='motorbikes',
        ),
        migrations.AlterModelTable(
            name='order_details',
            table='order_details',
        ),
        migrations.AlterModelTable(
            name='order_items',
            table='order_items',
        ),
        migrations.AlterModelTable(
            name='payment_details',
            table='payment_details',
        ),
        migrations.AlterModelTable(
            name='users',
            table='users',
        ),
    ]
