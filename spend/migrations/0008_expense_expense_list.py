# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-01 21:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spend', '0007_expenselist'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='expense_list',
            field=models.TextField(default=''),
        ),
    ]
