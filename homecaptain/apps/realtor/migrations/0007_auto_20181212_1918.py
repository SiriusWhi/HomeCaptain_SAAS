# Generated by Django 2.0 on 2018-12-12 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtor', '0006_auto_20181212_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='broker',
            name='phone',
            field=models.CharField(blank=True, max_length=16),
        ),
    ]
