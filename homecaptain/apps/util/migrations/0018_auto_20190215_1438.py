# Generated by Django 2.1 on 2019-02-15 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('util', '0017_hcoutgoingemail_anymail_message_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hcoutgoingemail',
            name='template_name',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
