# Generated by Django 3.1.2 on 2020-10-10 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0007_auto_20201010_1722'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
    ]
