from django.db import models

class ModePaiement(models.Model):
    idModePaiement = models.AutoField(primary_key=True)
    NomMode = models.CharField(max_length=50)
    
    def __str__(self):
        return self.NomMode
    
    class Meta:
        verbose_name = "Mode de paiement"
        verbose_name_plural = "Modes de paiement"