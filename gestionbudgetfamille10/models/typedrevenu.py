from django.db import models

class TypeRevenu(models.Model):
    idTypeRevenu = models.AutoField(primary_key=True)
    NomType = models.CharField(max_length=50)
    
    def __str__(self):
        return self.NomType
    
    class Meta:
        verbose_name = "Type de revenu"
        verbose_name_plural = "Types de revenu"