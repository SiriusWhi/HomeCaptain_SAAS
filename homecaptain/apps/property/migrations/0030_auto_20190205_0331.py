# Generated by Django 2.1 on 2019-02-05 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0029_auto_20190204_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalproperty',
            name='is_mls_auto_created',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='property',
            name='is_mls_auto_created',
            field=models.BooleanField(default=False),
        ),
    ]
