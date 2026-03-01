from django.db import models

class Famille(models.Model):
    idFamille = models.AutoField(primary_key=True)
    NomFamille = models.CharField(max_length=100)
    NombreMembres = models.IntegerField(default=1)
    
    def __str__(self):
        return self.NomFamille
    
    class Meta:
        verbose_name = "Famille"
        verbose_name_plural = "Familles"