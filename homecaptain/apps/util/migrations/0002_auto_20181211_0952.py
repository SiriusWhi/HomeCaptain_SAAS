# Generated by Django 2.0 on 2018-12-11 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('util', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='address',
            name='postalcode',
            field=models.CharField(blank=True, max_length=16),
        ),
        migrations.AlterField(
            model_name='address',
            name='state',
            field=models.CharField(blank=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='address',
            name='street',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]