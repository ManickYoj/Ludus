from factory import DjangoModelFactory, lazy_attribute


class BotPlayerFactory(DjangoModelFactory):
  class Meta:
    model = 'game.BotPlayer'

  name = lazy_attribute(lambda x: x.user.username)
