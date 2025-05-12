from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    remember_me = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError(
                    'Invalid credentials',
                    code='invalid_credentials'
                )
            cleaned_data['user'] = user
        return cleaned_data


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True, min_length=8)
    password_confirm = forms.CharField(widget=forms.PasswordInput, required=True, label='Confirm Password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already taken.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError(
                {'password_confirm': 'Passwords do not match.'}
            )
        return cleaned_data


class EmailChangeForm(forms.Form):
    email = forms.EmailField(required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already taken.')
        return email


class ProfileSettingsForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)


class UsernameChangeForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username
