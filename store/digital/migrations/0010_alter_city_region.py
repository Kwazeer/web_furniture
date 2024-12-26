# Generated by Django 5.1.4 on 2024-12-19 16:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digital', '0009_alter_profile_address_alter_profile_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cities', to='digital.region', verbose_name='Регион'),
        ),
    ]