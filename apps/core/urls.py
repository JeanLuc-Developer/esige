from django.urls import path
from apps.core.views.dash import home
from apps.core.views.annuaires import annuaire
from apps.core.views.etablissement import etablissement
from apps.core.views.parametre import parametre


urlpatterns = [

    
    #Annuaire URLs
    path('annuaires/classe/', annuaire.annuaire_table_classe, name='annuaire_classe'),
    path('annuaires/ecole/', annuaire.annuaire_ecoles, name='annuaire_ecole'),
    path('annuaires/eleve/', annuaire.annuaire_table_eleve, name='annuaire_eleve'),
    path('annuaires/enseignant/', annuaire.annuaire_table_enseignant, name='annuaire_enseignant'),
    path('annuaires/api/table-data/', annuaire.get_table_data, name='get_table_data'),
    path('annuaires/export/excel/', annuaire.export_excel, name='export_excel'),
    path('annuaires/export/pdf/', annuaire.export_pdf, name='export_pdf'),
    path('annuaires/export/csv/', annuaire.export_csv, name='export_csv'),

    path('commodites/', annuaire.annuaire_commodites, name='annuaire_commodites'),
    path('api/commodites/data/', annuaire.get_commodites_data, name='get_commodites_data'),
    path('export/commodites/excel/', annuaire.export_commodites_excel, name='export_commodites_excel'),
    path('export/commodites/pdf/', annuaire.export_commodites_pdf, name='export_commodites_pdf'),
    path('themes-transversaux/', annuaire.themes_transversaux, name='themes_transversaux'),
    path('get-themes-data/', annuaire.get_themes_data, name='get_themes_data'),
    path('export-themes-excel/', annuaire.export_themes_excel, name='export_themes_excel'),
    path('export-themes-pdf/', annuaire.export_themes_pdf, name='export_themes_pdf'),
    path('export-themes-csv/', annuaire.export_themes_csv, name='export_themes_csv'),
    path('salles-organisees/', annuaire.salles_organisees, name='salles_organisees'),
    path('get-salles-data/', annuaire.get_salles_data, name='get_salles_data'),
    path('export-salles-excel/', annuaire.export_salles_excel, name='export_salles_excel'),
    path('export-salles-pdf/', annuaire.export_salles_pdf, name='export_salles_pdf'),
    path('export-salles-csv/', annuaire.export_salles_csv, name='export_salles_csv'),

    path('effectifs-st1/', annuaire.effectifs_st1, name='effectifs_st1'),
    path('get-effectifs-data/', annuaire.get_effectifs_data, name='get_effectifs_data'),
    path('export-effectifs-excel/', annuaire.export_effectifs_excel, name='export_effectifs_excel'),
    path('export-effectifs-pdf/', annuaire.export_effectifs_pdf, name='export_effectifs_pdf'),
    path('export-effectifs-csv/', annuaire.export_effectifs_csv, name='export_effectifs_csv'),

    # Page principale des enseignants
    path('enseignants/', annuaire.annuaire_enseignants, name='annuaire_enseignants'),
    # Endpoint AJAX pour récupérer les données
    path('get_enseignants_data/', annuaire.get_enseignants_data, name='get_enseignants_data'),
    # Export des données
    path('export_enseignants_excel/', annuaire.export_enseignants_excel, name='export_enseignants_excel'),
    path('export_enseignants_pdf/', annuaire.export_enseignants_pdf, name='export_enseignants_pdf'),
    path('export_enseignants_csv/', annuaire.export_enseignants_csv, name='export_enseignants_csv'),
    

    path('guides-manuels/', annuaire.guides_manuels_view, name='guides_manuels'),
    
    # Endpoint AJAX pour récupérer les données des tableaux
    path('get-guides-manuels-data/', annuaire.get_guides_manuels_data, name='get_guides_manuels_data'),
    
    # Export des données
    path('export-guides-excel/', annuaire.export_guides_excel, name='export_guides_excel'),
    path('export-guides-pdf/', annuaire.export_guides_pdf, name='export_guides_pdf'),
    path('export-guides-csv/', annuaire.export_guides_csv, name='export_guides_csv'),

    path('get-table-data/', annuaire.get_table_data, name='get_table_data_ratio'),
    path('export-excel/', annuaire.export_excel, name='export_excel_ratio'),
    path('export-pdf/', annuaire.export_pdf, name='export_pdf'),
    #path('get-filter-options/', annuaire.get_filter_options, name='get_filter_options'),

    



    path('forms_annuaire/', annuaire.annuaire_form, name='forms_annuaire'),

    #Etablissement URLs
    path('etablissements/', etablissement.tablissement_table, name='etablissement'),
    path('forms_etablissement/', etablissement.etablissement_form, name='forms_etablissement'),
    path('etablissements/import/', etablissement.import_etablissements, name='import_etablissements'),
    path('etablissements/import/excel/', etablissement.import_excel, name='import_excel'),
    path('etablissements/import/csv/', etablissement.import_csv, name='import_csv'),
    #path('etablissements/import/template/excel/', etablissement.download_excel_template, name='download_excel_template'),
    #path('etablissements/import/template/csv/', etablissement.download_csv_template, name='download_csv_template'),

    #Parametre URLs
    path('parametres/', parametre.parametre_table, name='parametre'),
    path('forms_paremetre/', parametre.parametre_form, name='forms_parametre'),
    

    path('dash/', home.accueil, name='dash'),

    path('ecoles/', annuaire.annuaire_ecoles, name='annuaire_ecoles'),
    
    # Endpoint AJAX pour les données des tableaux
    path('get-table-data/', annuaire.get_table_data, name='get_table_data'),
    
    # URLs d'export
    path('export-excel/', annuaire.export_excel, name='export_excel'),
    path('export-pdf/', annuaire.export_pdf, name='export_pdf'),
    path('export-csv/', annuaire.export_csv, name='export_csv'),


    path('locaux/', annuaire.annuaire_locaux, name='annuaire_locaux'),
    path('api/locaux/data/', annuaire.get_locaux_data, name='get_locaux_data'),
    path('export/locaux/excel/', annuaire.export_locaux_excel, name='export_locaux_excel'),
    path('export/locaux/pdf/', annuaire.export_locaux_pdf, name='export_locaux_pdf'),
    path('export/locaux/csv/', annuaire.export_locaux_csv, name='export_locaux_csv'),

    path('gestion-ratios/', annuaire.gestion_ratios, name='gestion_ratios'),
    path('get-ratios-data/', annuaire.get_ratios_data, name='get_ratios_data'),


    ]