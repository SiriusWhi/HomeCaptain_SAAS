# Generated by Django 2.1 on 2018-12-26 13:46

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requirement', '0003_auto_20181225_0734'),
    ]

    operations = [
        migrations.AddField(
            model_name='requirement',
            name='bathrooms',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='requirement',
            name='bedrooms',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='requirement',
            name='square_feet',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='requirement',
            name='target_price_maximum',
            field=models.DecimalField(decimal_places=0, default=Decimal('0'), max_digits=12),
        ),
        migrations.AddField(
            model_name='requirement',
            name='target_price_minimum',
            field=models.DecimalField(decimal_places=0, default=Decimal('0'), max_digits=12),
        ),
    ]
