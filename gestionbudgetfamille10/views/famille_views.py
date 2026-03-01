from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Famille
from ..forms import FamilleForm

def liste_familles(request):
    """Liste de toutes les familles"""
    familles = Famille.objects.all()
    return render(request, 'gestionbudgetfamille10/famille/liste.html', {'familles': familles})

def ajouter_famille(request):
    """Ajouter une nouvelle famille"""
    if request.method == 'POST':
        form = FamilleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Famille créée avec succès !")
            return redirect('liste_familles')
    else:
        form = FamilleForm()
    
    return render(request, 'gestionbudgetfamille10/famille/form.html', {
        'form': form,
        'titre': 'Ajouter une famille'
    })

def detail_famille(request, pk):
    """Détail d'une famille avec ses membres et budgets"""
    famille = get_object_or_404(Famille, idFamille=pk)
    membres = famille.membres.all()
    budgets = famille.budgets.all().order_by('-Annee', '-Mois')
    
    return render(request, 'gestionbudgetfamille10/famille/detail.html', {
        'famille': famille,
        'membres': membres,
        'budgets': budgets
    })

def modifier_famille(request, pk):
    """Modifier une famille"""
    famille = get_object_or_404(Famille, idFamille=pk)
    
    if request.method == 'POST':
        form = FamilleForm(request.POST, instance=famille)
        if form.is_valid():
            form.save()
            messages.success(request, "Famille modifiée avec succès !")
            return redirect('detail_famille', pk=pk)
    else:
        form = FamilleForm(instance=famille)
    
    return render(request, 'gestionbudgetfamille10/famille/form.html', {
        'form': form,
        'titre': 'Modifier la famille',
        'famille': famille
    })

def supprimer_famille(request, pk):
    """Supprimer une famille"""
    famille = get_object_or_404(Famille, idFamille=pk)
    
    if request.method == 'POST':
        famille.delete()
        messages.success(request, "Famille supprimée avec succès !")
        return redirect('liste_familles')
    
    return render(request, 'gestionbudgetfamille10/famille/supprimer.html', {'famille': famille})