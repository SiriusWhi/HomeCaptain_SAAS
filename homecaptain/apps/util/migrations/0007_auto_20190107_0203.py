# Generated by Django 2.1 on 2019-01-07 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('util', '0006_recommend'),
    ]

    operations = [
        migrations.AddField(
            model_name='discourage',
            name='emails',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='discourage',
            name='usernames',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='recommend',
            name='emails',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='recommend',
            name='usernames',
            field=models.TextField(blank=True),
        ),
    ]
