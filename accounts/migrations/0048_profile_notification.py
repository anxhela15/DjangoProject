# Generated by Django 2.0.1 on 2018-08-28 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0047_auto_20180827_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='notification',
            field=models.BooleanField(default=False),
        ),
    ]