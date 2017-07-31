from django.apps import AppConfig

default_app_config = 'game.__init__.GameConfig'


class GameConfig(AppConfig):
  name = 'game'
  verbose_name = 'Game'
