from django.db import models
import random

from _consts import ATTR_DEFAULT, NAME_MAX_LENGTH


class ActiveManager(models.Manager):
  def get_queryset(self):
    return super(
      ActiveManager, self
    ).get_queryset().filter(
      killed_on=None
    ).exclude(
      recruited_on=None
    )


class CandidateManager(models.Manager):
  def get_queryset(self):
    return super(
      CandidateManager, self
    ).get_queryset().filter(recruited_on=None)


class KilledManager(models.Manager):
  def get_queryset(self):
    return super(
      KilledManager, self
    ).get_queryset().exclude(killed_on=None)


class Gladiator(models.Model):
  # Managers
  objects = models.Manager()
  active = ActiveManager()
  candidates = CandidateManager()
  killed = KilledManager()

  # Data
  name = models.CharField(max_length=NAME_MAX_LENGTH)
  background = models.CharField(max_length=NAME_MAX_LENGTH)
  value = models.IntegerField(default=0)
  fame = models.IntegerField(default=0)

  agility = models.IntegerField(default=ATTR_DEFAULT)
  strength = models.IntegerField(default=ATTR_DEFAULT)
  endurance = models.IntegerField(default=ATTR_DEFAULT)

  reserved_on = models.PositiveIntegerField(
    blank=True,
    null=True,
    default=None
  )
  recruited_on = models.PositiveIntegerField(
    blank=True,
    null=True,
    default=None,
  )
  killed_on = models.PositiveIntegerField(
    blank=True,
    null=True,
    default=None
  )

  # Foreign Keys
  school = models.ForeignKey(
    'School',
    on_delete=models.CASCADE,
  )

  def __str__(self):
    return self.name

  class Meta:
    app_label = 'game'

  def recruit(self):
    """
    Recruit a candidate gladiator.

    Updates the current gladiator object to reflect that it has been recruited.
    """
    self.recruited_on = self.school.day
    self.recruited = True
    self.reserved = False
    self.save()

  def increment_agility(self, incr):
    self.agility += incr
    self.save()

  def increment_endurance(self, incr):
    self.endurance += incr
    self.save()

  def increment_strength(self, incr):
    self.strength += incr
    self.save()

  def prepare(self, action):
    if action in ['SPAR', 'PRAC']:
      incr_func = random.choice[
        self.increment_agility,
        self.increment_endurance,
        self.increment_strength
      ]

      incr_func(1)

    elif action == 'FIGH':
      # TODO: Enter in match
      pass
