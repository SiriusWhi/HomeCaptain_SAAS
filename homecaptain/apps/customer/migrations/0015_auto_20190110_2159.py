# Generated by Django 2.1 on 2019-01-11 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0014_auto_20190110_0542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='milestones',
            field=models.CharField(blank=True, choices=[('Customer Still Searching for home', 'Still Searching for home'), ('Customer Offer Submitted', 'Offer Submitted'), ('Customer Ratified Contract', 'Ratified Contract'), ('Customer Closing Confirmed', 'Closing Confirmed'), ('Archived', 'Archived'), ('Searching Reset', 'Searching Reset'), ('Search for Home on Hold', 'Search on Hold'), ('Customer No Longer Looking', 'No Longer Looking'), ('Customer No Longer Responding', 'No Longer Responding'), ('Using a Different Realtor', 'Using a Different Realtor'), ('Unqualified', 'Unqualified'), ('Customer Home Listed', 'Home Listed'), ('Purchase Offer Submitted', 'Purchase Offer Submitted'), ('Home Sold', 'Home Sold')], max_length=128),
        ),
        migrations.AlterField(
            model_name='customerstatusupdate',
            name='previous_milestone',
            field=models.CharField(blank=True, choices=[('Customer Still Searching for home', 'Still Searching for home'), ('Customer Offer Submitted', 'Offer Submitted'), ('Customer Ratified Contract', 'Ratified Contract'), ('Customer Closing Confirmed', 'Closing Confirmed'), ('Archived', 'Archived'), ('Searching Reset', 'Searching Reset'), ('Search for Home on Hold', 'Search on Hold'), ('Customer No Longer Looking', 'No Longer Looking'), ('Customer No Longer Responding', 'No Longer Responding'), ('Using a Different Realtor', 'Using a Different Realtor'), ('Unqualified', 'Unqualified'), ('Customer Home Listed', 'Home Listed'), ('Purchase Offer Submitted', 'Purchase Offer Submitted'), ('Home Sold', 'Home Sold')], max_length=128),
        ),
    ]