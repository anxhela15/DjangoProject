# Generated by Django 2.0.1 on 2018-09-04 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0072_project_new_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='finishtime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='completed at'),
        ),
    ]
