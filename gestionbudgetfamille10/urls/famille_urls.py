from django.urls import path
from ..views import famille_views

urlpatterns = [
    path('', famille_views.liste_familles, name='liste_familles'),
    path('ajouter/', famille_views.ajouter_famille, name='ajouter_famille'),
    path('<int:pk>/', famille_views.detail_famille, name='detail_famille'),
    path('<int:pk>/modifier/', famille_views.modifier_famille, name='modifier_famille'),
    path('<int:pk>/supprimer/', famille_views.supprimer_famille, name='supprimer_famille'),
]