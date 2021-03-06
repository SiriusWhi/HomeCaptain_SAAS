# Generated by Django 2.1 on 2019-01-01 18:05

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('concierge', '0003_concierge_name'),
        ('realtor', '0011_auto_20190101_0243'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lender', '0007_auto_20190101_0243'),
        ('customer', '0010_historicalcustomer'),
        ('requirement', '0004_auto_20181226_1346'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalRequirement',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, editable=False)),
                ('modified', models.DateTimeField(blank=True, editable=False)),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('desired_city_1', models.CharField(blank=True, max_length=128)),
                ('desired_state_1', models.CharField(blank=True, max_length=64)),
                ('desired_city_2', models.CharField(blank=True, max_length=128)),
                ('desired_state_2', models.CharField(blank=True, max_length=64)),
                ('desired_city_3', models.CharField(blank=True, max_length=128)),
                ('desired_state_3', models.CharField(blank=True, max_length=64)),
                ('desired_property_description', models.TextField(blank=True)),
                ('target_price_minimum', models.DecimalField(decimal_places=0, default=Decimal('0'), max_digits=12)),
                ('target_price_maximum', models.DecimalField(decimal_places=0, default=Decimal('0'), max_digits=12)),
                ('square_feet', models.IntegerField(default=0)),
                ('bedrooms', models.IntegerField(default=0)),
                ('bathrooms', models.IntegerField(default=0)),
                ('realtor_client_contact_date', models.DateField(blank=True, null=True)),
                ('realtor_lo_comments', models.TextField(blank=True)),
                ('realtor_rating_commnet', models.TextField(blank=True)),
                ('realtor_hc_comments', models.TextField(blank=True)),
                ('lo_realtor_comments', models.TextField(blank=True)),
                ('lo_rating_comment', models.TextField(blank=True)),
                ('lo_hc_comments', models.TextField(blank=True)),
                ('customer_rating_comments', models.TextField(blank=True)),
                ('realtor_general_comments', models.TextField(blank=True)),
                ('customer_general_comments', models.TextField(blank=True)),
                ('lo_general_comments', models.TextField(blank=True)),
                ('feedback', models.TextField(blank=True)),
                ('lo_feedback', models.TextField(blank=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('concierge', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='concierge.Concierge')),
                ('customer', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='customer.Customer')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('loan_officer', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='lender.LoanOfficer')),
                ('realtor', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='realtor.Realtor')),
            ],
            options={
                'verbose_name': 'historical requirement',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
