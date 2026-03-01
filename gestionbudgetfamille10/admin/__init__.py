from django.contrib import admin
from ..models import *

# Enregistrement des modèles
admin.site.register(Famille)
admin.site.register(Membre)
admin.site.register(TypeRevenu)
admin.site.register(Revenu)
admin.site.register(CategorieDepense)
admin.site.register(ModePaiement)
admin.site.register(Depense)
admin.site.register(Budget)