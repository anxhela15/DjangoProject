# Generated by Django 2.0.1 on 2018-08-23 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_auto_20180823_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.TextField(default='DEFAULT VALUE'),
        ),
    ]
