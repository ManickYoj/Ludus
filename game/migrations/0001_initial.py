# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [(b'game', '0001_initial'), (b'game', '0002_auto_20170826_1931'), (b'game', '0003_auto_20170826_1934')]

    dependencies = [
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
                ('entry_fee', models.IntegerField(default=0)),
                ('base_reward', models.IntegerField(default=0)),
                ('seed', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
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
                ('period', models.IntegerField(default=(0, b'Recruit'), choices=[(0, b'Recruit'), (1, b'Assign'), (2, b'Fight')])),
            ],
        ),
        migrations.CreateModel(
            name='BotPlayer',
            fields=[
                ('player_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='game.Player')),
            ],
            bases=('game.player',),
        ),
        migrations.CreateModel(
            name='UserPlayer',
            fields=[
                ('player_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='game.Player')),
                ('user', models.OneToOneField(parent_link=True, related_name='player', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('game.player',),
        ),
        migrations.AddField(
            model_name='school',
            name='player',
            field=models.ForeignKey(to='game.Player'),
        ),
        migrations.AddField(
            model_name='gladiator',
            name='school',
            field=models.ForeignKey(to='game.School'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='gladiator',
            field=models.ForeignKey(default=None, blank=True, to='game.Gladiator', null=True),
        ),
        migrations.AddField(
            model_name='challenge',
            name='match',
            field=models.ForeignKey(to='game.Match'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='school',
            field=models.ForeignKey(to='game.School'),
        ),
        migrations.RenameField(
            model_name='school',
            old_name='period',
            new_name='_period',
        ),
        migrations.AlterField(
            model_name='school',
            name='_period',
            field=models.IntegerField(default=0, choices=[(0, b'Recruit'), (1, b'Assign'), (2, b'Fight')]),
        ),
    ]
