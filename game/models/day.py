from django.db import models
from django.dispatch import receiver
from django.contrib import admin


class Day(models.Model):
  # Enum values
  RECRUIT = 'REC'
  PREPARE = 'PRE'
  FIGHT = 'FIG'
  PHASES = [
    RECRUIT,
    PREPARE,
    FIGHT,
  ]

  # Data
  number = models.PositiveIntegerField(default=0)
  phase = models.CharField(
    max_length=3,
    choices=(
      (RECRUIT, 'Dawn'),
      (PREPARE, 'Midday'),
      (FIGHT, 'Dusk'),
    ),
    default=RECRUIT
  )

  # Foreign Keys
  school = models.OneToOneField(
    'School',
    on_delete=models.CASCADE
  )

  """
  advance
  -------

  Increments the current day's phase. If the day is ending, creates the next
  day instead and replaces the current day with tomorrow.
  """
  def advance(self):
    index = Day.PHASES.index(self.phase)
    index += 1

    # If it's the end of the day, advance to tomorrow
    if index == len(Day.PHASES):
      self.tomorrow()

    # If it's not the end of the day, advance to the next phase
    else:
      self.phase = Day.PHASES[index]
      self.save()

  """
  tomorrow
  --------

  Creates a new day object representing the day after the current. Deletes
  the current day from the database and advances the school's day pointer
  to the next day.
  """
  def tomorrow(self):
    # TODO: When linked with recruits, ensure that this method reserves any
    # recruits with a hold on them for the next day.

    # Delete the current object's db record
    self.delete()

    # Create the new record in the db
    Day.objects.create(
      school=self.school,
      number=(self.number + 1),
    )

    # Update school so that it references new day
    self.school.save()

  class Meta:
    app_label = 'game'


# Create an associated day when a new school is created
@receiver(models.signals.post_save, sender='game.School')
def create_day(sender, instance, created, **kwargs):
  if created:
    Day.objects.get_or_create(school=instance)


# If the School model is updated, ensure the Day is too
@receiver(models.signals.post_save, sender='game.School')
def save_player(sender, instance, created, **kwargs):
  instance.player.save()


# Display in admin UI
# TODO: Why is this needed here but not on other classes
admin.site.register(Day)
