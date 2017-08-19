from django.db import models
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
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
      self.generate_challenges()

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

  def generate_challenge(self):
    from game.factories import MatchFactory, SchoolFactory, GladiatorFactory
    from game.models import Challenge, Gladiator

    match = MatchFactory(entry=True)

    challenger_school = School.objects.filter(ai=True).first()
    if challenger_school is None:
      challenger_school = SchoolFactory(bot=True)

    challenger = Gladiator.active.filter(school=challenger_school).first()
    if challenger is None:
      challenger = GladiatorFactory(recruit=True, school=challenger_school)

    # Create challenge as issued by bot for posterity
    Challenge(
      status=Challenge.ACCEPTED,
      day=challenger_school.day,
      school=challenger_school,
      gladiator=challenger,
      match=match,
    ).save()

    # Return a challenge to the current school
    challenge = Challenge(
      status=Challenge.ISSUED,
      day=self.day,
      school=self,
      match=match,
    )

    challenge.save()

    return challenge

  def generate_challenges(self, count=3):
    from game.models import Challenge

    challenges = list(
      Challenge.issued.filter(
        school=self,
      )
    )

    for challenge in challenges:
      challenge.status = Challenge.REJECTED
      challenge.save()

    return [self.generate_challenge() for _ in range(count)]

  # @receiver(models.signals.post_save, sender='game.School')
  # def setup_school(sender, instance, created, **kwargs):
  #   """
  #   Run setup logic on school. Specifically, generate initial candidates and
  #   challenges.

  #   Args:
  #     sender: [description]
  #     instance: [description]
  #     created: [description]
  #     **kwargs: [description]
  #   """
  #   if created:
  #     instance.generate_candidates()
  #     instance.generate_challenges()

  def can_purchase(self, amount):
    return True if (self.denarii - amount) >= 0 else False

  def purchase(self, amount):
    if self.can_purchase(amount):
      self.denarii -= amount
      self.save()
    else:
      raise StandardError("Cannot purchase. Not enough denarii.")
