# Generated by Django 2.1 on 2019-01-04 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hcauth', '0007_auto_20190103_1652'),
        ('lender', '0007_auto_20190102_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanofficer',
            name='recommended_users',
            field=models.ManyToManyField(blank=True, related_name='recommended_loanofficer', to='hcauth.HomeCaptainRecommend'),
        ),
    ]
