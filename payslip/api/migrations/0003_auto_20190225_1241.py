# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-02-25 12:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20190223_0714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeedetails',
            name='name',
            field=models.CharField(max_length=250),
        ),
    ]
