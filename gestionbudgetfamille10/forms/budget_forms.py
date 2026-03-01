from django import forms
from ..models import Budget, Famille

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['Mois', 'Annee', 'MontantPrevu', 'idFamille']
        widgets = {
            'Mois': forms.Select(attrs={'class': 'form-control'}),
            'Annee': forms.NumberInput(attrs={'class': 'form-control', 'min': '2020', 'max': '2030'}),
            'MontantPrevu': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'idFamille': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'Mois': 'Mois',
            'Annee': 'Année',
            'MontantPrevu': 'Montant prévu (€)',
            'idFamille': 'Famille',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['idFamille'].queryset = Famille.objects.all()
        self.fields['idFamille'].empty_label = "Sélectionnez une famille"
        
    def clean(self):
        cleaned_data = super().clean()
        mois = cleaned_data.get('Mois')
        annee = cleaned_data.get('Annee')
        famille = cleaned_data.get('idFamille')
        
        # Vérification qu'il n'y a pas déjà un budget pour ce mois/année/famille
        if mois and annee and famille:
            if Budget.objects.filter(Mois=mois, Annee=annee, idFamille=famille).exists():
                if not self.instance.pk:  # Si c'est une création (pas une modification)
                    raise forms.ValidationError(
                        f"Un budget existe déjà pour {famille.NomFamille} en {mois}/{annee}"
                    )
        return cleaned_data