from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from datetime import datetime
from ..models import Revenu, Membre, TypeRevenu
from ..forms import RevenuForm, RechercheForm

def liste_revenus(request):
    """Liste des revenus avec filtres"""
    form = RechercheForm(request.GET or None)
    revenus = Revenu.objects.all().select_related('idMembre', 'idTypeRevenu')
    
    if form.is_valid():
        if form.cleaned_data['date_debut']:
            revenus = revenus.filter(Date__gte=form.cleaned_data['date_debut'])
        if form.cleaned_data['date_fin']:
            revenus = revenus.filter(Date__lte=form.cleaned_data['date_fin'])
        if form.cleaned_data['mois']:
            revenus = revenus.filter(Date__month=form.cleaned_data['mois'])
        if form.cleaned_data['annee']:
            revenus = revenus.filter(Date__year=form.cleaned_data['annee'])
    
    # Statistiques
    total = revenus.aggregate(total=Sum('Montant'))['total'] or 0
    par_type = revenus.values('idTypeRevenu__NomType').annotate(total=Sum('Montant'))
    
    return render(request, 'gestionbudgetfamille10/revenu/liste.html', {
        'revenus': revenus.order_by('-Date'),
        'form': form,
        'total': total,
        'par_type': par_type
    })

def ajouter_revenu(request):
    """Ajouter un nouveau revenu"""
    famille_id = request.GET.get('famille')
    
    if request.method == 'POST':
        form = RevenuForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Revenu ajouté avec succès !")
            return redirect('liste_revenus')
    else:
        form = RevenuForm(famille_id=famille_id)
    
    return render(request, 'gestionbudgetfamille10/revenu/form.html', {
        'form': form,
        'titre': 'Ajouter un revenu'
    })

def modifier_revenu(request, pk):
    """Modifier un revenu"""
    revenu = get_object_or_404(Revenu, idRevenu=pk)
    
    if request.method == 'POST':
        form = RevenuForm(request.POST, instance=revenu, famille_id=revenu.idMembre.idFamille.idFamille)
        if form.is_valid():
            form.save()
            messages.success(request, "Revenu modifié avec succès !")
            return redirect('liste_revenus')
    else:
        form = RevenuForm(instance=revenu, famille_id=revenu.idMembre.idFamille.idFamille)
    
    return render(request, 'gestionbudgetfamille10/revenu/form.html', {
        'form': form,
        'titre': 'Modifier le revenu',
        'revenu': revenu
    })

def supprimer_revenu(request, pk):
    """Supprimer un revenu"""
    revenu = get_object_or_404(Revenu, idRevenu=pk)
    
    if request.method == 'POST':
        revenu.delete()
        messages.success(request, "Revenu supprimé avec succès !")
        return redirect('liste_revenus')
    
    return render(request, 'gestionbudgetfamille10/revenu/supprimer.html', {'revenu': revenu})