# Generated by Django 3.2.4 on 2021-08-14 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0003_auto_20210728_0055'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenditure',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
