from django.urls import path
from ..views import accueil_views

urlpatterns = [
    path('', accueil_views.accueil, name='accueil'),
    path('dashboard/', accueil_views.dashboard, name='dashboard'),
    path('alertes/', accueil_views.alertes, name='alertes'),
    path('import-excel/', accueil_views.import_excel, name='import_excel'),
    path('export-excel/<str:modele>/', accueil_views.export_excel, name='export_excel'),
]