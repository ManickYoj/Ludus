from django.db import models
from _consts import NAME_MAX_LENGTH


class School(models.Model):
  # Enum values
  RECRUIT = 'REC'
  PREPARE = 'PRE'
  FIGHT = 'FIG'
  PERIODS = [
    RECRUIT,
    PREPARE,
    FIGHT,
  ]

  # Data
  name = models.CharField(max_length=NAME_MAX_LENGTH)
  denarii = models.PositiveIntegerField(default=2000)
  day = models.PositiveIntegerField(default=0)
  ai = models.BooleanField(default=False)
  period = models.CharField(
    max_length=3,
    choices=(
      (RECRUIT, 'Dawn'),
      (PREPARE, 'Midday'),
      (FIGHT, 'Dusk'),
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

  """
  advanceDay
  --------

  Advances the period of the day, or advances one day to the next if at the
  last period. If the day advances, triggers regenerating sets of recruits
  and challenges.
  """
  def advance_period(self):
    # TODO: When linked with recruits, ensure that this method reserves any
    # recruits with a hold on them for the next day.
    index = (School.PERIODS.index(self.period) + 1) % len(School.PERIODS)
    self.period = School.PERIODS[index]

    if index == 0:
      self.day += 1

    self.save()

  def generate_candidates(self, count=3):
    from game.models import Gladiator
    from game.factories import GladiatorFactory
    from random import choice

    # Remove all candidates from the school who were not reserved yesterday
    Gladiator.candidates.filter(
      school=self,
    ).exclude(
      reserved_on=self.day - 1
    ).delete()

    candidates = list(Gladiator.candidates.filter(
      school=self
    ))

    generators = [
      lambda: GladiatorFactory(convict=True, school=self),
      lambda: GladiatorFactory(conscript=True, school=self),
    ]

    # Generate a new candidate from a random generator until we have filled up
    # the roster
    while len(candidates) < count:
      candidates.append(choice(generators)())

    return candidates
