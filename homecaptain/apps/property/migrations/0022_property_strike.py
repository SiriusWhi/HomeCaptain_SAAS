# Generated by Django 2.1 on 2019-02-01 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0021_property_loan_officer'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='strike',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3)], default=0),
        ),
    ]
