# Generated by Django 2.1 on 2019-02-05 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtor', '0018_merge_20190201_0251'),
    ]

    operations = [
        migrations.AddField(
            model_name='broker',
            name='is_mls_auto_created',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='realtor',
            name='is_mls_auto_created',
            field=models.BooleanField(default=False),
        ),
    ]