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
            name='Gladiator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('agility', models.IntegerField(default=5)),
                ('strength', models.IntegerField(default=5)),
                ('endurance', models.IntegerField(default=5)),
                ('fame', models.IntegerField(default=0)),
                ('recruit_day', models.PositiveIntegerField(default=0)),
                ('killed_on', models.IntegerField(default=None, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('win_reward', models.IntegerField(default=0)),
                ('lose_reward', models.IntegerField(default=0)),
                ('day', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('victor', models.BooleanField(default=False)),
                ('gladiator', models.ForeignKey(to='game.Gladiator')),
                ('match', models.ForeignKey(to='game.Match')),
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
                ('day', models.PositiveIntegerField(default=0)),
                ('player', models.ForeignKey(to='game.Player')),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='participants',
            field=models.ManyToManyField(to='game.Gladiator', through='game.Participation'),
        ),
        migrations.AddField(
            model_name='gladiator',
            name='school',
            field=models.ForeignKey(default=None, blank=True, to='game.School', null=True),
        ),
    ]
