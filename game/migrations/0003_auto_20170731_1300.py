# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20170730_1806'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.PositiveIntegerField(default=0)),
                ('phase', models.CharField(default=b'REC', max_length=3, choices=[(b'REC', b'Recruit'), (b'PRE', b'Prepare'), (b'FIG', b'Fight'), (b'END', b'End of Day')])),
            ],
        ),
        migrations.RemoveField(
            model_name='school',
            name='day',
        ),
        migrations.RemoveField(
            model_name='school',
            name='day_phase',
        ),
        migrations.AddField(
            model_name='day',
            name='school',
            field=models.OneToOneField(to='game.School'),
        ),
    ]
