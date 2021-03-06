# Generated by Django 2.1 on 2019-01-12 13:04

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('hcauth', '0008_auto_20190108_2032'),
    ]

    operations = [
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('archiving_object_id', models.PositiveIntegerField()),
                ('archived_object_id', models.PositiveIntegerField()),
                ('comments', models.TextField(blank=True)),
                ('archived_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='archives_received', to='contenttypes.ContentType')),
                ('archiving_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='archives_done', to='contenttypes.ContentType')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='archive',
            unique_together={('archiving_content_type', 'archiving_object_id', 'archived_content_type', 'archived_object_id')},
        ),
    ]
