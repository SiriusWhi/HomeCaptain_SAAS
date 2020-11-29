# Generated by Django 2.0 on 2018-12-22 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_auto_20181212_0615'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='customer_lo_used',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='customer_realtor_used_as_agent',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='lo_hc_rep_rating',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='lo_realtor_rating',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='realtor_hc_rating',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='realtor_lo_rating',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='milestones',
            field=models.CharField(blank=True, choices=[('', ''), ('Customer Still Searching for home', 'Customer Still Searching for home'), ('Customer Offer Submitted', 'Customer Offer Submitted'), ('Customer Ratified Contract', 'Customer Ratified Contract'), ('Customer Closing Confirmed', 'Customer Closing Confirmed'), ('Archived', 'Archived'), ('Searching Reset', 'Searching Reset'), ('Search for Home on Hold', 'Search for Home on Hold'), ('Customer No Longer Looking', 'Customer No Longer Looking'), ('Customer No Longer Responding', 'Customer No Longer Responding'), ('Using a Different Realtor', 'Using a Different Realtor'), ('Unqualified', 'Unqualified')], max_length=128),
        ),
    ]