# Generated by Django 3.2.4 on 2021-08-24 18:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0018_staff_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='purchase_date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 8, 24, 21, 47, 49, 596246)),
            preserve_default=False,
        ),
    ]
