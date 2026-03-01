from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Membre, Famille
from ..forms import MembreForm

def liste_membres(request):
    """Liste de tous les membres"""
    famille_id = request.GET.get('famille')
    if famille_id:
        membres = Membre.objects.filter(idFamille_id=famille_id)
    else:
        membres = Membre.objects.all()
    
    familles = Famille.objects.all()
    return render(request, 'gestionbudgetfamille10/membre/liste.html', {
        'membres': membres,
        'familles': familles
    })

def ajouter_membre(request):
    """Ajouter un nouveau membre"""
    if request.method == 'POST':
        form = MembreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Membre ajouté avec succès !")
            return redirect('liste_membres')
    else:
        # Pré-sélectionner une famille si spécifiée dans l'URL
        famille_id = request.GET.get('famille')
        initial = {}
        if famille_id:
            initial['idFamille'] = famille_id
        form = MembreForm(initial=initial)
    
    return render(request, 'gestionbudgetfamille10/membre/form.html', {
        'form': form,
        'titre': 'Ajouter un membre'
    })

def modifier_membre(request, pk):
    """Modifier un membre"""
    membre = get_object_or_404(Membre, idMembre=pk)
    
    if request.method == 'POST':
        form = MembreForm(request.POST, instance=membre)
        if form.is_valid():
            form.save()
            messages.success(request, f"Membre {membre.Prenom} {membre.Nom} modifié avec succès !")
            return redirect('detail_famille', pk=membre.idFamille.idFamille)
    else:
        form = MembreForm(instance=membre)
    
    return render(request, 'gestionbudgetfamille10/membre/form.html', {
        'form': form,
        'titre': 'Modifier le membre',
        'membre': membre
    })

def supprimer_membre(request, pk):
    """Supprimer un membre"""
    membre = get_object_or_404(Membre, idMembre=pk)
    famille_id = membre.idFamille.idFamille
    
    if request.method == 'POST':
        membre.delete()
        messages.success(request, "Membre supprimé avec succès !")
        return redirect('detail_famille', pk=famille_id)
    
    return render(request, 'gestionbudgetfamille10/membre/supprimer.html', {'membre': membre})