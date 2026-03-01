from django.urls import path
from .views import *

urlpatterns = [
    # Accueil
    path('', accueil_views.accueil, name='accueil'),
    path('dashboard/', accueil_views.dashboard, name='dashboard'),
    
    # Familles
    path('familles/', famille_views.liste_familles, name='liste_familles'),
    path('familles/ajouter/', famille_views.ajouter_famille, name='ajouter_famille'),
    path('familles/<int:pk>/', famille_views.detail_famille, name='detail_famille'),
    path('familles/<int:pk>/modifier/', famille_views.modifier_famille, name='modifier_famille'),
    path('familles/<int:pk>/supprimer/', famille_views.supprimer_famille, name='supprimer_famille'),
    
    # Membres
    path('membres/', membre_views.liste_membres, name='liste_membres'),
    path('membres/ajouter/', membre_views.ajouter_membre, name='ajouter_membre'),
    path('membres/<int:pk>/modifier/', membre_views.modifier_membre, name='modifier_membre'),
    path('membres/<int:pk>/supprimer/', membre_views.supprimer_membre, name='supprimer_membre'),
    
    # Revenus
    path('revenus/', revenu_views.liste_revenus, name='liste_revenus'),
    path('revenus/ajouter/', revenu_views.ajouter_revenu, name='ajouter_revenu'),
    path('revenus/<int:pk>/modifier/', revenu_views.modifier_revenu, name='modifier_revenu'),
    path('revenus/<int:pk>/supprimer/', revenu_views.supprimer_revenu, name='supprimer_revenu'),
    
    # Dépenses
    path('depenses/', depense_views.liste_depenses, name='liste_depenses'),
    path('depenses/ajouter/', depense_views.ajouter_depense, name='ajouter_depense'),
    path('depenses/<int:pk>/modifier/', depense_views.modifier_depense, name='modifier_depense'),
    path('depenses/<int:pk>/supprimer/', depense_views.supprimer_depense, name='supprimer_depense'),
    
    # Budgets
    path('budgets/', budget_views.liste_budgets, name='liste_budgets'),
    path('budgets/ajouter/', budget_views.ajouter_budget, name='ajouter_budget'),
    path('budgets/<int:pk>/modifier/', budget_views.modifier_budget, name='modifier_budget'),
    path('budgets/<int:pk>/supprimer/', budget_views.supprimer_budget, name='supprimer_budget'),
    
    # Rapports et statistiques
    path('rapports/', rapport_views.generer_rapport, name='generer_rapport'),
    path('statistiques/', statistiques_views.statistiques, name='statistiques'),
    
    # Alertes
    path('alertes/', accueil_views.alertes, name='alertes'),
    
    # Import/Export
    path('import-excel/', accueil_views.import_excel, name='import_excel'),
    path('export-excel/<str:modele>/', accueil_views.export_excel, name='export_excel'),
]