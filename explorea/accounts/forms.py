from django import forms
from django.contrib.auth import get_user_model


class RegisterForm(forms.ModelForm):
    """
    Registration form derived from registration model.
    """
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label='Password confirmation',
        strip=False,
        widget=forms.PasswordInput,
        help_text='Enter the same password as before, for verification.'
    )

    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]
