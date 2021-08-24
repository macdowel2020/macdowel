# Generated by Django 3.2.4 on 2021-08-23 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0010_salary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salary',
            name='staff',
        ),
        migrations.AlterField(
            model_name='salary',
            name='payment_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hr.staff'),
        ),
    ]