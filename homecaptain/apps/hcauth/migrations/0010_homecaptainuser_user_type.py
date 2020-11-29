# Generated by Django 2.1 on 2019-01-22 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hcauth', '0009_auto_20190112_0504'),
    ]

    operations = [
        migrations.AddField(
            model_name='homecaptainuser',
            name='user_type',
            field=models.CharField(blank=True, choices=[('buyer', 'Buyer'), ('seller', 'Seller'), ('realtor', 'Realtor'), ('loan-officer', 'Loan Officer')], max_length=16),
        ),
    ]