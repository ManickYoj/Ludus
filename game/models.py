from django.db import models
from django.conf import settings


NAME_MAX_LENGTH = 60
ATTR_DEFAULT = 5


class Player(models.Model):
  # Data
  name = models.CharField(max_length=NAME_MAX_LENGTH)

  # Foreign Keys
  user = models.OneToOneField(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
  )

  def __str__(self):
    return self.name


class School(models.Model):
  # Data
  name = models.CharField(max_length=NAME_MAX_LENGTH)
  day = models.PositiveIntegerField(default=0)

  # Foreign Keys
  player = models.ForeignKey(
    Player,
    on_delete=models.CASCADE
  )

  def __str__(self):
    return self.name


class Gladiator(models.Model):
  # Data
  name = models.CharField(max_length=NAME_MAX_LENGTH)
  agility = models.IntegerField(default=ATTR_DEFAULT)
  strength = models.IntegerField(default=ATTR_DEFAULT)
  endurance = models.IntegerField(default=ATTR_DEFAULT)
  fame = models.IntegerField(default=0)
  recruit_day = models.PositiveIntegerField(default=0)
  killed_on = models.IntegerField(
    blank=True,
    null=True,
    default=None
  )

  # Foreign Keys
  school = models.ForeignKey(
    School,
    blank=True,
    default=None,
    null=True,
    on_delete=models.CASCADE,
  )

  def __str__(self):
    return self.name


class Match(models.Model):
  # Data
  win_reward = models.IntegerField(default=0)
  lose_reward = models.IntegerField(default=0)
  day = models.PositiveIntegerField(default=0)

  # Foreign Keys
  participants = models.ManyToManyField(
    Gladiator,
    through='Participation'
  )


class Participation(models.Model):
  # Data
  victor = models.BooleanField(default=False)

  # Foreign Keys
  gladiator = models.ForeignKey(
    Gladiator,
    on_delete=models.CASCADE
  )
  match = models.ForeignKey(
    Match,
    on_delete=models.CASCADE
  )
