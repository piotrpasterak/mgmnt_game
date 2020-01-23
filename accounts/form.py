from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class UserCreateForm(UserCreationForm):
    _GENDER = (
        ('U', 'Nie deklaruje'),
        ('M', 'Meżczyzna'),
        ('F', 'Kobieta'),
    )

    _EXPERIENCE = (
        (0, 'Żadne'),
        (1, 'Mniej niz 1 rok'),
        (2, 'Mniej niz 2 lata'),
        (3, 'Mniej niz 3 lata'),
        (4, 'Wiecej niz 3 lata'),
    )

    email = forms.EmailField(required= True,  help_text='Wymagane. Podaj poprawny email.', label="Email")
    gender = forms.ChoiceField(help_text='Opcjonalne. Wybierz z listy.', choices= _GENDER, widget=forms.Select, label="Płeć")
    experience = forms.ChoiceField(help_text='Optional. Wybierz z listy.', choices=_EXPERIENCE, widget=forms.Select, label="Doświadczenie zawodowe")

    class Meta:
        model = User
        fields = ('username', 'email', 'gender', 'experience', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.gender = self.cleaned_data["gender"]
        user.experience = self.cleaned_data["experience"]

        if commit:
            user.save()
        return user
