# Generated by Django 2.0.1 on 2018-08-24 11:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0030_auto_20180823_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='dateofcreation',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
