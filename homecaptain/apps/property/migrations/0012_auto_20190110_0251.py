# Generated by Django 2.1 on 2019-01-10 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0011_property_favorite_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prequalificationrequest',
            name='loan_officer',
        ),
        migrations.RemoveField(
            model_name='prequalificationrequest',
            name='property',
        ),
        migrations.RemoveField(
            model_name='valuationrequest',
            name='property',
        ),
        migrations.RemoveField(
            model_name='valuationrequest',
            name='realtor',
        ),
        migrations.DeleteModel(
            name='PreQualificationRequest',
        ),
        migrations.DeleteModel(
            name='ValuationRequest',
        ),
    ]