from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.validators import RegexValidator

from .models import Country, PersonalActor, PersonalMovie
import string

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


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username or email', 'autocomplete': 'username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password', 'autocomplete': 'current-password'})

    def clean_username(self):
        value = self.cleaned_data['username'].strip()
        return value


class PosterValidationMixin:
    def clean(self):
        cleaned_data = super().clean()
        poster_image = cleaned_data.get('poster_image')
        if not poster_image:
            raise forms.ValidationError('Please upload a JPG/PNG image.')
        return cleaned_data


class PersonalMovieForm(PosterValidationMixin, forms.ModelForm):
    country = forms.CharField()

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

    def clean_country(self):
        value = self.data.get(self.add_prefix('country'), '')
        return _resolve_or_create_country(value)


class PersonalActorForm(PosterValidationMixin, forms.ModelForm):
    first_name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'country-select', 'autocomplete': 'off', 'placeholder': 'Type country name'}))
    class Meta:
        model = PersonalActor
        fields = ['country', 'poster_image', 'score']
        labels = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full name'}),
            'production_year': forms.NumberInput(attrs={'placeholder': 'Birth year (Gregorian)'}),
        }
        widgets = {
            'poster_image': forms.ClearableFileInput(attrs={'accept': '.png,.jpg,.jpeg'}),
            'score': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '100', 'placeholder': '0 - 100'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = 'First name'
        self.fields['last_name'].label = 'Last name'
        self.order_fields(['first_name', 'last_name', 'country', 'poster_image', 'score'])

    def clean_country(self):
        value = self.data.get(self.add_prefix('country'), '')
        return _resolve_or_create_country(value)

    def save(self, commit=True):
        actor = super().save(commit=False)
        first_name = self.cleaned_data.get('first_name', '').strip()
        last_name = self.cleaned_data.get('last_name', '').strip()
        actor.full_name = f'{first_name} {last_name}'.strip()
        actor.production_year = 0
        if commit:
            actor.save()
        return actor