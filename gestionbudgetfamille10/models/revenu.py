from django.db import models
from .membre import Membre
from .typedrevenu import TypeRevenu

class Revenu(models.Model):
    idRevenu = models.AutoField(primary_key=True)
    Montant = models.DecimalField(max_digits=10, decimal_places=2)
    Date = models.DateField()
    idMembre = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='revenus')
    idTypeRevenu = models.ForeignKey(TypeRevenu, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.Montant}€ - {self.Date}"
    
    class Meta:
        verbose_name = "Revenu"
        verbose_name_plural = "Revenus"