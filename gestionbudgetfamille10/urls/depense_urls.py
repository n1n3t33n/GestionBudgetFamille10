from django.urls import path
from ..views import depense_views

urlpatterns = [
    path('', depense_views.liste_depenses, name='liste_depenses'),
    path('ajouter/', depense_views.ajouter_depense, name='ajouter_depense'),
    path('<int:pk>/modifier/', depense_views.modifier_depense, name='modifier_depense'),
    path('<int:pk>/supprimer/', depense_views.supprimer_depense, name='supprimer_depense'),
]