from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *

# Configuration Jazzmin personnalisée
JAZZMIN_SETTINGS = {
    "site_title": "Administration Scolaire",
    "site_header": "Système d'Information Scolaire",
    "site_brand": "Admin Scolaire",
    "welcome_sign": "Bienvenue dans l'administration scolaire",
    "copyright": "Système Scolaire",
    "search_model": ["auth.User", "Etablissement"],
    
    "topmenu_links": [
        {"name": "Accueil", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"model": "auth.User"},
        {"app": "your_app_name"},
    ],
    
    "usermenu_links": [
        {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
    ],
    
    "show_sidebar": True,
    "navigation_expanded": True,
    
    "hide_apps": [],
    "hide_models": [],
    
    "order_with_respect_to": ["auth", "Annee_scolaire", "Etablissement", "Formulaires"],
    
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "Annee_scolaire": "fas fa-calendar-alt",
        "Etablissement": "fas fa-school",
        "Formulaires": "fas fa-file-alt",
        "Identifications": "fas fa-id-card",
        "Informations_generale": "fas fa-info-circle",
        "Proveds": "fas fa-building",
        "Provinces": "fas fa-map-marker-alt",
        "Regimes_gestion": "fas fa-cogs",
        "Sous_proved": "fas fa-building",
        "Territoires": "fas fa-globe",
    },
    
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

# Admin classes pour chaque modèle

@admin.register(Annee_scolaire)
class AnneeScolaireAdmin(admin.ModelAdmin):
    list_display = ('id', 'lib_annee_scolaire', 'active', 'generate', 'open', 'valid')
    list_filter = ('active', 'generate', 'open', 'valid')
    search_fields = ('lib_annee_scolaire',)
    list_editable = ('active', 'generate', 'open', 'valid')
    list_per_page = 20

@admin.register(Etablissement)
class EtablissementAdmin(admin.ModelAdmin):
    list_display = ('nomEtablissement', 'anneeId', 'type_enseignement', 'isActive', 'isDeleted')
    list_filter = ('anneeId', 'type_enseignement', 'isActive', 'isDeleted', 'createdAt')
    search_fields = ('nomEtablissement', 'nom_norm', 'adresseEtablissement')
    readonly_fields = ('createdAt',)
    list_per_page = 25
    date_hierarchy = 'createdAt'

@admin.register(Formulaires)
class FormulairesAdmin(admin.ModelAdmin):
    list_display = ('id', 'nomEtab', 'etablissement_id', 'idAnnee', 'responded', 'validated', 'created_at')
    list_filter = ('responded', 'validated', 'type', 'idAnnee', 'created_at')
    search_fields = ('nomEtab', 'nom_norm')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 30
    date_hierarchy = 'created_at'

@admin.register(Identifications)
class IdentificationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'denomination', 'fk_annee_id', 'download', 'finished', 'submit')
    list_filter = ('download', 'finished', 'submit', 'fk_annee_id', 'milieu')
    search_fields = ('denomination', 'nom_chef_etab', 'adresse', 'num_secope')
    readonly_fields = ('updated_at',)
    list_per_page = 25

@admin.register(Informations_generale)
class InformationsGeneraleAdmin(admin.ModelAdmin):
    list_display = ('id', 'identification_id', 'cloture', 'coges', 'internet')
    list_filter = ('cloture', 'coges', 'internet', 'point_eau')
    search_fields = ('nom_second_etablissement', 'organisme_projet')
    list_per_page = 20

@admin.register(Proveds)
class ProvedsAdmin(admin.ModelAdmin):
    list_display = ('id', 'libelle', 'fk_province_id', 'slug')
    list_filter = ('fk_province_id',)
    search_fields = ('libelle', 'slug')
    readonly_fields = ('createdAt',)
    list_per_page = 20

@admin.register(Provinces)
class ProvincesAdmin(admin.ModelAdmin):
    list_display = ('id', 'libelle', 'chef_lieu', 'is_deleted', 'created_at')
    list_filter = ('is_deleted', 'created_at')
    search_fields = ('libelle', 'chef_lieu', 'slug')
    readonly_fields = ('created_at',)
    list_per_page = 20

@admin.register(Regimes_gestion)
class RegimesGestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'description', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('code', 'description')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20

@admin.register(Sous_proved)
class SousProvedAdmin(admin.ModelAdmin):
    list_display = ('id', 'libelle', 'fk_proved_id', 'fk_territoire_id', 'lieu_implantation')
    list_filter = ('fk_proved_id', 'fk_territoire_id')
    search_fields = ('libelle', 'slug', 'lieu_implantation')
    readonly_fields = ('created_at',)
    list_per_page = 20

@admin.register(Territoires)
class TerritoiresAdmin(admin.ModelAdmin):
    list_display = ('id', 'libelle', 'fk_province_id', 'fk_proved_id')
    list_filter = ('fk_province_id', 'fk_proved_id')
    search_fields = ('libelle', 'slug')
    readonly_fields = ('createdAt',)
    list_per_page = 20

# Classes admin pour les modèles ST1
@admin.register(St1_effectifs_par_age)
class St1EffectifsParAgeAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id')
    list_per_page = 20

@admin.register(St1_enseignant)
class St1EnseignantAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id', 'personnel_eligible_retraite')
    list_per_page = 20

@admin.register(St1_groupes_specifiques)
class St1GroupesSpecifiquesAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id')
    list_per_page = 20

@admin.register(St1_guides_educateurs)
class St1GuidesEducateursAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id')
    list_per_page = 20

@admin.register(St1_infrastuctures)
class St1InfrastructuresAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id')
    list_per_page = 20

@admin.register(St1_locaux)
class St1LocauxAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id')
    list_per_page = 20

@admin.register(St1_manuels_enfants)
class St1ManuelsEnfantsAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id')
    list_per_page = 20

@admin.register(St1_personnel_administratif)
class St1PersonnelAdministratifAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id')
    list_per_page = 20

# Classes admin pour les modèles ST2
@admin.register(St2_classes_autorisees_et_organisees)
class St2ClassesAutoriseesOrganiseesAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id')
    list_per_page = 20

@admin.register(St2_effectifs_eleve_ciquieme)
class St2EffectifsEleveCinquiemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id')
    list_per_page = 20

@admin.register(St2_effectifs_eleve_deuxieme)
class St2EffectifsEleveDeuxiemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id')
    list_per_page = 20

@admin.register(St2_effectifs_eleve_premiere)
class St2EffectifsElevePremiereAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id')
    list_per_page = 20

@admin.register(St2_effectifs_eleves_preprimaire)
class St2EffectifsElevesPreprimaireAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id')
    list_per_page = 20

@admin.register(St2_effectifs_eleve_quatrieme)
class St2EffectifsEleveQuatriemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id')
    list_per_page = 20

@admin.register(St2_effectifs_eleve_sixieme)
class St2EffectifsEleveSixiemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id')
    list_per_page = 20

@admin.register(St2_effectifs_eleve_troisieme)
class St2EffectifsEleveTroisiemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id')
    list_per_page = 20

@admin.register(St2_environnement_et_developpement)
class St2EnvironnementDeveloppementAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id', 'st2_activites_parascolaires', 'st2_gouvernement_eleves')
    list_per_page = 20

@admin.register(St2_equipements_ateliers_ou_laboratoires)
class St2EquipementsAteliersLabosAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id', 'st2_NomEquipement', 'st2_TypeAtelierOuLabo')
    list_per_page = 20

@admin.register(St2_etat_des_locaux)
class St2EtatDesLocauxAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id')
    list_per_page = 20

@admin.register(St2_etat_des_locaux_specifiques)
class St2EtatDesLocauxSpecifiquesAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id')
    list_per_page = 20

@admin.register(St2_guides_pedagogiques_disponibles)
class St2GuidesPedagogiquesDisponiblesAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id')
    list_per_page = 20

@admin.register(St2_manuels_disponibles)
class St2ManuelsDisponiblesAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id')
    list_per_page = 20

@admin.register(St2_personnel_administratif_et_ouvrier)
class St2PersonnelAdministratifOuvrierAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id')
    list_per_page = 20

@admin.register(St2_repartition_et_affectations)
class St2RepartitionAffectationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id', 'niveau')
    list_per_page = 20

@admin.register(St2_repartition_enseignants_et_eligibles)
class St2RepartitionEnseignantsEligiblesAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id', 'nb_enseignants_eligibles_retraite')
    list_per_page = 20

@admin.register(St2_repartition_releve)
class St2RepartitionReleveAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id')
    list_per_page = 20

@admin.register(St2_resultat_enaf_epsante)
class St2ResultatEnafEpsanteAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id', 'st2_taux_abandon', 'st2_taux_reussite_enafep')
    list_per_page = 20

# Classes admin pour les modèles ST3
@admin.register(St3_disponible_programme_national)
class St3DisponibleProgrammeNationalAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id', 'NomDuFiliere', 'TypeDeProgrammeNational')
    list_per_page = 20

@admin.register(St3_documentation)
class St3DocumentationAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id', 'st3_manuel_procedure', 'st3_plan_communication')
    list_per_page = 20

@admin.register(St3_dual_input_section)
class St3DualInputSectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id', 'st3_enseignants_formes_genre', 'st3_femmes_enseignantes_recrutees')
    list_per_page = 20

@admin.register(St3_effectif_eleve_inscrit_sexe_annee_etude_age_revolu)
class St3EffectifsEleveInscritAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id')
    list_per_page = 20

@admin.register(Effectif_eleve_type_enseignement)
class EffectifEleveTypeEnseignementAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id')
    list_per_page = 20

@admin.register(St3_personnel_administratif_fonction_sexe)
class St3PersonnelAdministratifFonctionSexeAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id')
    list_per_page = 20

@admin.register(St3_effectif_par_age_sexe)
class St3EffectifParAgeSexeAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id')
    list_per_page = 20

@admin.register(St3_effectif_par_categorie_particuliere)
class St3EffectifParCategorieParticuliereAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id')
    list_per_page = 20

@admin.register(St3_eleve)
class St3EleveAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id', 'Nom', 'Sexe', 'Filiere')
    search_fields = ('Nom', 'Filiere')
    list_per_page = 20

@admin.register(St3_enregistrement_equipement)
class St3EnregistrementEquipementAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id', 'NomEquipement', 'TypeAtelierOuLabo')
    list_per_page = 20

@admin.register(St3_equipement_existant)
class St3EquipementExistantAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id', 'NomEquipement')
    list_per_page = 20

@admin.register(St3_formation)
class St3FormationAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id', 'st3_enseignants_formes_genre')
    list_per_page = 20

@admin.register(St3_infrastructure_activites)
class St3InfrastructureActivitesAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id', 'st3_activites_parascolaires', 'st3_gouvernement_eleves')
    list_per_page = 20

@admin.register(St3_manuel_disponible_niveau)
class St3ManuelDisponibleNiveauAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id')
    list_per_page = 20

@admin.register(St3_nombre_locaux_caracteristique_etat_mur)
class St3NombreLocauxCaracteristiqueEtatMurAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id')
    list_per_page = 20

@admin.register(St3_nombre_locaux_caracteristique_etat_nature_toilette)
class St3NombreLocauxCaracteristiqueEtatNatureToiletteAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id')
    list_per_page = 20

@admin.register(St3_note_section)
class St3NoteSectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id', 'st3_note')
    list_per_page = 20

@admin.register(St3_personnel_enseignant)
class St3PersonnelEnseignantAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id', 'chef_formation', 'educateurs_formes')
    list_per_page = 20

@admin.register(St3_personnel_enseignant_sexe_qualification)
class St3PersonnelEnseignantSexeQualificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id', 'st3_NombreEnseignantARetraite', 'st3_NombreEnseignantNonPaye')
    list_per_page = 20

@admin.register(St3_repartition_temps_formation)
class St3RepartitionTempsFormationAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id', 'NomFiliere', 'NombreHeureFormationTheorique')
    list_per_page = 20

@admin.register(St3_reseaux_environnement)
class St3ReseauxEnvironnementAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id', 'st3_chef_participe_rld', 'st3_participation_rep')
    list_per_page = 20

@admin.register(St3_resultat_examen_etat)
class St3ResultatExamenEtatAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id', 'NomDuFiliere', 'ElevesInscritsF', 'ElevesInscritsG')
    list_per_page = 20

@admin.register(St3_resultat_jury_national)
class St3ResultatJuryNationalAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_st_id', 'NomFiliere', 'NombreReussitesF', 'NombreReussitesG')
    list_per_page = 20

# Désenregistrer le modèle Group si vous ne voulez pas le voir dans l'admin
# admin.site.unregister(Group)