from django import forms
from ..models import Famille

class FamilleForm(forms.ModelForm):
    class Meta:
        model = Famille
        fields = ['NomFamille', 'NombreMembres']
        widgets = {
            'NomFamille': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la famille'}),
            'NombreMembres': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
        labels = {
            'NomFamille': 'Nom de la famille',
            'NombreMembres': 'Nombre de membres',
        }