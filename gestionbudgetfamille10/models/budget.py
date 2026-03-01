from django.db import models
from .famille import Famille

class Budget(models.Model):
    MOIS_CHOICES = [
        (1, 'Janvier'), (2, 'Février'), (3, 'Mars'), (4, 'Avril'),
        (5, 'Mai'), (6, 'Juin'), (7, 'Juillet'), (8, 'Août'),
        (9, 'Septembre'), (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre')
    ]
    
    idBudget = models.AutoField(primary_key=True)
    Mois = models.IntegerField(choices=MOIS_CHOICES)
    Annee = models.IntegerField()
    MontantPrevu = models.DecimalField(max_digits=10, decimal_places=2)
    idFamille = models.ForeignKey(Famille, on_delete=models.CASCADE, related_name='budgets')
    
    def __str__(self):
        return f"{self.get_Mois_display()} {self.Annee} - {self.MontantPrevu}CFA"
    
    class Meta:
        verbose_name = "Budget"
        verbose_name_plural = "Budgets"
        unique_together = ['Mois', 'Annee', 'idFamille']  # Un seul budget par mois/année/famille