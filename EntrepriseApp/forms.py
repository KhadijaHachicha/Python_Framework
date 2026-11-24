from django import forms
from .models import Entreprise, Utilisateur
from django.contrib.auth.forms import UserCreationForm


class EntrepriseForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        fields = '__all__'


class RegisterUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Utilisateur
        fields = UserCreationForm.Meta.fields + (
            'first_name',
            'last_name',
            'email',
            'role',
            'telephone',
        )
