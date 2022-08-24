# Generated by Django 4.1 on 2022-08-24 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Url',
            fields=[
                ('long_url', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('short_url', models.CharField(max_length=500)),
                ('clicks', models.IntegerField()),
                ('time_created', models.CharField(max_length=100)),
            ],
        ),
    ]