# Generated by Django 3.2.4 on 2021-08-23 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0008_auto_20210823_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenditure',
            name='expenditure_category',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='income',
            name='income_category',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
