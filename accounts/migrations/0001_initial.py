# Generated by Django 2.0.1 on 2018-08-15 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Deployment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('d_name', models.CharField(default='DEFAULT VALUE', max_length=50)),
                ('deployer', models.ForeignKey(default=0, limit_choices_to={'groups__name': 'Deployers'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('view_project', 'can see available projects'),),
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=100)),
                ('file', models.FileField(default='DEFAULT VALUE', upload_to='accounts/static/accounts/')),
                ('deployment', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='accounts.Deployment')),
            ],
            options={
                'permissions': (('view_project', 'can see available projects'), ('create_project', 'can create new projects')),
            },
        ),
    ]