# Generated by Django 2.1 on 2018-12-29 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hcauth', '0005_homecaptainrecommend'),
        ('property', '0004_property_favorite_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='recommended_users',
            field=models.ManyToManyField(blank=True, related_name='recommended_property', to='hcauth.HomeCaptainRecommend'),
        ),
    ]
