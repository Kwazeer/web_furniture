# Generated by Django 5.1.4 on 2024-12-18 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digital', '0008_region_alter_favoriteproduct_options_customer_order_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, default='Не указано', max_length=100, null=True, verbose_name='Адрес (ул. дом. кв.)'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(blank=True, default='Не указано', max_length=50, null=True, verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, default='Не указано', max_length=30, null=True, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='region',
            field=models.CharField(blank=True, default='Не указано', max_length=50, null=True, verbose_name='Регион'),
        ),
    ]
