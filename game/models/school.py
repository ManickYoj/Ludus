from django.db import models
from django.dispatch import receiver
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

  def advance_period(self):
    """
    Increment the period of the day, or advance the day if appropriate. If
    the day does advance, triggers the regeneration of recruits and
    challenges.
    """
    # TODO: When linked with recruits, ensure that this method reserves any
    # recruits with a hold on them for the next day.
    index = (School.PERIODS.index(self.period) + 1) % len(School.PERIODS)
    self.period = School.PERIODS[index]

    if index == 0:
      self.day += 1
      self.generate_candidates()

    self.save()

  def generate_candidates(self, count=3):
    """
    Generates a set of candidates totaling `count`. Candidates reserved on
    the previous day will be included in the set.

    Args:
      count: The number of candidates to be in the resulting candidate pool
      (default: {3})

    Returns:
      The `count` candidate gladiators (list)
    """
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

  @receiver(models.signals.post_save, sender='game.School')
  def setup_school(sender, instance, created, **kwargs):
    """
    Run setup logic on school. Specifically, generate initial candidates and
    challenges.

    Args:
      sender: [description]
      instance: [description]
      created: [description]
      **kwargs: [description]
    """
    if created:
      instance.generate_candidates()

  def purchase(self, amount):
    print (self.denarii)
    self.denarii -= amount
    print (self.denarii)
    print self.save
    # TODO: This save works in the shell but not on the server
    # This may be caused by something to do with transactions
    self.save()
