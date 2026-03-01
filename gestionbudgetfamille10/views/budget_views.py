from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from ..models import Budget, Famille, Depense
from ..forms import BudgetForm

def liste_budgets(request):
    """Liste de tous les budgets"""
    famille_id = request.GET.get('famille')
    if famille_id:
        budgets = Budget.objects.filter(idFamille_id=famille_id).order_by('-Annee', '-Mois')
    else:
        budgets = Budget.objects.all().order_by('-Annee', '-Mois')
    
    familles = Famille.objects.all()
    
    # Calculer les dépenses réelles pour chaque budget
    for budget in budgets:
        depenses = Depense.objects.filter(
            Date__month=budget.Mois,
            Date__year=budget.Annee,
            idMembre__idFamille=budget.idFamille
        ).aggregate(total=Sum('Montant'))['total'] or 0
        budget.depenses_reelles = depenses
        budget.difference = budget.MontantPrevu - depenses
        budget.pourcentage = (depenses / budget.MontantPrevu * 100) if budget.MontantPrevu > 0 else 0
    
    return render(request, 'gestionbudgetfamille10/budget/liste.html', {
        'budgets': budgets,
        'familles': familles
    })

def ajouter_budget(request):
    """Ajouter un nouveau budget"""
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Budget créé avec succès !")
            return redirect('liste_budgets')
    else:
        # Pré-remplir avec le mois et l'année courants
        from datetime import datetime
        initial = {
            'Mois': datetime.now().month,
            'Annee': datetime.now().year
        }
        form = BudgetForm(initial=initial)
    
    return render(request, 'gestionbudgetfamille10/budget/form.html', {
        'form': form,
        'titre': 'Créer un budget'
    })

def modifier_budget(request, pk):
    """Modifier un budget"""
    budget = get_object_or_404(Budget, idBudget=pk)
    
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, "Budget modifié avec succès !")
            return redirect('liste_budgets')
    else:
        form = BudgetForm(instance=budget)
    
    return render(request, 'gestionbudgetfamille10/budget/form.html', {
        'form': form,
        'titre': 'Modifier le budget',
        'budget': budget
    })

def supprimer_budget(request, pk):
    """Supprimer un budget"""
    budget = get_object_or_404(Budget, idBudget=pk)
    
    if request.method == 'POST':
        budget.delete()
        messages.success(request, "Budget supprimé avec succès !")
        return redirect('liste_budgets')
    
    return render(request, 'gestionbudgetfamille10/budget/supprimer.html', {'budget': budget})

def detail_budget(request, pk):
    """Détail d'un budget avec analyse"""
    budget = get_object_or_404(Budget, idBudget=pk)
    
    # Récupérer toutes les dépenses du mois
    depenses = Depense.objects.filter(
        Date__month=budget.Mois,
        Date__year=budget.Annee,
        idMembre__idFamille=budget.idFamille
    ).select_related('idCategorieDepense', 'idMembre')
    
    # Statistiques par catégorie
    depenses_par_categorie = depenses.values(
        'idCategorieDepense__NomCategorie'
    ).annotate(
        total=Sum('Montant')
    ).order_by('-total')
    
    # Statistiques par membre
    depenses_par_membre = depenses.values(
        'idMembre__Prenom',
        'idMembre__Nom'
    ).annotate(
        total=Sum('Montant')
    ).order_by('-total')
    
    total_depenses = depenses.aggregate(total=Sum('Montant'))['total'] or 0
    
    context = {
        'budget': budget,
        'depenses': depenses,
        'total_depenses': total_depenses,
        'reste': budget.MontantPrevu - total_depenses,
        'depenses_par_categorie': depenses_par_categorie,
        'depenses_par_membre': depenses_par_membre,
        'pourcentage': (total_depenses / budget.MontantPrevu * 100) if budget.MontantPrevu > 0 else 0
    }
    
    return render(request, 'gestionbudgetfamille10/budget/detail.html', context)