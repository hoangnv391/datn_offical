# Generated by Django 3.1.5 on 2024-05-13 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_test_db', '0028_auto_20240513_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email'),
        ),
    ]
