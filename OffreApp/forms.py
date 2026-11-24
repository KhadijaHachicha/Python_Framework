from django import forms
from .models import Offre


class OffreForm(forms.ModelForm):
    class Meta:
        model = Offre
        fields = '__all__'
        widgets = {
            'date_proposition': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={'type': 'datetime-local'},
            ),
        }
