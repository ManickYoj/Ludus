# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20170731_1300'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recruit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('value', models.IntegerField(default=0)),
                ('fame', models.IntegerField(default=0)),
                ('agility', models.IntegerField(default=0)),
                ('strength', models.IntegerField(default=0)),
                ('endurance', models.IntegerField(default=0)),
                ('reserved', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='day',
            name='phase',
            field=models.CharField(default=b'REC', max_length=3, choices=[(b'REC', b'Dawn'), (b'PRE', b'Midday'), (b'FIG', b'Dusk')]),
        ),
        migrations.AddField(
            model_name='recruit',
            name='day',
            field=models.ForeignKey(to='game.Day'),
        ),
    ]
