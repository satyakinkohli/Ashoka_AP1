# Generated by Django 3.1.2 on 2020-10-16 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0007_auto_20201016_0815'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='name',
            field=models.CharField(default='', max_length=50),
        ),
    ]