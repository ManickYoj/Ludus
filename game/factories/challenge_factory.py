from factory import (
  DjangoModelFactory,
  Trait,
)
from game.models import Challenge
import faker
import random
fake = faker.Faker()


class ChallengeFactory(DjangoModelFactory):
  class Meta:
    model = 'game.Challenge'

  status = Challenge.ISSUED

  class Params:
    entry = Trait(
      entry_fee=0,
      base_reward=random.randint(1, 3) * 100,
    )
