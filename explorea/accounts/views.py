from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from .forms import RegisterForm


def profile(request):
    """
    Page with user information.
    """

    return render(request, 'accounts/profile.html')


def register(request):
    """
    Registration form.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            password = form.cleaned_data.get('password1')

            auth_user = authenticate(username=user.username, password=password)
            login(request, auth_user)

            return redirect('profile')

    return render(request, 'accounts/register.html', {'form': RegisterForm()})
