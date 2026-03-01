from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from ..models import Depense, Membre, CategorieDepense, ModePaiement
from ..forms import DepenseForm, RechercheForm

def liste_depenses(request):
    """Liste des dépenses avec filtres"""
    form = RechercheForm(request.GET or None)
    depenses = Depense.objects.all().select_related('idMembre', 'idCategorieDepense', 'idModePaiement')
    
    if form.is_valid():
        if form.cleaned_data['date_debut']:
            depenses = depenses.filter(Date__gte=form.cleaned_data['date_debut'])
        if form.cleaned_data['date_fin']:
            depenses = depenses.filter(Date__lte=form.cleaned_data['date_fin'])
        if form.cleaned_data['mois']:
            depenses = depenses.filter(Date__month=form.cleaned_data['mois'])
        if form.cleaned_data['annee']:
            depenses = depenses.filter(Date__year=form.cleaned_data['annee'])
    
    # Statistiques
    total = depenses.aggregate(total=Sum('Montant'))['total'] or 0
    par_categorie = depenses.values('idCategorieDepense__NomCategorie').annotate(total=Sum('Montant'))
    par_mode = depenses.values('idModePaiement__NomMode').annotate(total=Sum('Montant'))
    
    return render(request, 'gestionbudgetfamille10/depense/liste.html', {
        'depenses': depenses.order_by('-Date'),
        'form': form,
        'total': total,
        'par_categorie': par_categorie,
        'par_mode': par_mode
    })

def ajouter_depense(request):
    """Ajouter une nouvelle dépense"""
    famille_id = request.GET.get('famille')
    
    if request.method == 'POST':
        form = DepenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Dépense ajoutée avec succès !")
            return redirect('liste_depenses')
    else:
        form = DepenseForm(famille_id=famille_id)
    
    return render(request, 'gestionbudgetfamille10/depense/form.html', {
        'form': form,
        'titre': 'Ajouter une dépense'
    })

def modifier_depense(request, pk):
    """Modifier une dépense"""
    depense = get_object_or_404(Depense, idDepense=pk)
    
    if request.method == 'POST':
        form = DepenseForm(request.POST, instance=depense, famille_id=depense.idMembre.idFamille.idFamille)
        if form.is_valid():
            form.save()
            messages.success(request, "Dépense modifiée avec succès !")
            return redirect('liste_depenses')
    else:
        form = DepenseForm(instance=depense, famille_id=depense.idMembre.idFamille.idFamille)
    
    return render(request, 'gestionbudgetfamille10/depense/form.html', {
        'form': form,
        'titre': 'Modifier la dépense',
        'depense': depense
    })

def supprimer_depense(request, pk):
    """Supprimer une dépense"""
    depense = get_object_or_404(Depense, idDepense=pk)
    
    if request.method == 'POST':
        depense.delete()
        messages.success(request, "Dépense supprimée avec succès !")
        return redirect('liste_depenses')
    
    return render(request, 'gestionbudgetfamille10/depense/supprimer.html', {'depense': depense})