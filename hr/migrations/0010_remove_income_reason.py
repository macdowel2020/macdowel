# Generated by Django 3.2.3 on 2021-07-22 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0009_auto_20210722_1931'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='income',
            name='reason',
        ),
    ]