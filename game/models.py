from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User

NAME_MAX_LENGTH = 60
ATTR_DEFAULT = 0


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


# Create a new Player object when a new user registers
@receiver(models.signals.post_save, sender=User)
def create_player(sender, instance, created, **kwargs):
  if created:
    Player.objects.create(
      user=instance,
      name=instance.username
    )


# If the User model is updated, ensure the Player is too
@receiver(models.signals.post_save, sender=User)
def save_player(sender, instance, created, **kwargs):
  instance.player.save()


class School(models.Model):
  # Enum values
  RECRUIT = 'REC'
  PREPARE = 'PRE'
  FIGHT = 'FIG'
  END = 'END'

  # Data
  name = models.CharField(max_length=NAME_MAX_LENGTH)
  day = models.PositiveIntegerField(default=0)
  denarii = models.PositiveIntegerField(default=2000)
  day_phase = models.CharField(
    max_length=3,
    choices=(
      (RECRUIT, 'Recruit'),
      (PREPARE, 'Prepare'),
      (FIGHT, 'Fight'),
      (END, 'End of Day'),
    ),
    default=RECRUIT
  )

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
  value = models.IntegerField(default=0)
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
