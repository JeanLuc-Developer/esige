from django.urls import path
from apps.core.views.dash import home
from apps.core.views.annuaires import annuaire
from apps.core.views.etablissement import etablissement
from apps.core.views.parametre import parametre


urlpatterns = [

    
    #Annuaire URLs
    path('annuaires/classe/', annuaire.annuaire_table_classe, name='annuaire_classe'),
    path('annuaires/ecole/', annuaire.annuaire_table_ecole, name='annuaire_ecole'),
    path('annuaires/eleve/', annuaire.annuaire_table_eleve, name='annuaire_eleve'),
    path('annuaires/enseignant/', annuaire.annuaire_table_enseignant, name='annuaire_enseignant'),
    path('forms_annuaire/', annuaire.annuaire_form, name='forms_annuaire'),

    #Etablissement URLs
    path('etablissements/', etablissement.tablissement_table, name='etablissement'),
    path('forms_etablissement/', etablissement.etablissement_form, name='forms_etablissement'),

    #Parametre URLs
    path('parametres/', parametre.parametre_table, name='parametre'),
    path('forms_paremetre/', parametre.parametre_form, name='forms_parametre'),
    

    path('dash/', home.accueil, name='dash'),
    ]