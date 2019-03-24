# Generated by Django 2.0.1 on 2018-09-17 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0113_auto_20180917_1207'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reasons',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('task', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='accounts.Task')),
            ],
        ),
    ]
