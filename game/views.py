from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory
from django.core.exceptions import PermissionDenied
from django import forms

from models import Player, School, Gladiator


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


# This form is not actually used on the recruit page at present
# Rather, a matching custom form is rendered (to make the layout easier)
# and this class is used to validate the form response
class RecruitmentForm(forms.Form):
  def __init__(self, candidates, *args, **kwargs):
    super(RecruitmentForm, self).__init__(*args, **kwargs)

    candiate_choices = [(c.id, c.name) for c in candidates]
    candiate_choices.append(("-1", 'Do not recruit a gladiator today.'))

    self.fields['recruit_id'] = forms.ChoiceField(
      choices=candiate_choices,
      widget=forms.RadioSelect,
    )


def recruit(request, school):
  candidates = school.gladiator_set.filter(recruited_on=None)

  if request.method == 'POST':
    form = RecruitmentForm(candidates, request.POST)

    if form.is_valid():
      recruit_id = int(form.cleaned_data['recruit_id'])
      candidate_ids = [c.id for c in candidates]

      if recruit_id in candidate_ids:
        recruit = get_object_or_404(Gladiator, pk=recruit_id)

        try:
          school.purchase(recruit.value)
          recruit.recruit()
          school.advance_period()
          return redirect('game:game', school_id=school.id)
        except StandardError as err:
          form.add_error(None, err)

      elif recruit_id == -1:
        school.advance_period()
        return redirect('game:game', school_id=school.id)

  else:
    form = RecruitmentForm(candidates)

  context = {
    'school': school,
    'candidates': candidates,
    'form': form,
  }

  return render(request, 'pages/recruit.html', context)


class PrepareForm(forms.Form):
  def __init__(self, gladiators, *args, **kwargs):
    super(PrepareForm, self).__init__(*args, **kwargs)

    train_choices = [
      ("FIGH", "Enter in Fight"),
      ("SPAR", "Spar with Gladiators"),
      ("PRAC", "Practice with Dummy"),
      ("REST", "Rest"),
    ]

    # self.fields['test'] = forms.ChoiceField(
    #   label=gladiators[0].name,
    #   choices=train_choices,
    #   widget=forms.RadioSelect,
    #   initial="REST",
    # )
    self.fields.update({
      str(g.id): forms.ChoiceField(
        label=g.name,
        choices=train_choices,
        widget=forms.RadioSelect,
        initial="REST",
      ) for g in gladiators
    })


def prepare(request, school):
  gladiators = Gladiator.active.filter(school=school)

  if request.method == 'POST':
    form = PrepareForm(gladiators, request.POST)
    print request.POST
    print form.data

    if form.is_valid():
      for gladiator in gladiators:
        action = form.cleaned_data[str(gladiator.id)]
        gladiator.prepare(action)

      school.advance_period()
      return redirect('game:game', school_id=school.id)

  else:
    form = PrepareForm(gladiators)

  context = {
    'school': school,
    'gladiators': gladiators,
    'form': form,
  }

  return render(request, 'pages/prepare.html', context)


def fight(request, school):
  school.advance_period()
  return redirect('game:game', school_id=school.id)
