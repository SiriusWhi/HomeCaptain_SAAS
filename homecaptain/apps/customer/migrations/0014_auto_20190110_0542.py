# Generated by Django 2.1 on 2019-01-10 13:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0013_auto_20190110_0423'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerStatusUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('is_updated', models.BooleanField(default=False)),
                ('previous_milestone', models.CharField(blank=True, choices=[('Customer No Longer Looking', 'No Longer Looking'), ('Archived', 'Archived'), ('Using a Different Realtor', 'Using a Different Realtor'), ('Unqualified', 'Unqualified'), ('Purchase Offer Submitted', 'Purchase Offer Submitted'), ('Home Sold', 'Home Sold'), ('Search for Home on Hold', 'Search on Hold'), ('Customer No Longer Responding', 'No Longer Responding'), ('Customer Closing Confirmed', 'Closing Confirmed'), ('Customer Ratified Contract', 'Ratified Contract'), ('Customer Still Searching for home', 'Still Searching for home'), ('Customer Home Listed', 'Home Listed'), ('Customer Offer Submitted', 'Offer Submitted'), ('Searching Reset', 'Searching Reset')], max_length=128)),
                ('closed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customerstatusupdaterequests_closed', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='customer',
            name='needs_update',
        ),
        migrations.AlterField(
            model_name='customer',
            name='milestones',
            field=models.CharField(blank=True, choices=[('Customer No Longer Looking', 'No Longer Looking'), ('Archived', 'Archived'), ('Using a Different Realtor', 'Using a Different Realtor'), ('Unqualified', 'Unqualified'), ('Purchase Offer Submitted', 'Purchase Offer Submitted'), ('Home Sold', 'Home Sold'), ('Search for Home on Hold', 'Search on Hold'), ('Customer No Longer Responding', 'No Longer Responding'), ('Customer Closing Confirmed', 'Closing Confirmed'), ('Customer Ratified Contract', 'Ratified Contract'), ('Customer Still Searching for home', 'Still Searching for home'), ('Customer Home Listed', 'Home Listed'), ('Customer Offer Submitted', 'Offer Submitted'), ('Searching Reset', 'Searching Reset')], max_length=128),
        ),
        migrations.AddField(
            model_name='customerstatusupdate',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_update_history', to='customer.Customer'),
        ),
        migrations.AddField(
            model_name='customerstatusupdate',
            name='requested_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customerstatusupdaterequests_created', to=settings.AUTH_USER_MODEL),
        ),
    ]