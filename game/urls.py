from django.conf.urls import url

from . import views

urlpatterns = [
    url(
      r'^$',
      views.select_school,
      name='select-school'
    ),

    url(
      r'^school_create/$',
      views.create_school,
      name='create-school'
    ),

    url(
      r'^game/(?P<school_id>[0-9]+)/$',
      views.game,
      name='game'
    ),

    url(
      r'^players/$',
      views.players,
      name='players'
    ),

    url(
      r'^players/(?P<player_id>[0-9]+)/$',
      views.player,
      name='player'
    ),
]
