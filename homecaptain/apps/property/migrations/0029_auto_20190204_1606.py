# Generated by Django 2.1 on 2019-02-05 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0028_auto_20190204_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalproperty',
            name='permit_address_on_internet',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='historicalproperty',
            name='vow_address_display',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='property',
            name='permit_address_on_internet',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='property',
            name='vow_address_display',
            field=models.BooleanField(default=True),
        ),
    ]