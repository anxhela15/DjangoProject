# Generated by Django 2.0.1 on 2018-09-07 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0079_auto_20180907_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='payed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='payment_calculated',
            field=models.BooleanField(default=False),
        ),
    ]
