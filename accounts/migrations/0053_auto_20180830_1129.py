# Generated by Django 2.0.1 on 2018-08-30 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0052_project_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='version',
            field=models.FloatField(default=1.0),
        ),
    ]
