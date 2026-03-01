from django import forms
from ..models import Revenu, Membre, TypeRevenu

class RevenuForm(forms.ModelForm):
    class Meta:
        model = Revenu
        fields = ['Montant', 'Date', 'idMembre', 'idTypeRevenu']
        widgets = {
            'Montant': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'Date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'idMembre': forms.Select(attrs={'class': 'form-control'}),
            'idTypeRevenu': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'Montant': 'Montant (€)',
            'Date': 'Date',
            'idMembre': 'Membre',
            'idTypeRevenu': 'Type de revenu',
        }
    
    def __init__(self, *args, **kwargs):
        # Permet de filtrer les membres par famille si besoin
        famille_id = kwargs.pop('famille_id', None)
        super().__init__(*args, **kwargs)
        
        if famille_id:
            self.fields['idMembre'].queryset = Membre.objects.filter(idFamille_id=famille_id)
        else:
            self.fields['idMembre'].queryset = Membre.objects.all()
            
        self.fields['idTypeRevenu'].queryset = TypeRevenu.objects.all()
        self.fields['idMembre'].empty_label = "Sélectionnez un membre"
        self.fields['idTypeRevenu'].empty_label = "Sélectionnez un type"