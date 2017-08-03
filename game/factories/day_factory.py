from factory import DjangoModelFactory, lazy_attribute, SubFactory
import random

class DayFactory(DjangoModelFactory):
  class Meta:
    model = 'game.Day'
    django_get_or_create = ('school', )

  school = SubFactory('game.factories.SchoolFactory')
  number = lazy_attribute(lambda x: random.randint(0, 2000))