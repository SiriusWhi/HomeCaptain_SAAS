# Generated by Django 2.1 on 2019-01-29 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('concierge', '0004_concierge_recommended_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='concierge',
            name='specialities',
        ),
    ]
