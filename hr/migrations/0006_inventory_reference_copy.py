# Generated by Django 3.2.3 on 2021-07-14 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0005_inventory'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='reference_copy',
            field=models.ImageField(blank=True, default='logo.jpg', null=True, upload_to='projects/photocopies'),
        ),
    ]