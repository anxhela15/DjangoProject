# Generated by Django 2.0.1 on 2018-09-03 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0058_monthlyweatherbycity'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MonthlyWeatherByCity',
        ),
    ]
