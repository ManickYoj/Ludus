from factory import DjangoModelFactory, lazy_attribute, SubFactory


class PlayerFactory(DjangoModelFactory):
  class Meta:
    model = 'game.Player'
    django_get_or_create = ('user',)

  user = SubFactory('game.factories.UserFactory')
  name = lazy_attribute(lambda x: x.user.username)
