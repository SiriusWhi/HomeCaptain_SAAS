# Generated by Django 2.1 on 2018-12-25 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtor', '0008_auto_20181223_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='realtor',
            name='agent_milestone_end_cycle',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='realtor',
            name='amount_paid',
            field=models.CharField(blank=True, max_length=16),
        ),
        migrations.AddField(
            model_name='realtor',
            name='realtor_contact_company_phone',
            field=models.CharField(blank=True, max_length=16),
        ),
        migrations.AddField(
            model_name='realtor',
            name='realtor_contact_mobile_phone',
            field=models.CharField(blank=True, max_length=16),
        ),
        migrations.AddField(
            model_name='realtor',
            name='realtor_interests',
            field=models.CharField(blank=True, choices=[('Becoming a Featured Agent?', 'Becoming a Featured Agent?'), ('Join our subscription list?', 'Join our subscription list?')], max_length=32),
        ),
        migrations.AddField(
            model_name='realtor',
            name='realtor_nps',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='realtor',
            name='realtor_status_start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='realtor',
            name='send_realtor_status_e_mail',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='realtor',
            name='simplesms_donotsms',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='realtor',
            name='velocify_realtor_phone',
            field=models.CharField(blank=True, max_length=16),
        ),
    ]
