from django.db import models

from _consts import NAME_MAX_LENGTH


class School(models.Model):

  # Data
  name = models.CharField(max_length=NAME_MAX_LENGTH)
  denarii = models.PositiveIntegerField(default=2000)

  # Foreign Keys
  player = models.ForeignKey(
    'Player',
    on_delete=models.CASCADE
  )

  def __str__(self):
    return self.name

  class Meta:
    app_label = 'game'
