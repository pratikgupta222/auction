# Generated by Django 2.1.2 on 2018-10-15 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biddings', '0003_auctionitem_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionitem',
            name='final_amount',
            field=models.FloatField(blank=True, null=True, verbose_name='Final Amount'),
        ),
    ]
