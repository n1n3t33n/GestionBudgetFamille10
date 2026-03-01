from django.urls import path
from ..views import budget_views

urlpatterns = [
    path('', budget_views.liste_budgets, name='liste_budgets'),
    path('ajouter/', budget_views.ajouter_budget, name='ajouter_budget'),
    path('<int:pk>/', budget_views.detail_budget, name='detail_budget'),
    path('<int:pk>/modifier/', budget_views.modifier_budget, name='modifier_budget'),
    path('<int:pk>/supprimer/', budget_views.supprimer_budget, name='supprimer_budget'),
]