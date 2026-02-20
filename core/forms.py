from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.validators import RegexValidator
from .db_guards import table_has_column

from .models import Country, PersonalActor, PersonalMovie

User = get_user_model()


class CountryChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj: Country) -> str:
        return f'{obj.flag_emoji} {obj.name}'


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
    country = CountryChoiceField(queryset=Country.objects.none(), to_field_name='name')

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
        if table_has_column(Country._meta.db_table, 'iso_code'):
            self.fields['country'].queryset = Country.objects.all()
        else:
            self.fields['country'].queryset = Country.objects.none()
        self.fields['country'].widget.attrs['list'] = 'movie-country-options'


class PersonalActorForm(PosterValidationMixin, forms.ModelForm):
    country = CountryChoiceField(queryset=Country.objects.none(), to_field_name='name')
    class Meta:
        model = PersonalActor
        fields = ['full_name', 'production_year', 'country', 'poster_image', 'score']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full actor name'}),
            'production_year': forms.NumberInput(attrs={'placeholder': 'Production year'}),
            'country': forms.TextInput(attrs={'class': 'country-select', 'autocomplete': 'off', 'placeholder': 'Type country name'}),
            'poster_image': forms.ClearableFileInput(attrs={'accept': '.png,.jpg,.jpeg'}),
            'score': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '100', 'placeholder': '0 - 100'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if table_has_column(Country._meta.db_table, 'iso_code'):
            self.fields['country'].queryset = Country.objects.all()
        else:
            self.fields['country'].queryset = Country.objects.none()
        self.fields['country'].widget.attrs['list'] = 'actor-country-options'