# Generated by Django 2.0.1 on 2018-09-03 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0055_auto_20180830_1137'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='days',
            field=models.IntegerField(default=0),
        ),
    ]
