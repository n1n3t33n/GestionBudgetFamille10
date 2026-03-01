from django.urls import path
from ..views import statistiques_views

urlpatterns = [
    path('', statistiques_views.statistiques, name='statistiques'),
    path('par-categorie/', statistiques_views.statistiques_par_categorie, name='statistiques_par_categorie'),
]