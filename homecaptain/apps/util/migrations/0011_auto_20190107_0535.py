# Generated by Django 2.1 on 2019-01-07 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('util', '0010_auto_20190107_0404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discourage',
            name='is_public',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='recommend',
            name='is_public',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
