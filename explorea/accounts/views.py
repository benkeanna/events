from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, update_session_auth_hash

from .forms import RegisterForm, EditUserForm, EditProfileForm


@login_required
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
		else:
			return render(request, 'accounts/register.html', {'form': form})

	return render(request, 'accounts/register.html', {'form': RegisterForm()})


@login_required
def edit_profile(request):
	user_form = EditUserForm(request.POST or None, instance=request.user)
	profile_form = EditProfileForm(request.POST or None, instance=request.user.profile)

	if request.method == 'POST':
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			profile = profile_form.save()

			return redirect('accounts:profile')

	return render(request, 'accounts/edit_profile.html',
		{'user_form': user_form, 'profile_form': profile_form})


@login_required
def change_password(request):
	"""
	Page for changing password.
	"""
	if request.method == 'POST':
		form = PasswordChangeForm(data=request.POST, user=request.user)

		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			return redirect('/accounts/profile/')
		else:
			return render(request, 'accounts/change_password.html',
			              {'form': form})

	form = PasswordChangeForm(user=request.user)
	return render(request, 'accounts/change_password.html', {'form': form})
