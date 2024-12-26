# Generated by Django 5.1.4 on 2024-12-12 21:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digital', '0004_alter_specvalue_options_alter_category_parent_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название серии')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'серии',
                'verbose_name_plural': 'серий',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='model_series', to='digital.series', verbose_name='Серия'),
        ),
    ]
