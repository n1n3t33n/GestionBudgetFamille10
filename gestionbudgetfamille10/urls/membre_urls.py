from django.urls import path
from ..views import membre_views

urlpatterns = [
    path('', membre_views.liste_membres, name='liste_membres'),
    path('ajouter/', membre_views.ajouter_membre, name='ajouter_membre'),
    path('<int:pk>/modifier/', membre_views.modifier_membre, name='modifier_membre'),
    path('<int:pk>/supprimer/', membre_views.supprimer_membre, name='supprimer_membre'),
]