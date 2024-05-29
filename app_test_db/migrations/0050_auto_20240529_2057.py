# Generated by Django 3.1.5 on 2024-05-29 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_test_db', '0049_auto_20240529_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='order_status',
            field=models.CharField(blank=True, choices=[('ordered', 'Đã đặt hàng'), ('processing', 'Đang xử lý'), ('success', 'Giao hàng thành công'), ('canceled', 'Đã hủy')], default='ordered', max_length=20, null=True, verbose_name='Tình trạng'),
        ),
    ]
