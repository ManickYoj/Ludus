from factory import (
  DjangoModelFactory,
  Trait,
)
import faker
import random
fake = faker.Faker()


class MatchFactory(DjangoModelFactory):
  class Meta:
    model = 'game.Match'

  seed = random.randint(-1024, 1024)

  class Params:
    entry = Trait(
      entry_fee=0,
      base_reward=random.randint(1, 3) * 100,
    )
