# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_auto_20170801_1259'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='day',
            name='school',
        ),
        migrations.RemoveField(
            model_name='recruit',
            name='day',
        ),
        migrations.RemoveField(
            model_name='gladiator',
            name='recruit_day',
        ),
        migrations.AddField(
            model_name='gladiator',
            name='recruited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='gladiator',
            name='recruited_on',
            field=models.PositiveIntegerField(default=None, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='gladiator',
            name='reserved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='school',
            name='day',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='school',
            name='period',
            field=models.CharField(default=b'REC', max_length=3, choices=[(b'REC', b'Dawn'), (b'PRE', b'Midday'), (b'FIG', b'Dusk')]),
        ),
        migrations.AlterField(
            model_name='gladiator',
            name='killed_on',
            field=models.PositiveIntegerField(default=None, null=True, blank=True),
        ),
        migrations.DeleteModel(
            name='Day',
        ),
        migrations.DeleteModel(
            name='Recruit',
        ),
    ]
