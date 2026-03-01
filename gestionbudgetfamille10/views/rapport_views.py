from django.shortcuts import render
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
from ..models import Famille, Revenu, Depense, Budget
from ..forms import RechercheForm

def generer_rapport(request):
    """Générer un rapport financier personnalisé"""
    famille = Famille.objects.first()
    if not famille:
        return render(request, 'gestionbudgetfamille10/rapport/erreur.html', {
            'message': 'Veuillez d\'abord créer une famille.'
        })
    
    form = RechercheForm(request.GET or None)
    
    # Période par défaut : 3 derniers mois
    date_fin = timezone.now().date()
    date_debut = date_fin - timedelta(days=90)
    
    revenus = Revenu.objects.filter(idMembre__idFamille=famille)
    depenses = Depense.objects.filter(idMembre__idFamille=famille)
    
    if form.is_valid():
        if form.cleaned_data['date_debut']:
            date_debut = form.cleaned_data['date_debut']
            revenus = revenus.filter(Date__gte=date_debut)
            depenses = depenses.filter(Date__gte=date_debut)
        if form.cleaned_data['date_fin']:
            date_fin = form.cleaned_data['date_fin']
            revenus = revenus.filter(Date__lte=date_fin)
            depenses = depenses.filter(Date__lte=date_fin)
    
    # Calculs principaux
    total_revenus = revenus.aggregate(total=Sum('Montant'))['total'] or 0
    total_depenses = depenses.aggregate(total=Sum('Montant'))['total'] or 0
    
    # Analyse par mois
    mois_analyse = []
    date_courante = date_debut
    while date_courante <= date_fin:
        mois = date_courante.month
        annee = date_courante.year
        
        rev_mois = revenus.filter(Date__month=mois, Date__year=annee).aggregate(
            total=Sum('Montant')
        )['total'] or 0
        
        dep_mois = depenses.filter(Date__month=mois, Date__year=annee).aggregate(
            total=Sum('Montant')
        )['total'] or 0
        
        # Récupérer le budget du mois s'il existe
        budget = Budget.objects.filter(
            Mois=mois,
            Annee=annee,
            idFamille=famille
        ).first()
        
        mois_analyse.append({
            'mois': mois,
            'annee': annee,
            'nom_mois': date_courante.strftime('%B %Y'),
            'revenus': rev_mois,
            'depenses': dep_mois,
            'solde': rev_mois - dep_mois,
            'budget': budget.MontantPrevu if budget else None,
            'respect_budget': (dep_mois <= budget.MontantPrevu) if budget else None
        })
        
        # Passer au mois suivant
        if date_courante.month == 12:
            date_courante = date_courante.replace(year=date_courante.year + 1, month=1)
        else:
            date_courante = date_courante.replace(month=date_courante.month + 1)
    
    # Top catégories de dépenses
    top_categories = depenses.values(
        'idCategorieDepense__NomCategorie'
    ).annotate(
        total=Sum('Montant'),
        nombre=Count('idDepense')
    ).order_by('-total')[:5]
    
    # Moyennes
    nombre_jours = (date_fin - date_debut).days + 1
    moyenne_journaliere = total_depenses / nombre_jours if nombre_jours > 0 else 0
    
    context = {
        'famille': famille,
        'form': form,
        'date_debut': date_debut,
        'date_fin': date_fin,
        'total_revenus': total_revenus,
        'total_depenses': total_depenses,
        'solde_periode': total_revenus - total_depenses,
        'mois_analyse': mois_analyse,
        'top_categories': top_categories,
        'moyenne_journaliere': moyenne_journaliere,
        'nombre_operations': revenus.count() + depenses.count(),
    }
    
    return render(request, 'gestionbudgetfamille10/rapport/generer.html', context)

def rapport_annuel(request, annee):
    """Rapport annuel détaillé"""
    famille = Famille.objects.first()
    if not famille:
        return redirect('ajouter_famille')
    
    # Données par mois
    donnees_mensuelles = []
    for mois in range(1, 13):
        revenus = Revenu.objects.filter(
            Date__month=mois,
            Date__year=annee,
            idMembre__idFamille=famille
        ).aggregate(total=Sum('Montant'))['total'] or 0
        
        depenses = Depense.objects.filter(
            Date__month=mois,
            Date__year=annee,
            idMembre__idFamille=famille
        ).aggregate(total=Sum('Montant'))['total'] or 0
        
        budget = Budget.objects.filter(
            Mois=mois,
            Annee=annee,
            idFamille=famille
        ).first()
        
        donnees_mensuelles.append({
            'mois': mois,
            'revenus': revenus,
            'depenses': depenses,
            'solde': revenus - depenses,
            'budget': budget.MontantPrevu if budget else None,
        })
    
    # Totaux annuels
    total_revenus = sum(d['revenus'] for d in donnees_mensuelles)
    total_depenses = sum(d['depenses'] for d in donnees_mensuelles)
    
    context = {
        'famille': famille,
        'annee': annee,
        'donnees_mensuelles': donnees_mensuelles,
        'total_revenus': total_revenus,
        'total_depenses': total_depenses,
        'solde_annuel': total_revenus - total_depenses,
    }
    
    return render(request, 'gestionbudgetfamille10/rapport/annuel.html', context)