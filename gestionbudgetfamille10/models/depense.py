from django.db import models
from .membre import Membre
from .categoriedepense import CategorieDepense
from .modepaiement import ModePaiement

class Depense(models.Model):
    idDepense = models.AutoField(primary_key=True)
    Montant = models.DecimalField(max_digits=10, decimal_places=2)
    Date = models.DateField()
    idMembre = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='depenses')
    idCategorieDepense = models.ForeignKey(CategorieDepense, on_delete=models.CASCADE)
    idModePaiement = models.ForeignKey(ModePaiement, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.Montant}CFA - {self.Date}"
    
    class Meta:
        verbose_name = "Dépense"
        verbose_name_plural = "Dépenses"