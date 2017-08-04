# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=3, choices=[(b'ISS', b'Issued'), (b'ACC', b'Accepted'), (b'REJ', b'Rejected'), (b'WON', b'Won'), (b'LOS', b'Lost')])),
                ('day', models.PositiveIntegerField(default=None, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Gladiator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('background', models.CharField(max_length=60)),
                ('value', models.IntegerField(default=0)),
                ('fame', models.IntegerField(default=0)),
                ('agility', models.IntegerField(default=0)),
                ('strength', models.IntegerField(default=0)),
                ('endurance', models.IntegerField(default=0)),
                ('reserved_on', models.PositiveIntegerField(default=None, null=True, blank=True)),
                ('recruited_on', models.PositiveIntegerField(default=None, null=True, blank=True)),
                ('killed_on', models.PositiveIntegerField(default=None, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('base_pay', models.IntegerField(default=0)),
                ('base_reward', models.IntegerField(default=0)),
                ('seed', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('denarii', models.PositiveIntegerField(default=2000)),
                ('day', models.PositiveIntegerField(default=0)),
                ('ai', models.BooleanField(default=False)),
                ('period', models.CharField(default=b'REC', max_length=3, choices=[(b'REC', b'Dawn'), (b'PRE', b'Midday'), (b'FIG', b'Dusk')])),
                ('player', models.ForeignKey(to='game.Player')),
            ],
        ),
        migrations.AddField(
            model_name='gladiator',
            name='school',
            field=models.ForeignKey(to='game.School'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='gladiator',
            field=models.OneToOneField(null=True, default=None, blank=True, to='game.Gladiator'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='match',
            field=models.ForeignKey(to='game.Match'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='school',
            field=models.OneToOneField(to='game.School'),
        ),
    ]
