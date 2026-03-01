from django.urls import path
from ..views import revenu_views

urlpatterns = [
    path('', revenu_views.liste_revenus, name='liste_revenus'),
    path('ajouter/', revenu_views.ajouter_revenu, name='ajouter_revenu'),
    path('<int:pk>/modifier/', revenu_views.modifier_revenu, name='modifier_revenu'),
    path('<int:pk>/supprimer/', revenu_views.supprimer_revenu, name='supprimer_revenu'),
]