# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-16 16:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=32)),
                ('ip', models.CharField(max_length=32)),
                ('port', models.CharField(max_length=8)),
                ('status', models.CharField(max_length=10)),
            ],
        ),
    ]
