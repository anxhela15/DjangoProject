# Generated by Django 2.0.1 on 2018-08-19 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20180819_1105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='project_id',
        ),
        migrations.AlterField(
            model_name='project',
            name='id',
            field=models.PositiveIntegerField(default=0, primary_key=True, serialize=False),
        ),
    ]
