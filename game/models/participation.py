from django.db import models


class Participation(models.Model):
  # Data
  victor = models.BooleanField(default=False)

  # Foreign Keys
  gladiator = models.ForeignKey(
    'Gladiator',
    on_delete=models.CASCADE
  )
  match = models.ForeignKey(
    'Match',
    on_delete=models.CASCADE
  )

  class Meta:
    app_label = 'game'
