from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login


def home(request):
  return render(request, 'home.html')


def signup(request):
  # Create a new user if a viewer is sending user info
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():

      # Create new user
      form.save()

      # Login new user
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password1')
      user = authenticate(username=username, password=password)
      login(request, user)

      # Redirect the new user to the game app
      return redirect('game:school_select')

  else:
    form = UserCreationForm()

  return render(request, 'registration/signup.html', {'form': form})
