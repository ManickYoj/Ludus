# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gladiator',
            name='value',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='school',
            name='day_phase',
            field=models.CharField(default=b'REC', max_length=3, choices=[(b'REC', b'Recruit'), (b'PRE', b'Prepare'), (b'FIG', b'Fight'), (b'END', b'End of Day')]),
        ),
        migrations.AddField(
            model_name='school',
            name='denarii',
            field=models.PositiveIntegerField(default=2000),
        ),
        migrations.AlterField(
            model_name='gladiator',
            name='agility',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='gladiator',
            name='endurance',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='gladiator',
            name='strength',
            field=models.IntegerField(default=0),
        ),
    ]
