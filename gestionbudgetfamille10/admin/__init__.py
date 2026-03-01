from django.contrib import admin
from ..models import *
from ..forms import *

class MembreAdmin(admin.ModelAdmin):
    form = MembreForm
    list_display = ['Prenom', 'Nom', 'Role', 'idFamille']
    list_filter = ['Role', 'idFamille']
    search_fields = ['Nom', 'Prenom']

class RevenuAdmin(admin.ModelAdmin):
    form = RevenuForm
    list_display = ['Montant', 'Date', 'idMembre', 'idTypeRevenu']
    list_filter = ['Date', 'idTypeRevenu', 'idMembre']
    date_hierarchy = 'Date'

class DepenseAdmin(admin.ModelAdmin):
    form = DepenseForm
    list_display = ['Montant', 'Date', 'idMembre', 'idCategorieDepense', 'idModePaiement']
    list_filter = ['Date', 'idCategorieDepense', 'idModePaiement', 'idMembre']
    date_hierarchy = 'Date'

class BudgetAdmin(admin.ModelAdmin):
    form = BudgetForm
    list_display = ['idFamille', 'get_Mois_display', 'Annee', 'MontantPrevu']
    list_filter = ['idFamille', 'Mois', 'Annee']

# Enregistrement avec les classes personnalisées
admin.site.register(Famille)
admin.site.register(Membre, MembreAdmin)
admin.site.register(TypeRevenu)
admin.site.register(Revenu, RevenuAdmin)
admin.site.register(CategorieDepense)
admin.site.register(ModePaiement)
admin.site.register(Depense, DepenseAdmin)
admin.site.register(Budget, BudgetAdmin)