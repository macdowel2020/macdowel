# Generated by Django 3.2.4 on 2021-08-23 11:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0007_auto_20210816_0052'),
    ]

    operations = [
        migrations.RenameField(
            model_name='asset',
            old_name='amount_sold',
            new_name='asset_model',
        ),
        migrations.RenameField(
            model_name='asset',
            old_name='categories',
            new_name='asset_name',
        ),
        migrations.RenameField(
            model_name='asset',
            old_name='sold_to',
            new_name='cost',
        ),
        migrations.RenameField(
            model_name='asset',
            old_name='number',
            new_name='location',
        ),
        migrations.AddField(
            model_name='asset',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 8, 23, 14, 5, 1, 932489)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='asset',
            name='date_sold',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='serial_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]