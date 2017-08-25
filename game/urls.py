from django.conf.urls import url

from game.views import create_school, select_school, game

urlpatterns = [
    url(
      r'^$',
      select_school,
      name='select-school'
    ),

    url(
      r'^create-school/$',
      create_school,
      name='create-school'
    ),

    url(
      r'^game/(?P<school_id>[0-9]+)/$',
      game,
      name='game'
    ),
]
