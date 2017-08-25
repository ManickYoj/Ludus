from django.db import models
import random


class Match(models.Model):
  # Data
  entry_fee = models.IntegerField(default=0)
  base_reward = models.IntegerField(default=0)
  seed = models.IntegerField()

  class Meta:
    app_label = 'game'

  def get_random_generator(self):
    random_generator = random.Random()
    random_generator.seed(self.seed)
    return random_generator
