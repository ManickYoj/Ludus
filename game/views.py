from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Player


@login_required
def school_select(request):
  print "foo"
  return render(request, 'school_select.html')


@login_required
def players(request):
  return render(
    request,
    'players.html',
    {
      "players": Player.objects.all()
    }
  )


@login_required
def player(request, player_id):
  player = get_object_or_404(Player, pk=player_id)
  return HttpResponse("Hello %s" % player.name)
