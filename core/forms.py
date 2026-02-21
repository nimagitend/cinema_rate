from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.core.validators import RegexValidator

import string
from datetime import date
from decimal import Decimal

from .models import Country, PersonalActor, PersonalMovie, UserProfile

User = get_user_model()

def _next_available_iso_code() -> str:
    letters = string.ascii_uppercase
    used_codes = set(Country.objects.values_list('iso_code', flat=True))
    for first in letters:
        for second in letters:
            code = f'{first}{second}'
            if code not in used_codes:
                return code
    return 'ZZ'


def _resolve_or_create_country(raw_value: str) -> Country:
    value = raw_value.strip()
    if not value:
        value = 'Unknown'

    existing = Country.objects.filter(name__iexact=value).first()
    if existing:
        return existing

    iso_code = _next_available_iso_code()
    return Country.objects.create(name=value, iso_code=iso_code)

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(
        max_length=150,
        validators=[RegexValidator(r'^[a-zA-Z0-9_]+$', 'Username must use English letters, numbers, or underscore.')],
        help_text='Use only English letters, numbers, and underscore.',
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter your email', 'autocomplete': 'email'})
        self.fields['username'].widget.attrs.update({'placeholder': 'Choose a username', 'autocomplete': 'username'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Create a password', 'autocomplete': 'new-password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm your password', 'autocomplete': 'new-password'})

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username or email', 'autocomplete': 'username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password', 'autocomplete': 'current-password'})

    def clean_username(self):
        value = self.cleaned_data['username'].strip()
        return value

class ProfileInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your email', 'autocomplete': 'email'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email is already registered.')
        return email


class ProfileAvatarForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar',)
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'accept': '.png,.jpg,.jpeg,.webp'})
        }

class ProfilePasswordForm(PasswordChangeForm):
    pass


class PersonalMovieForm(forms.ModelForm):
    country = forms.CharField(required=False)

    class Meta:
        model = PersonalMovie
        fields = ['title', 'production_year', 'country', 'poster_image', 'score']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Full movie title'}),
            'production_year': forms.NumberInput(attrs={'placeholder': 'Production year'}),
            'country': forms.TextInput(attrs={'class': 'country-select', 'autocomplete': 'off', 'placeholder': 'Type country name'}),
            'poster_image': forms.ClearableFileInput(attrs={'accept': '.png,.jpg,.jpeg'}),
            'score': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '100', 'placeholder': '0 - 100'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['title', 'production_year', 'poster_image', 'score']:
            self.fields[field_name].required = False

    def clean_title(self):
        return self.cleaned_data.get('title') or 'Untitled movie'

    def clean_production_year(self):
        return self.cleaned_data.get('production_year') or date.today().year

    def clean_score(self):
        return self.cleaned_data.get('score') or Decimal('0')

    def clean_country(self):
        value = self.data.get(self.add_prefix('country'), '')
        return _resolve_or_create_country(value)


class PersonalActorForm(forms.ModelForm):
    full_name = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'placeholder': 'Full name'}))
    born = forms.IntegerField(min_value=1900, required=False, widget=forms.NumberInput(attrs={'placeholder': 'Birth year (Gregorian)'}))
    country = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'country-select', 'autocomplete': 'off', 'placeholder': 'Type country name'}))
    class Meta:
        model = PersonalActor
        fields = ['full_name', 'born', 'country', 'poster_image', 'score']
        labels = {'born': 'Born'}
        widgets = {
            'poster_image': forms.ClearableFileInput(attrs={'accept': '.png,.jpg,.jpeg'}),
            'score': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '100', 'placeholder': '0 - 100'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['poster_image', 'score']:
            self.fields[field_name].required = False

    def clean_full_name(self):
        return self.cleaned_data.get('full_name') or 'Unknown actor'

    def clean_born(self):
        return self.cleaned_data.get('born') or date.today().year

    def clean_score(self):
        return self.cleaned_data.get('score') or Decimal('0')

    def clean_country(self):
        value = self.data.get(self.add_prefix('country'), '')
        return _resolve_or_create_country(value)

    def save(self, commit=True):
        actor = super().save(commit=False)
        actor.full_name = self.cleaned_data.get('full_name', '').strip()
        actor.production_year = self.cleaned_data.get('born')
        if commit:
            actor.save()
        return actor