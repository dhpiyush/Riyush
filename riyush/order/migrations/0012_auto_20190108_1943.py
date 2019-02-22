# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-01-08 14:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_order_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL),
        ),
    ]
