# Generated by Django 2.0.1 on 2018-08-19 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20180818_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='file_name',
            field=models.CharField(default='DEFAULT', max_length=100),
        ),
    ]
