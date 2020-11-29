# Generated by Django 2.1 on 2019-01-08 09:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('event', '0006_auto_20190107_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='requested_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='event',
            name='additional_attendees',
            field=models.ManyToManyField(blank=True, to='event.AdditionalEventAttendee'),
        ),
    ]