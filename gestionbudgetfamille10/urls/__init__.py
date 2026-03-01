from django.urls import include, path

urlpatterns = [
    path('', include('gestionbudgetfamille10.urls.accueil_urls')),
    path('familles/', include('gestionbudgetfamille10.urls.famille_urls')),
    path('membres/', include('gestionbudgetfamille10.urls.membre_urls')),
    path('revenus/', include('gestionbudgetfamille10.urls.revenu_urls')),
    path('depenses/', include('gestionbudgetfamille10.urls.depense_urls')),
    path('budgets/', include('gestionbudgetfamille10.urls.budget_urls')),
    path('rapports/', include('gestionbudgetfamille10.urls.rapport_urls')),
    path('statistiques/', include('gestionbudgetfamille10.urls.statistiques_urls')),
]