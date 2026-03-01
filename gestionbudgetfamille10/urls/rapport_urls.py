from django.urls import path
from ..views import rapport_views

urlpatterns = [
    path('', rapport_views.generer_rapport, name='generer_rapport'),
    path('annuel/<int:annee>/', rapport_views.rapport_annuel, name='rapport_annuel'),
]