from django import forms

class RechercheForm(forms.Form):
    date_debut = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Date début'
    )
    date_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Date fin'
    )
    
    mois = forms.ChoiceField(
        choices=[('', 'Tous')] + [(i, f'Mois {i}') for i in range(1, 13)],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Mois'
    )
    
    annee = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '2020', 'max': '2030'}),
        label='Année'
    )