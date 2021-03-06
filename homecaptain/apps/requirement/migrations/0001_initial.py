# Generated by Django 2.0 on 2018-12-11 09:44

from django.db import migrations, models
import django.db.models.deletion
import localflavor.us.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lender', '0001_initial'),
        ('concierge', '0001_initial'),
        ('customer', '0001_initial'),
        ('realtor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('desired_city_1', models.CharField(blank=True, max_length=128)),
                ('desired_state_1', localflavor.us.models.USStateField(blank=True, max_length=2)),
                ('desired_city_2', models.CharField(blank=True, max_length=128)),
                ('desired_state_2', localflavor.us.models.USStateField(blank=True, max_length=2)),
                ('desired_city_3', models.CharField(blank=True, max_length=128)),
                ('desired_state_3', localflavor.us.models.USStateField(blank=True, max_length=2)),
                ('desired_property_description', models.TextField(blank=True)),
                ('concierge', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='concierge.Concierge')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requirements', to='customer.Customer')),
                ('loan_officer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lender.LoanOfficer')),
                ('realtor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='realtor.Realtor')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
