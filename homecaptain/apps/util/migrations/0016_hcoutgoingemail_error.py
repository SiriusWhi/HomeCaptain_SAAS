# Generated by Django 2.1 on 2019-02-14 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('util', '0015_hcoutgoingemail'),
    ]

    operations = [
        migrations.AddField(
            model_name='hcoutgoingemail',
            name='error',
            field=models.TextField(blank=True),
        ),
    ]
