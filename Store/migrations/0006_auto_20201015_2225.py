# Generated by Django 3.1.1 on 2020-10-15 16:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0005_auto_20201015_1520'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='phone',
        ),
    ]