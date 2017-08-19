from factory import (
  DjangoModelFactory,
  lazy_attribute,
  SubFactory,
  Trait,
)
from game.models import School
import random
import faker
fake = faker.Faker()


class SchoolFactory(DjangoModelFactory):
  class Meta:
    model = 'game.School'
    django_get_or_create = ('player',)

  player = SubFactory('game.factories.PlayerFactory')
  name = lazy_attribute(lambda x: fake.company())
  denarii = lazy_attribute(lambda x: random.randint(0, 1000000))
  day = lazy_attribute(lambda x: random.randint(0, 500))
  period = lazy_attribute(lambda x: random.choice(School.PERIODS))
  ai = False

  class Params:
    bot = Trait(
      ai=True,
    )
