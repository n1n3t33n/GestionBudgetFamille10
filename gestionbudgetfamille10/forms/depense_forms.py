from django import forms
from ..models import Depense, Membre, CategorieDepense, ModePaiement

class DepenseForm(forms.ModelForm):
    class Meta:
        model = Depense
        fields = ['Montant', 'Date', 'idMembre', 'idCategorieDepense', 'idModePaiement']
        widgets = {
            'Montant': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'Date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'idMembre': forms.Select(attrs={'class': 'form-control'}),
            'idCategorieDepense': forms.Select(attrs={'class': 'form-control'}),
            'idModePaiement': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'Montant': 'Montant (€)',
            'Date': 'Date',
            'idMembre': 'Membre',
            'idCategorieDepense': 'Catégorie',
            'idModePaiement': 'Mode de paiement',
        }
    
    def __init__(self, *args, **kwargs):
        famille_id = kwargs.pop('famille_id', None)
        super().__init__(*args, **kwargs)
        
        if famille_id:
            self.fields['idMembre'].queryset = Membre.objects.filter(idFamille_id=famille_id)
        else:
            self.fields['idMembre'].queryset = Membre.objects.all()
            
        self.fields['idCategorieDepense'].queryset = CategorieDepense.objects.all()
        self.fields['idModePaiement'].queryset = ModePaiement.objects.all()
        
        self.fields['idMembre'].empty_label = "Sélectionnez un membre"
        self.fields['idCategorieDepense'].empty_label = "Sélectionnez une catégorie"
        self.fields['idModePaiement'].empty_label = "Sélectionnez un mode de paiement"