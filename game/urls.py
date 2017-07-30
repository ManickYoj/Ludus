from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.school_select, name='school_select'),

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
