# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='gladiator',
            field=models.ForeignKey(default=None, blank=True, to='game.Gladiator', null=True),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='school',
            field=models.ForeignKey(to='game.School'),
        ),
        migrations.AlterField(
            model_name='userplayer',
            name='user',
            field=models.OneToOneField(parent_link=True, related_name='player', to=settings.AUTH_USER_MODEL),
        ),
    ]
