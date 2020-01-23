from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class UserCreateForm(UserCreationForm):
    _GENDER = (
        ('U', 'Prefer not to say'),
        ('M', 'Male'),
        ('F', 'Female'),
    )

    _EXPERIENCE = (
        (0, 'None'),
        (1, 'Less than 1 year'),
        (2, 'Less than 2 year'),
        (3, 'Less than 3 year'),
        (4, 'More than 3 year'),
    )

    email = forms.EmailField(required= True,  help_text='Required. Please enter correct email.' )
    gender = forms.ChoiceField(help_text='Optional. Please choose from list.', choices= _GENDER, widget=forms.Select)
    experience = forms.ChoiceField(help_text='Optional. Please choose from list.', choices=_EXPERIENCE, widget=forms.Select)

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
