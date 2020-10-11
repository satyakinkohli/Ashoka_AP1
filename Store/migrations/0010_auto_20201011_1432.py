# Generated by Django 3.1.2 on 2020-10-11 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0009_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='no_of_reviews',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, default='Please buy this. The seller is broke and needs the money', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
