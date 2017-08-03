from factory import DjangoModelFactory, lazy_attribute
import faker
fake = faker.Faker()

class UserFactory(DjangoModelFactory):
  class Meta:
    model = 'auth.User'

  first_name = lazy_attribute(lambda x: fake.first_name())
  last_name = lazy_attribute(lambda x: fake.last_name())
  username = lazy_attribute(lambda x: x.first_name + "." + x.last_name)
