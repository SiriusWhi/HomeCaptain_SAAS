# Generated by Django 2.1 on 2018-12-28 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtor', '0009_auto_20181225_0734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='broker',
            name='company',
            field=models.CharField(blank=True, max_length=256, unique=True),
        ),
    ]