# Generated by Django 2.1.2 on 2018-10-29 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0014_auto_20181018_0803'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boards',
            name='has_price_info',
        ),
        migrations.RemoveField(
            model_name='boards',
            name='has_receipt_info',
        ),
        migrations.AddField(
            model_name='boards',
            name='not_board_amount',
            field=models.IntegerField(default=0),
        ),
    ]