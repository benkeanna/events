from django import forms


class RegisterForm(forms.Form):

    username = forms.CharField(max_length=30, help_text='How will we call you?')
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
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
