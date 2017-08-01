from django.db import models
from django.contrib import admin

from _consts import ATTR_DEFAULT, NAME_MAX_LENGTH


class GladiatorBase(models.Model):
  # Data
  name = models.CharField(max_length=NAME_MAX_LENGTH)
  value = models.IntegerField(default=0)
  fame = models.IntegerField(default=0)

  agility = models.IntegerField(default=ATTR_DEFAULT)
  strength = models.IntegerField(default=ATTR_DEFAULT)
  endurance = models.IntegerField(default=ATTR_DEFAULT)

  def __str__(self):
    return self.name

  class Meta:
    app_label = 'game'
    abstract = True


class Gladiator(GladiatorBase):
  # Data
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


class Recruit(GladiatorBase):
  # Data
  reserved = models.BooleanField(default=False)

  # Foreign Keys
  day = models.ForeignKey(
    'Day',
    on_delete=models.CASCADE,
  )

  """
  recruit
  -------

  Takes this recruit and adds him to the player's gladiator school by creating
  a new gladiator object with this recruit's properties. Deletes the recruit.
  """
  def recruit(self):
    new_gladiator = Gladiator()

    # Pull all data from the fields on recruit that match fields on gladiator
    # and apply the values
    for field_name, value in self.__dict__.items():
      if field_name in new_gladiator.__dict__:
        new_gladiator.__dict__[field_name] = value

    # Add any remaining custom attributes
    new_gladiator.recruit_day = self.day.number
    new_gladiator.school = self.day.school

    new_gladiator.save()

    self.delete()


# TODO: Find out why!
admin.site.register(Recruit)
