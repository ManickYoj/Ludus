from factory import DjangoModelFactory, lazy_attribute
import faker
fake = faker.Faker()


class PlayerFactory(DjangoModelFactory):
  class Meta:
    model = 'game.Player'

  name = lazy_attribute(lambda x: fake.first_name() + fake.last_name())
