from django.db import models
from .famille import Famille

class Membre(models.Model):
    ROLE_CHOICES = [
        ('parent', 'Parent'),
        ('enfant', 'Enfant'),
        ('autre', 'Autre'),
    ]
    
    idMembre = models.AutoField(primary_key=True)
    Nom = models.CharField(max_length=50)
    Prenom = models.CharField(max_length=50)
    Role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='enfant')
    idFamille = models.ForeignKey(Famille, on_delete=models.CASCADE, related_name='membres')
    
    def __str__(self):
        return f"{self.Prenom} {self.Nom}"
    
    class Meta:
        verbose_name = "Membre"
        verbose_name_plural = "Membres"