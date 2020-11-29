# Generated by Django 2.1 on 2019-01-01 15:40

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0009_auto_20181225_0734'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalCustomer',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, editable=False)),
                ('modified', models.DateTimeField(blank=True, editable=False)),
                ('uid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('velocify_milestone_id', models.FloatField(blank=True, null=True)),
                ('source_lead_id', models.CharField(blank=True, max_length=32)),
                ('send_realtor_status_email', models.BooleanField(null=True)),
                ('seller', models.BooleanField(null=True)),
                ('realtor_unresponsive', models.BooleanField(null=True)),
                ('realtor_feedback', models.TextField(blank=True)),
                ('real_estate_agent_confirmed', models.BooleanField(null=True)),
                ('real_estate_agent_assigned', models.BooleanField(null=True)),
                ('pre_approval_granted', models.BooleanField(null=True)),
                ('pre_approval_amount', models.FloatField(blank=True, null=True)),
                ('owner_id', models.CharField(blank=True, max_length=36)),
                ('lo_has_been_briefed', models.BooleanField(null=True)),
                ('lead_status', models.CharField(blank=True, max_length=32)),
                ('lead_number', models.CharField(blank=True, max_length=36)),
                ('last_modified_date', models.DateTimeField(blank=True, null=True)),
                ('last_activity_date', models.DateField(null=True)),
                ('last_activity', models.DateField(null=True)),
                ('last_action', models.CharField(blank=True, max_length=256)),
                ('hc_realtor_cs', models.CharField(blank=True, max_length=256)),
                ('hc_realtor_comments', models.CharField(blank=True, max_length=2048)),
                ('purchase_price', models.DecimalField(decimal_places=0, default=Decimal('0'), max_digits=12)),
                ('task_dropdown', models.CharField(blank=True, choices=[('', ''), ('Agent Milestone Followup', 'Agent Milestone Followup'), ('Lead Follow up', 'Lead Follow up'), ('Lender Follow up', 'Lender Follow up')], max_length=64)),
                ('milestones', models.CharField(blank=True, choices=[('', ''), ('Customer Still Searching for home', 'Customer Still Searching for home'), ('Customer Offer Submitted', 'Customer Offer Submitted'), ('Customer Ratified Contract', 'Customer Ratified Contract'), ('Customer Closing Confirmed', 'Customer Closing Confirmed'), ('Archived', 'Archived'), ('Searching Reset', 'Searching Reset'), ('Search for Home on Hold', 'Search for Home on Hold'), ('Customer No Longer Looking', 'Customer No Longer Looking'), ('Customer No Longer Responding', 'Customer No Longer Responding'), ('Using a Different Realtor', 'Using a Different Realtor'), ('Unqualified', 'Unqualified')], max_length=128)),
                ('milestone_status_reason', models.CharField(blank=True, choices=[('', ''), ('Considering Another Lender', 'Considering Another Lender'), ('Considering Another Realtor', 'Considering Another Realtor'), ('Realtor Not Responding', 'Realtor Not Responding'), ('Loan Officer Not Responding', 'Loan Officer Not Responding'), ('Found Another Realtor', 'Found Another Realtor'), ('Found Another Lender', 'Found Another Lender'), ('Customer Plans Fell Through', 'Customer Plans Fell Through'), ('Customer is No Longer Interested in Buying/Selling', 'Customer is No Longer Interested in Buying/Selling'), ('Appointment Set', 'Appointment Set'), ('Viewing Homes', 'Viewing Homes')], max_length=64)),
                ('hc_realtor_responsiveness', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True)),
                ('hc_realtor_rating', models.IntegerField(blank=True, null=True)),
                ('hc_realtor_knowledge', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True)),
                ('hc_lo_responsiveness', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True)),
                ('hc_lo_rating', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True)),
                ('hc_lo_knowledge', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True)),
                ('hc_lo_cs', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True)),
                ('customer_realtor_rating', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True)),
                ('customer_lo_rating', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True)),
                ('customer_hc_rep_rating', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True)),
                ('buyer_seller', models.CharField(blank=True, choices=[('', ''), ('Buyer', 'Buyer'), ('Seller', 'Seller'), ('Both', 'Both')], max_length=16)),
                ('account_type', models.CharField(blank=True, choices=[('', ''), ('Analyst', 'Analyst'), ('Competitor', 'Competitor'), ('Customer', 'Customer'), ('Integrator', 'Integrator'), ('Investor', 'Investor'), ('Partner', 'Partner'), ('Press', 'Press'), ('Prospect', 'Prospect'), ('Reseller', 'Reseller'), ('Other', 'Other')], max_length=16)),
                ('realtor_lo_rating', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True)),
                ('realtor_hc_rating', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True)),
                ('lo_realtor_rating', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True)),
                ('lo_hc_rep_rating', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True)),
                ('hc', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True)),
                ('customer_realtor_used_as_agent', models.BooleanField(null=True)),
                ('customer_lo_used', models.BooleanField(null=True)),
                ('account_at_risk', models.BooleanField(null=True)),
                ('hc_lo_comments', models.CharField(blank=True, max_length=2048)),
                ('hc_general_comments', models.TextField(blank=True)),
                ('gift_card_sent_date', models.DateField(blank=True, null=True)),
                ('estimated_closing_date', models.DateField(blank=True, null=True)),
                ('do_not_sms', models.BooleanField(null=True)),
                ('date_closed', models.DateField(blank=True, null=True)),
                ('customer_still_searching', models.BooleanField(null=True)),
                ('customer_realtor_comments', models.TextField(blank=True)),
                ('customer_rating_comments', models.CharField(blank=True, max_length=2048)),
                ('customer_nps', models.DecimalField(decimal_places=0, default=Decimal('0'), max_digits=12)),
                ('customer_lo_comments', models.TextField(blank=True)),
                ('customer_hc_rep_comments', models.TextField(blank=True)),
                ('customer_general_comments', models.CharField(blank=True, max_length=2048)),
                ('customer_feedback', models.TextField(blank=True)),
                ('customer_closed', models.BooleanField(null=True)),
                ('current_status', models.CharField(blank=True, max_length=128)),
                ('created_date', models.DateTimeField(blank=True, null=True)),
                ('company', models.CharField(blank=True, max_length=128)),
                ('comments_for_banks', models.TextField(blank=True)),
                ('closing_documents_received', models.BooleanField(null=True)),
                ('cash_back_amount', models.CharField(blank=True, max_length=32)),
                ('buyer', models.BooleanField(null=True)),
                ('bank_name_account', models.CharField(blank=True, max_length=128)),
                ('account_lost', models.BooleanField(null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical customer',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
