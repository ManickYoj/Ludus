from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory
from django.core.exceptions import PermissionDenied

from models import Player, School


@login_required
def select_school(request):
  context = {
    'schools': request.user.player.school_set.all(),
  }
  return render(request, 'select_school.html', context)


@login_required
def create_school(request):
  CreateSchoolForm = modelform_factory(School, fields=["name"])

  if request.method == 'POST':
    form = CreateSchoolForm(request.POST)

    if form.is_valid():
      instance = form.save(commit=False)
      instance.player = request.user.player
      instance.save()
      return redirect('game:select-school')

  else:
    form = CreateSchoolForm()

  return render(request, 'create_school.html', {'form': form})


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


@login_required
def game(request, school_id):
  school = get_object_or_404(School, pk=school_id)

  HANDLERS = {
    School.RECRUIT: recruit,
    School.PREPARE: prepare,
    School.FIGHT: fight,
  }

  if not school.player.user == request.user:
    raise PermissionDenied

  return HANDLERS[school.period](request, school)


def recruit(request, school):
  context = {
    'school': school,
    'candidates': school.gladiator_set.filter(recruited_on=None),
  }
  return render(request, 'pages/recruit.html', context)


def prepare(self):
  pass


def fight(self):
  pass
