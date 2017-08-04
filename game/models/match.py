from django.db import models


class Match(models.Model):
  # Data
  base_pay = models.IntegerField(default=0)
  base_reward = models.IntegerField(default=0)
  seed = models.IntegerField()

  class Meta:
    app_label = 'game'
