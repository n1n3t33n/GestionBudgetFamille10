from django import forms
from ..models import Membre, Famille

class MembreForm(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ['Nom', 'Prenom', 'Role', 'idFamille']
        widgets = {
            'Nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'Prenom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'Role': forms.Select(attrs={'class': 'form-control'}),
            'idFamille': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'Nom': 'Nom',
            'Prenom': 'Prénom',
            'Role': 'Rôle',
            'idFamille': 'Famille',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pour n'afficher que les familles qui existent
        self.fields['idFamille'].queryset = Famille.objects.all()
        self.fields['idFamille'].empty_label = "Sélectionnez une famille"