# Generated by Django 2.0.1 on 2018-08-24 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0037_profile_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='require_suggestion',
            field=models.BooleanField(default=False),
        ),
    ]
