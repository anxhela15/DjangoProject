# Generated by Django 2.0.1 on 2018-09-03 08:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0056_profile_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='dateofcreation',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
