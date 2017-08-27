from django.db import models
import enum

from game.models import Gladiator
from _consts import NAME_MAX_LENGTH


class School(models.Model):
  class Meta:
    app_label = 'game'

  @enum.unique
  class ASSIGNMENTS(enum.IntEnum):
    FIGHT = 0
    SPAR = 1
    PRACTICE = 2
    REST = 3

    def desc(self):
      cls = self.__class__
      descriptions = {
        cls.FIGHT: "Enter in Fight",
        cls.SPAR: "Spar with Another Gladiator",
        cls.PRACTICE: "Practice with Dummy",
        cls.REST: "Rest",
      }
      return descriptions[self]

  @enum.unique
  class PERIOD(enum.IntEnum):
    RECRUIT = 0
    ASSIGN = 1
    FIGHT = 2

    def next(self):
      cls = self.__class__
      members = list(cls)
      index = (members.index(self) + 1) % len(cls)
      return members[index]

  # Data
  name = models.CharField(max_length=NAME_MAX_LENGTH)
  denarii = models.PositiveIntegerField(default=2000)
  day = models.PositiveIntegerField(default=0)
  ai = models.BooleanField(default=False)
  _period = models.IntegerField(
    choices=((x.value, x.name.title()) for x in PERIOD),
    default=PERIOD.RECRUIT.value,
  )

  # Foreign Keys
  player = models.ForeignKey(
    'Player',
    on_delete=models.CASCADE
  )

  @property
  def period(self):
    return School.PERIOD(self._period)

  @period.setter
  def period(self, value):
    self._period = value

  def __str__(self):
    return self.name

  def advance_period(self):
    """
    Increment the period of the day, or advance the day if appropriate. If
    the day does advance, triggers the regeneration of recruits and
    challenges.
    """
    self.period = self.period.next()

    if self.period.value == 0:
      self.day += 1
      self.generate_candidates()
      # self.generate_challenges()

    self.save()

  def assign(self, gladiators_by_action):
    # TODO: Delete this debug block
    import pprint
    pp = pprint.PrettyPrinter()
    pp.pprint(gladiators_by_action)

    # TODO: Do this.

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

    # Remove all candidates from the school who were not reserved yesterday
    Gladiator.candidates.filter(
      school=self,
    ).exclude(
      reserved_on=self.day - 1
    ).delete()

    candidates = list(Gladiator.candidates.filter(school=self))

    # Generate new candidates until we have filled up the roster
    while len(candidates) < count:
      candidates.append(Gladiator.generate(school=self))

    return candidates

  def can_purchase(self, amount):
    return True if (self.denarii - amount) >= 0 else False

  def purchase(self, amount):
    if self.can_purchase(amount):
      self.denarii -= amount
      self.save()
    else:
      raise StandardError("Cannot purchase. Not enough denarii.")

  # def generate_challenge(self):
  #   from game.factories import MatchFactory, SchoolFactory, GladiatorFactory
  #   from game.models import Challenge, Gladiator

  #   challenger_school = School.objects.filter(ai=True).first()
  #   if challenger_school is None:
  #     challenger_school = SchoolFactory(bot=True)

  #   challenger = Gladiator.active.filter(school=challenger_school).first()
  #   if challenger is None:
  #     challenger = GladiatorFactory(recruit=True, school=challenger_school)

  # def generate_challenges(self, count=3):
  #   from game.models import Challenge

  #   challenges = list(
  #     Challenge.issued.filter(
  #       school=self,
  #     )
  #   )

  #   for challenge in challenges:
  #     challenge.status = Challenge.REJECTED
  #     challenge.save()

  #   return [self.generate_challenge() for _ in range(count)]
