# Generated by Django 2.1 on 2019-01-09 04:32

from django.conf import settings
import django.contrib.postgres.fields.jsonb
import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('event', '0007_auto_20190108_0135'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='additionaleventattendee',
            name='attendee',
        ),
        migrations.RemoveField(
            model_name='event',
            name='is_concierge_confirmed',
        ),
        migrations.RemoveField(
            model_name='event',
            name='is_concierge_required',
        ),
        migrations.RemoveField(
            model_name='event',
            name='is_loan_officer_confirmed',
        ),
        migrations.RemoveField(
            model_name='event',
            name='is_loan_officer_required',
        ),
        migrations.RemoveField(
            model_name='event',
            name='is_owner_confirmed',
        ),
        migrations.RemoveField(
            model_name='event',
            name='is_owner_required',
        ),
        migrations.RemoveField(
            model_name='event',
            name='is_realtor_confirmed',
        ),
        migrations.RemoveField(
            model_name='event',
            name='is_realtor_required',
        ),
        migrations.AddField(
            model_name='event',
            name='buyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='buyer_showings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='emails',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default='', encoder=django.core.serializers.json.DjangoJSONEncoder),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='is_buyer_concierge_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='is_buyer_concierge_required',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='is_buyer_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='is_buyer_loan_officer_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='is_buyer_loan_officer_required',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='is_buyer_realtor_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='is_buyer_realtor_required',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='is_buyer_required',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='is_seller_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='is_seller_realtor_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='is_seller_realtor_required',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='is_seller_required',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='requesting_user_type',
            field=models.CharField(choices=[('buyer', 'buyer'), ('realtor', 'realtor')], default='realtor', max_length=16),
        ),
        migrations.AlterField(
            model_name='event',
            name='additional_attendees',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='event',
            name='requested_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requested_events', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='AdditionalEventAttendee',
        ),
    ]