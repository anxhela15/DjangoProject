# Generated by Django 2.0.1 on 2018-09-11 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0095_profile_total_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='budget',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='progress',
            field=models.IntegerField(default=0),
        ),
    ]