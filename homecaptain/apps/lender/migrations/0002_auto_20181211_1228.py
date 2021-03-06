# Generated by Django 2.0 on 2018-12-11 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lender', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanofficer',
            name='lead_source',
            field=models.CharField(blank=True, choices=[('', ''), ('Advertisement', 'Advertisement'), ('Employee Referral', 'Employee Referral'), ('External Referral', 'External Referral'), ('Partner', 'Partner'), ('Public Relations', 'Public Relations'), ('Seminar - Partner', 'Seminar - Partner'), ('Trade Show', 'Trade Show'), ('Web', 'Web'), ('Word of mouth', 'Word of mouth'), ('Other', 'Other'), ('Great Plains', 'Great Plains'), ('NASB', 'NASB')], max_length=128),
        ),
        migrations.AlterField(
            model_name='loanofficer',
            name='titlee',
            field=models.CharField(blank=True, choices=[('', ''), ('Loan Officer', 'Loan Officer'), ('Team Lead', 'Team Lead'), ('Sales Manager', 'Sales Manager'), ('Purchasing', 'Purchasing'), ('Velocify Administrator', 'Velocify Administrator'), ('Vice President', 'Vice President'), ('Sales Assistant', 'Sales Assistant'), ('Production Assistant', 'Production Assistant'), ('Sales Agent', 'Sales Agent'), ('Branch Manager', 'Branch Manager'), ('Director', 'Director'), ('Purchase Loan Specialist', 'Purchase Loan Specialist'), ('Assistant Sales Manager', 'Assistant Sales Manager')], max_length=128),
        ),
    ]
