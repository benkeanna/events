from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from .forms import RegisterForm, EditProfileForm


def profile(request):
    """
    Page with user information.
    """

    return render(request, 'accounts/profile.html')


def register(request):
    """
    Registration page.
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


def edit_profile(request):
    """
    Edit profile page.
    """
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('profile')

    form = EditProfileForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})
