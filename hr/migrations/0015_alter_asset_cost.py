# Generated by Django 3.2.4 on 2021-08-24 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0014_alter_asset_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='cost',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]