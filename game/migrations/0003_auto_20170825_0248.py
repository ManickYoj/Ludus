# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 02:48
from __future__ import unicode_literals

from django.db import migrations, models
import school


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20170819_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='status',
            field=models.CharField(choices=[('ISS', 'Issued'), ('ACC', 'Accepted'), ('REJ', 'Rejected'), ('WON', 'Won'), ('LOS', 'Lost')], max_length=3),
        ),
        migrations.AlterField(
            model_name='school',
            name='period',
            field=models.CharField(choices=[('RE', 'Recruit'), ('AS', 'Assign'), ('FI', 'Fight')], default=school.PERIOD('RE'), max_length=2),
        ),
    ]
