from django.db import models


class Match(models.Model):
  # Data
  win_reward = models.IntegerField(default=0)
  lose_reward = models.IntegerField(default=0)
  day = models.PositiveIntegerField(default=0)

  # Foreign Keys
  participants = models.ManyToManyField(
    'Gladiator',
    through='Participation'
  )

  class Meta:
    app_label = 'game'
