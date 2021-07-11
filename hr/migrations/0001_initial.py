# Generated by Django 3.2.1 on 2021-05-06 00:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('contact', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('nin', models.CharField(blank=True, max_length=255, null=True)),
                ('gender', models.CharField(max_length=255)),
                ('role', models.CharField(max_length=255)),
                ('dob', models.DateField(blank=True, null=True)),
                ('staff_status', models.CharField(default='Inactive', max_length=255)),
                ('image', models.ImageField(default='logo.jpg', upload_to='profile/')),
                ('signature', models.ImageField(default='default.png', upload_to='profile/')),
                ('joined_on', models.DateTimeField(auto_now=True)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hr.department')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hr.project')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AuditTrail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.TextField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hr.project')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
