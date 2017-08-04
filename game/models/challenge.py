from django.db import models


class Challenge(models.Model):
  # Enum
  ISSUED = 'ISS'
  ACCEPTED = 'ACC'
  REJECTED = 'REJ'
  WON = 'WON'
  LOST = 'LOS'

  # Data
  status = models.CharField(
    max_length=3,
    choices=(
      (ISSUED, 'Issued'),
      (ACCEPTED, 'Accepted'),
      (REJECTED, 'Rejected'),
      (WON, 'Won'),
      (LOST, 'Lost'),
    )
  )
  day = models.PositiveIntegerField(
    null=True,
    blank=True,
    default=None,
  )

  # Foreign Keys
  school = models.OneToOneField(
    'School',
    on_delete=models.CASCADE
  )
  gladiator = models.OneToOneField(
    'Gladiator',
    on_delete=models.CASCADE,
    null=True,
    default=None,
    blank=True,
  )
  match = models.ForeignKey(
    'Match',
    on_delete=models.CASCADE
  )

  class Meta:
    app_label = 'game'

  def isAI(self):
    return self.school.ai
