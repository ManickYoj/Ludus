from django.db import models

from _consts import NAME_MAX_LENGTH


class School(models.Model):
  # Enum values
  RECRUIT = 'REC'
  PREPARE = 'PRE'
  FIGHT = 'FIG'
  END = 'END'

  # Data
  name = models.CharField(max_length=NAME_MAX_LENGTH)
  day = models.PositiveIntegerField(default=0)
  denarii = models.PositiveIntegerField(default=2000)
  day_phase = models.CharField(
    max_length=3,
    choices=(
      (RECRUIT, 'Recruit'),
      (PREPARE, 'Prepare'),
      (FIGHT, 'Fight'),
      (END, 'End of Day'),
    ),
    default=RECRUIT
  )

  # Foreign Keys
  player = models.ForeignKey(
    'Player',
    on_delete=models.CASCADE
  )

  def __str__(self):
    return self.name

  class Meta:
    app_label = 'game'
