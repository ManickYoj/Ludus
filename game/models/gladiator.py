from django.db import models

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
  active = ActiveManager()
  candidates = CandidateManager()
  killed = KilledManager()

  # Data
  name = models.CharField(max_length=NAME_MAX_LENGTH)
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

  # Foreign Key
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

  def recruit(self):
    """
    Recruit a candidate gladiator.

    Updates the current gladiator object to reflect that it has been recruited.
    """
    self.recruited_on = self.school.day
    self.recruited = True
    self.reserved = False
    self.save()
