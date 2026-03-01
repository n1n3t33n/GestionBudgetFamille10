from django.shortcuts import render
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from ..models import Famille, Revenu, Depense, TypeRevenu, CategorieDepense, ModePaiement

def statistiques(request):
    """Page principale des statistiques"""
    famille = Famille.objects.first()
    if not famille:
        return redirect('ajouter_famille')
    
    # Périodes d'analyse
    aujourdhui = timezone.now().date()
    debut_mois = aujourdhui.replace(day=1)
    debut_annee = aujourdhui.replace(month=1, day=1)
    
    # 1. STATISTIQUES DU MOIS EN COURS
    revenus_mois = Revenu.objects.filter(
        Date__month=aujourdhui.month,
        Date__year=aujourdhui.year,
        idMembre__idFamille=famille
    )
    
    depenses_mois = Depense.objects.filter(
        Date__month=aujourdhui.month,
        Date__year=aujourdhui.year,
        idMembre__idFamille=famille
    )
    
    total_revenus_mois = revenus_mois.aggregate(total=Sum('Montant'))['total'] or 0
    total_depenses_mois = depenses_mois.aggregate(total=Sum('Montant'))['total'] or 0
    
    # 2. STATISTIQUES DE L'ANNÉE
    revenus_annee = Revenu.objects.filter(
        Date__year=aujourdhui.year,
        idMembre__idFamille=famille
    )
    
    depenses_annee = Depense.objects.filter(
        Date__year=aujourdhui.year,
        idMembre__idFamille=famille
    )
    
    # 3. RÉPARTITION DES REVENUS PAR TYPE
    revenus_par_type = TypeRevenu.objects.annotate(
        total=Sum('revenu__Montant', 
                 filter=models.Q(revenu__idMembre__idFamille=famille,
                               revenu__Date__year=aujourdhui.year))
    ).values('NomType', 'total')
    
    # 4. RÉPARTITION DES DÉPENSES PAR CATÉGORIE
    depenses_par_categorie = CategorieDepense.objects.annotate(
        total=Sum('depense__Montant',
                 filter=models.Q(depense__idMembre__idFamille=famille,
                               depense__Date__year=aujourdhui.year)),
        nombre=Count('depense')
    ).values('NomCategorie', 'total', 'nombre').order_by('-total')
    
    # 5. DÉPENSES PAR MODE DE PAIEMENT
    depenses_par_mode = ModePaiement.objects.annotate(
        total=Sum('depense__Montant',
                 filter=models.Q(depense__idMembre__idFamille=famille,
                               depense__Date__year=aujourdhui.year))
    ).values('NomMode', 'total')
    
    # 6. ÉVOLUTION MENSUELLE (12 derniers mois)
    evolution_mensuelle = []
    for i in range(11, -1, -1):
        date = aujourdhui - timedelta(days=30*i)
        mois = date.month
        annee = date.year
        
        rev = Revenu.objects.filter(
            Date__month=mois,
            Date__year=annee,
            idMembre__idFamille=famille
        ).aggregate(total=Sum('Montant'))['total'] or 0
        
        dep = Depense.objects.filter(
            Date__month=mois,
            Date__year=annee,
            idMembre__idFamille=famille
        ).aggregate(total=Sum('Montant'))['total'] or 0
        
        evolution_mensuelle.append({
            'mois': date.strftime('%B %Y'),
            'revenus': float(rev),
            'depenses': float(dep),
            'solde': float(rev - dep)
        })
    
    # 7. TOP DÉPENSES
    top_depenses = Depense.objects.filter(
        idMembre__idFamille=famille
    ).select_related(
        'idCategorieDepense', 'idMembre'
    ).order_by('-Montant')[:10]
    
    # 8. STATISTIQUES PAR MEMBRE
    stats_par_membre = []
    for membre in famille.membres.all():
        rev_membre = Revenu.objects.filter(
            idMembre=membre,
            Date__year=aujourdhui.year
        ).aggregate(total=Sum('Montant'))['total'] or 0
        
        dep_membre = Depense.objects.filter(
            idMembre=membre,
            Date__year=aujourdhui.year
        ).aggregate(total=Sum('Montant'))['total'] or 0
        
        stats_par_membre.append({
            'membre': membre,
            'revenus': rev_membre,
            'depenses': dep_membre,
            'solde': rev_membre - dep_membre
        })
    
    context = {
        'famille': famille,
        'mois_courant': aujourdhui.strftime('%B %Y'),
        'annee_courante': aujourdhui.year,
        
        # Résumés
        'total_revenus_mois': total_revenus_mois,
        'total_depenses_mois': total_depenses_mois,
        'solde_mois': total_revenus_mois - total_depenses_mois,
        'total_revenus_annee': revenus_annee.aggregate(total=Sum('Montant'))['total'] or 0,
        'total_depenses_annee': depenses_annee.aggregate(total=Sum('Montant'))['total'] or 0,
        
        # Répartitions
        'revenus_par_type': revenus_par_type,
        'depenses_par_categorie': depenses_par_categorie,
        'depenses_par_mode': depenses_par_mode,
        
        # Évolutions
        'evolution_mensuelle': evolution_mensuelle,
        'top_depenses': top_depenses,
        'stats_par_membre': stats_par_membre,
        
        # Moyennes
        'moyenne_depense_mois': total_depenses_mois / 30 if total_depenses_mois > 0 else 0,
        'nombre_depenses_mois': depenses_mois.count(),
    }
    
    return render(request, 'gestionbudgetfamille10/statistiques/index.html', context)

def statistiques_par_categorie(request):
    """Statistiques détaillées par catégorie"""
    famille = Famille.objects.first()
    if not famille:
        return redirect('ajouter_famille')
    
    # Analyse par catégorie sur l'année
    categories = CategorieDepense.objects.all()
    donnees_categories = []
    
    for categorie in categories:
        depenses = Depense.objects.filter(
            idCategorieDepense=categorie,
            idMembre__idFamille=famille,
            Date__year=timezone.now().year
        )
        
        total = depenses.aggregate(total=Sum('Montant'))['total'] or 0
        nombre = depenses.count()
        moyenne = total / nombre if nombre > 0 else 0
        
        # Évolution mensuelle pour cette catégorie
        evolution = []
        for mois in range(1, 13):
            montant = depenses.filter(Date__month=mois).aggregate(
                total=Sum('Montant')
            )['total'] or 0
            evolution.append(montant)
        
        donnees_categories.append({
            'categorie': categorie,
            'total': total,
            'nombre': nombre,
            'moyenne': moyenne,
            'evolution': evolution
        })
    
    return render(request, 'gestionbudgetfamille10/statistiques/par_categorie.html', {
        'donnees_categories': donnees_categories
    })