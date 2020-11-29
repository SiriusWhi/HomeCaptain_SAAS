# Generated by Django 2.1 on 2019-01-04 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_auto_20190103_2006'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AddField(
            model_name='event',
            name='note',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(blank=True, choices=[('Property Showing', 'Property Showing'), ('Sign the Agent Document', 'Sign the Agent Document')], max_length=64),
        ),
    ]