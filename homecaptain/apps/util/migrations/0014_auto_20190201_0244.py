# Generated by Django 2.1 on 2019-02-01 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('util', '0013_auto_20190129_0613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='unit_number',
            field=models.CharField(blank=True, max_length=32),
        ),
    ]