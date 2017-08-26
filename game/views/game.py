from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django import forms

from game.models import Gladiator

from game.models import School


@login_required
def game(request, school_id):
  school = get_object_or_404(School, pk=school_id)

  HANDLERS = {
    School.PERIOD.RECRUIT.value: recruit,
    School.PERIOD.ASSIGN.value: prepare,
    School.PERIOD.FIGHT.value: fight,
  }

  if not school.player.userplayer == request.user.player:
    raise PermissionDenied

  print "School Period: {}".format(school.period)

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

    if form.is_valid():
      actions_by_gladiator = {
        g: form.cleaned_data[str(g.id)] for g in gladiators
      }

      school.assign(actions_by_gladiator)
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
