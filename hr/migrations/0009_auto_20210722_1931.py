# Generated by Django 3.2.3 on 2021-07-22 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0008_alter_project_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='income',
            name='category',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='income',
            name='qty',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='income',
            name='sub_total',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
