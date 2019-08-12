# Generated by Django 2.2 on 2019-08-12 15:14

from django.db import migrations, models
import django.db.models.deletion
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Algorithm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('algorithm_name', models.CharField(max_length=20)),
                ('default_algorithm_params', django_mysql.models.JSONField(default=dict)),
                ('algorithm_params_range', django_mysql.models.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='DataSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='datasets/')),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('feature_importance', models.CharField(max_length=64)),
                ('profile_name', models.CharField(max_length=30)),
                ('profile_params', django_mysql.models.JSONField(default=dict)),
                ('factors', django_mysql.models.JSONField(default=dict)),
                ('algorithm', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='datalab.Algorithm')),
                ('teach', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='datalab.DataSet')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('experiment_name', models.CharField(max_length=30)),
                ('analyzer_name', models.CharField(max_length=30)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='datalab.Profile')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='datalab.DataSet')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
