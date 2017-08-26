from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.forms import modelform_factory

from game.models import School


@login_required
def create_school(request):
  CreateSchoolForm = modelform_factory(School, fields=["name"])

  if request.method == 'POST':
    form = CreateSchoolForm(request.POST)

    if form.is_valid():
      instance = form.save(commit=False)
      instance.player = request.user.player
      instance.save()
      instance.generate_candidates()
      return redirect('game:select-school')

  else:
    form = CreateSchoolForm()

  return render(request, 'create_school.html', {'form': form})
