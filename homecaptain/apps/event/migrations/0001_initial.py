# Generated by Django 2.0 on 2018-12-11 09:44

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EventConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(choices=[('event_1', 'Event 1')], max_length=64)),
                ('is_owner_required', models.BooleanField(default=False)),
                ('is_loan_officer_required', models.BooleanField(default=False)),
                ('is_realtor_required', models.BooleanField(default=False)),
                ('is_concierge_required', models.BooleanField(default=False)),
                ('is_service_provider_required', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EventSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('proposed_at', models.DateTimeField()),
                ('is_owner_confirmed', models.BooleanField(default=False)),
                ('is_loan_officer_confirmed', models.BooleanField(default=False)),
                ('is_realtor_confirmed', models.BooleanField(default=False)),
                ('is_concierge_confirmed', models.BooleanField(default=False)),
                ('is_service_provider_confirmed', models.BooleanField(default=False)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.Event')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='event',
            name='event_config',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='event.EventConfig'),
        ),
    ]
