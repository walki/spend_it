# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-03 20:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spend', '0005_auto_20171203_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='date',
            field=models.TextField(default=''),
        ),
    ]