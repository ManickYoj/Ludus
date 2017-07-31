from django.db import models

from _consts import ATTR_DEFAULT, NAME_MAX_LENGTH


class Gladiator(models.Model):
  # Data
  name = models.CharField(max_length=NAME_MAX_LENGTH)
  value = models.IntegerField(default=0)
  fame = models.IntegerField(default=0)

  agility = models.IntegerField(default=ATTR_DEFAULT)
  strength = models.IntegerField(default=ATTR_DEFAULT)
  endurance = models.IntegerField(default=ATTR_DEFAULT)

  recruit_day = models.PositiveIntegerField(default=0)
  killed_on = models.IntegerField(
    blank=True,
    null=True,
    default=None
  )

  # Foreign Keys
  school = models.ForeignKey(
    'School',
    blank=True,
    default=None,
    null=True,
    on_delete=models.CASCADE,
  )

  def __str__(self):
    return self.name

  class Meta:
    app_label = 'game'
