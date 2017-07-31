from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User

from _consts import NAME_MAX_LENGTH


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

  class Meta:
    app_label = 'game'


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
