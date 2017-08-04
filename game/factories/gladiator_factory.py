from factory import (
  DjangoModelFactory,
  lazy_attribute,
  Trait,
)
import faker
import random
fake = faker.Faker()


def gen_stat(min_val=0, max_val=5):
  base = random.triangular(0, 1, .5)
  return int(round(base * (max_val - min_val) + min_val))


class GladiatorFactory(DjangoModelFactory):
  class Meta:
    model = 'game.Gladiator'

  name = lazy_attribute(lambda x: fake.first_name())

  class Params:
    recruit = Trait(
      reserved_on=None,
      recruited_on=None,
      killed_on=None,
    )

    convict = Trait(
      recruit=True,
      background='Convict',
      fame=0,
      value=0,

      agility=gen_stat(2, 5),
      strength=gen_stat(2, 5),
      endurance=gen_stat(2, 5),
    )

    conscript = Trait(
      recruit=True,
      background='Conscripted Deserter',
      fame=10,
      value=200,

      agility=gen_stat(4, 7),
      strength=gen_stat(4, 7),
      endurance=gen_stat(4, 7),
    )
