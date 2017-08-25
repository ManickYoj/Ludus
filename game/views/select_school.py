from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def select_school(request):
  context = {
    'schools': request.user.player.school_set.all(),
  }
  return render(request, 'select_school.html', context)
