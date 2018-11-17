from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login

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
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            password = form.cleaned_data.get('password1')

            User = get_user_model()
            user = User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            user.set_password(password)
            user.save()

            auth_user = authenticate(username=username, password=password)
            login(request, auth_user)

            return redirect('profile')

    return render(request, 'accounts/register.html', {'form': RegisterForm()})
