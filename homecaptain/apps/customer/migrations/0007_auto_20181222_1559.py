# Generated by Django 2.0 on 2018-12-22 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_customer_hc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_lo_rating',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]