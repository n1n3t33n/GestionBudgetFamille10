from django.core.management.base import BaseCommand
from gestionbudgetfamille10.models import TypeRevenu, CategorieDepense, ModePaiement

class Command(BaseCommand):
    help = 'Initialise les données de base'

    def handle(self, *args, **kwargs):
        # Types de revenus
        types_revenus = ['Salaire', 'Cadeau', 'Autre']
        for nom in types_revenus:
            TypeRevenu.objects.get_or_create(NomType=nom)
        
        # Catégories de dépenses
        categories = ['Alimentation', 'Logement', 'Transport', 'Loisirs', 'Santé', 'Éducation', 'Autre']
        for nom in categories:
            CategorieDepense.objects.get_or_create(NomCategorie=nom)
        
        # Modes de paiement
        modes = ['Espèces', 'Carte bancaire', 'Chèque', 'Virement', 'Autre']
        for nom in modes:
            ModePaiement.objects.get_or_create(NomMode=nom)
        
        self.stdout.write(self.style.SUCCESS('Données initialisées avec succès !'))