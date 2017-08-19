from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User

from _consts import NAME_MAX_LENGTH


class Player(models.Model):
  # Data
  name = models.CharField(max_length=NAME_MAX_LENGTH)

  class Meta:
    app_label = 'game'

  def __str__(self):
    return self.name


class UserPlayer(Player):
  # Foreign Keys
  user = models.OneToOneField(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    parent_link=True,
    related_name='player'
  )

  class Meta:
    app_label = 'game'

  def __str__(self):
    return self.name


# Create a new Player object when a new user registers
@receiver(models.signals.post_save, sender=User)
def create_player(sender, instance, created, **kwargs):
  if created:
    UserPlayer.objects.create(
      user=instance,
      name=instance.username
    )


# If the User model is updated, ensure the Player is too
@receiver(models.signals.post_save, sender=User)
def save_player(sender, instance, created, **kwargs):
  instance.player.save()


class BotPlayer(Player):
  # Foreign Keys
  pass

  class Meta:
    app_label = 'game'

  def __str__(self):
    return self.name
