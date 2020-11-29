# Generated by Django 2.1 on 2019-01-07 09:31

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('util', '0004_auto_20181229_0422'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discourage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('discouraging_object_id', models.PositiveIntegerField()),
                ('discouraged_object_id', models.PositiveIntegerField()),
                ('rating', models.IntegerField(blank=True, null=True)),
                ('comments', models.TextField(blank=True)),
                ('discouraged_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discourages_received', to='contenttypes.ContentType')),
                ('discouraging_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discourages_given', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]