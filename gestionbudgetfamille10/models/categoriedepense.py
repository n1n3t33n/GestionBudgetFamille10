from django.db import models

class CategorieDepense(models.Model):
    idCategorieDepense = models.AutoField(primary_key=True)
    NomCategorie = models.CharField(max_length=50)
    
    def __str__(self):
        return self.NomCategorie
    
    class Meta:
        verbose_name = "Catégorie de dépense"
        verbose_name_plural = "Catégories de dépense"