# Generated by Django 2.1 on 2019-01-07 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lender', '0008_loanofficer_recommended_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loanofficer',
            name='recommended_users',
        ),
    ]
