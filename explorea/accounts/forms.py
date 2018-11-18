from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UserModel


class RegisterForm(UserCreationForm):
    """
    Registration form derived from UserCreationForm.
    """
    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        ]


class EditProfileForm(UserChangeForm):
    """
    Change form derived from UserChangeForm.
    """
    class Meta:
        model = UserModel
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
        ]
