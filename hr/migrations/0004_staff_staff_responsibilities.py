# Generated by Django 3.2.3 on 2021-07-14 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0003_expenditure_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='staff_responsibilities',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]