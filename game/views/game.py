from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied, ValidationError
from django import forms

from game.models import Gladiator

from game.models import School


@login_required
def game(request, school_id):
  school = get_object_or_404(School, pk=school_id)

  HANDLERS = {
    School.PERIOD.RECRUIT.value: recruit,
    School.PERIOD.ASSIGN.value: Assign,
    School.PERIOD.FIGHT.value: fight,
  }

  if not school.player.userplayer == request.user.player:
    raise PermissionDenied

  return HANDLERS[school.period](request, school)


# This form is not actually used on the recruit page at present
# Rather, a matching custom form is rendered (to make the layout easier)
# and this class is used to validate the form response
class RecruitmentForm(forms.Form):
  def __init__(self, school, candidates, *args, **kwargs):
    super(RecruitmentForm, self).__init__(*args, **kwargs)
    self.school = school

    candiate_choices = [(c.id, c.name) for c in candidates]

    candiate_choices.append(("-1", 'NO-RECRUIT'))

    self.fields['recruit_id'] = forms.ChoiceField(
      choices=candiate_choices,
      widget=forms.RadioSelect,
    )

  def clean_recruit_id(self):
    # Only allow a player to opt out of recruitment if they have at least
    # one gladiator
    if (
      self.cleaned_data['recruit_id'] == "-1" and
      Gladiator.active.filter(school=self.school).count() == 0
    ):
      err = (
        'Cannot opt out of recruitment if you have no live gladiators.'
      )
      # TODO: This should be field specific, but the page doesn't display
      # field specific errors right now
      self.add_error(None, err)

    return self.cleaned_data['recruit_id']


def recruit(request, school):
  candidates = school.gladiator_set.filter(recruited_on=None)

  if request.method == 'POST':
    form = RecruitmentForm(school, candidates, request.POST)

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
    form = RecruitmentForm(school, candidates)

  context = {
    'school': school,
    'candidates': candidates,
    'form': form,
  }

  return render(request, 'pages/recruit.html', context)


class AssignForm(forms.Form):
  def __init__(self, gladiators, *args, **kwargs):
    super(AssignForm, self).__init__(*args, **kwargs)
    self.gladiators = gladiators

    self.fields.update({
      str(g.id): forms.ChoiceField(
        label=g.name,
        choices=[(a.value, a.desc()) for a in School.ASSIGNMENTS],
        widget=forms.RadioSelect,
        initial=School.ASSIGNMENTS.REST.value,
      ) for g in gladiators
    })

  def clean(self):
    super(AssignForm, self).clean()
    assignments = School.ASSIGNMENTS
    gladiators_by_action = {a: [] for a in assignments}

    for gladiator in self.gladiators:
      action = assignments(int(self.cleaned_data[str(gladiator.id)]))
      gladiators_by_action.setdefault(action, []).append(gladiator)

    if len(gladiators_by_action[assignments.FIGHT]) != 1:
      err = "Must have exactly one gladiator entered in a fight."
      self.add_error(None, err)

    if not (
      len(gladiators_by_action[assignments.SPAR]) == 0 or
      len(gladiators_by_action[assignments.SPAR]) == 2
    ):
      err = (
        "Must have exactly two gladiators (or none) "
        "as sparring partners."
      )
      self.add_error(None, err)

    if len(gladiators_by_action[assignments.PRACTICE]) > 3:
      err = (
        "A maximum of three gladiators can spar. "
        "We've only got so many dummies!"
      )
      self.add_error(None, err)

    self.cleaned_data['gladiators_by_action'] = gladiators_by_action

    return self.cleaned_data


def Assign(request, school):
  gladiators = Gladiator.active.filter(school=school)

  if request.method == 'POST':
    form = AssignForm(gladiators, request.POST)

    if form.is_valid():
      gladiators_by_action = form.cleaned_data['gladiators_by_action']

      school.assign(gladiators_by_action)
      school.advance_period()

      return redirect('game:game', school_id=school.id)

  else:
    form = AssignForm(gladiators)

  context = {
    'school': school,
    'gladiators': gladiators,
    'form': form,
  }

  return render(request, 'pages/assign.html', context)


def fight(request, school):
  school.advance_period()
  return redirect('game:game', school_id=school.id)
