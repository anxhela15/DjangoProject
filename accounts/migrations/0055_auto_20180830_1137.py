# Generated by Django 2.0.1 on 2018-08-30 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0054_auto_20180830_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='version',
            field=models.FloatField(default=0),
        ),
    ]
