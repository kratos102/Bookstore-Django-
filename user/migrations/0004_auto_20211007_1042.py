# Generated by Django 3.2.6 on 2021-10-07 03:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20211006_1104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customeruser',
            name='address',
        ),
        migrations.RemoveField(
            model_name='customeruser',
            name='firstname',
        ),
        migrations.RemoveField(
            model_name='customeruser',
            name='lastname',
        ),
        migrations.RemoveField(
            model_name='customeruser',
            name='phone_number',
        ),
    ]
