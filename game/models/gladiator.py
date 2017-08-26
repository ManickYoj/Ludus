from django.db import models
import random

from _consts import NAME_MAX_LENGTH, FIRST_NAMES, FAMILY_NAMES


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
  class Meta:
    app_label = 'game'

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

  agility = models.IntegerField(default=0)
  strength = models.IntegerField(default=0)
  endurance = models.IntegerField(default=0)

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

  @classmethod
  def generate(cls, school, fame=0):
    skill_points = (fame / 10) + 6
    skills = {
      'agility': 0,
      'strength': 0,
      'endurance': 0,
    }

    for i in range(skill_points):
      skill_name = random.choice(skills.keys())
      skills[skill_name] += 1

    gladiator = cls(
      name=random.choice(FIRST_NAMES) + " " + random.choice(FAMILY_NAMES),
      school=school,
      agility=skills['agility'],
      strength=skills['strength'],
      endurance=skills['endurance'],
    )

    gladiator.save()

    return gladiator

  def __str__(self):
    return self.name

  def recruit(self):
    """
    Recruit a candidate gladiator.

    Updates the current gladiator object to reflect that it has been recruited.
    """
    print "Recruiting Gladiator ... "
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
