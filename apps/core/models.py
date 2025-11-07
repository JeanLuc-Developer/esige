from django.db import models


class Annee_scolaire(models.Model):
    # La colonne 'id' est implicitement créée par Django comme clé primaire AutoField.

    # Colonne 'active' : Représente probablement un état actif (0 ou 1).
    active = models.BooleanField(
        default=False,
        verbose_name="Actif"
    )

    # Colonne 'generate' : Représente probablement un état booléen (1 pour générer, 0 sinon).
    generate = models.BooleanField(
        default=False,
        verbose_name="Générer"
    )

    # Colonne 'open' : Représente probablement un état d'ouverture (1 pour ouvert, 0 sinon).
    open = models.BooleanField(
        default=False,
        verbose_name="Ouvert"
    )

    # Colonne 'valid' : Représente probablement un état de validité (1 pour valide, 0 sinon).
    valid = models.BooleanField(
        default=False,
        verbose_name="Valide"
    )

    # Colonne 'lib_annee_scolaire' : Contient la description de l'année scolaire (ex: '2022-2023').
    lib_annee_scolaire = models.CharField(
        max_length=50,  # Une taille de 50 caractères est largement suffisante pour '2022-2023'
        verbose_name="Libellé Année Scolaire"
    )
    
    # Vous pouvez ajouter une méthode __str__ pour une meilleure représentation dans l'administration Django
    def __str__(self):
        return self.lib_annee_scolaire

    class Meta:
        # Met le nom de la table en minuscule et avec underscore
        verbose_name = "Année Scolaire"
        verbose_name_plural = "Années Scolaires"
        # Si vous voulez forcer le nom de la table dans la base de données à "annee_scolaire" (sans le préfixe de l'appli),
        # vous pouvez utiliser: db_table = 'annee_scolaire'

class Etablissement(models.Model):
   
    anneeId = models.ForeignKey(
        'Annee_scolaire', 
        on_delete=models.CASCADE,  # Ou models.PROTECT selon votre logique
        null=False, 
        verbose_name="Année ID"
    )

    # 3. nomEtablissement (varchar(255), Non)
    nomEtablissement = models.CharField(
        max_length=255, 
        null=False, 
        verbose_name="Nom de l'Établissement"
    )

    # 4. type_enseignement (varchar(50), Oui)
    type_enseignement = models.CharField(
        max_length=50, 
        null=True, 
        verbose_name="Type d'Enseignement"
    )

    # 5. NomChefEtablissement (varchar(255), Oui)
    NomChefEtablissement = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Nom du Chef d'Établissement"
    )

    # 6. adresseEtablissement (varchar(500), Oui)
    adresseEtablissement = models.CharField(
        max_length=500, 
        null=True, 
        verbose_name="Adresse de l'Établissement"
    )

    # 7. TelephoneEtablissement (varchar(50), Oui)
    TelephoneEtablissement = models.CharField(
        max_length=50, 
        null=True, 
        verbose_name="Téléphone de l'Établissement"
    )

    # 8-16. Clés étrangères (ID) vers d'autres tables (bigint(20)). On utilise des placeholders :

    # 8. provinceId (bigint(20), Non)
    provinceId = models.BigIntegerField(null=False, verbose_name="Province ID") # Utilisation de BigIntegerField pour bigint(20)

    # 9. provedId (bigint(20), Non)
    provedId = models.BigIntegerField(null=False, verbose_name="Proved ID")

    # 10. sousProvedId (bigint(20), Non)
    sousProvedId = models.BigIntegerField(null=False, verbose_name="Sous-Proved ID")

    # 11. informations_generale_id (bigint(20), Oui)
    informations_generale_id = models.BigIntegerField(null=True, verbose_name="Informations Générales ID")

    # 12. localisation_administrative_id (bigint(20), Oui)
    localisation_administrative_id = models.BigIntegerField(null=True, verbose_name="Localisation Administrative ID")

    # 13. localisation_scolaire_id (bigint(20), Oui)
    localisation_scolaire_id = models.BigIntegerField(null=True, verbose_name="Localisation Scolaire ID")

    # 14. territoireId (bigint(20), Oui)
    territoireId = models.BigIntegerField(null=True, verbose_name="Territoire ID")

    # 15. reference_juridique_id (bigint(20), Oui)
    reference_juridique_id = models.BigIntegerField(null=True, verbose_name="Référence Juridique ID")

    # 16. identification_id (bigint(20), Oui)
    identification_id = models.BigIntegerField(null=True, verbose_name="Identification ID")

    # 17. isActive (tinyint(1), Oui, Défaut: 1)
    # tinyint(1) est généralement converti en BooleanField en Django.
    isActive = models.BooleanField(
        default=True,  # Valeur par défaut 1
        verbose_name="Est Actif"
    )

    # 18. isDeleted (tinyint(1), Oui, Défaut: 0)
    isDeleted = models.BooleanField(
        default=False,  # Valeur par défaut 0
        verbose_name="Est Supprimé"
    )

    # 19. createdAt (timestamp, Oui, Défaut: current_timestamp())
    # Django utilise généralement DateTimeField pour les timestamps.
    # auto_now_add=True s'occupe de la valeur par défaut au moment de la création.
    createdAt = models.DateTimeField(
        auto_now_add=True, 
        null=True, 
        verbose_name="Date de Création"
    )

    # 20. nom_norm (varchar(255), Oui)
    nom_norm = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Nom Normalisé"
    )

    def __str__(self):
        return self.nomEtablissement

    class Meta:
        verbose_name = "Établissement"
        verbose_name_plural = "Établissements"
        # Si vous voulez que le nom de la table soit exactement 'Etablissement' (sans le préfixe de l'appli en minuscule)
        # vous devriez utiliser: db_table = 'Etablissement'

class Formulaires(models.Model):
    # 1. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django comme Primary Key (AutoField).

    # 2. updated_at (datetime(6), Non, Défaut: current_timestamp(6), Extra: ON UPDATE CURRENT_TIMESTAMP(6))
    updated_at = models.DateTimeField(
        auto_now=True,  # Met à jour automatiquement à chaque sauvegarde (correspond à ON UPDATE CURRENT_TIMESTAMP)
        null=False,
        verbose_name="Date de Dernière Mise à Jour"
    )

    # 3. responded (tinyint(1), Non, Défaut: 0)
    responded = models.BooleanField(
        default=False,  # 0 en tinyint(1) -> False en BooleanField
        null=False,
        verbose_name="A Répondu"
    )

    # 4. nomEtab (varchar(255), Oui)
    nomEtab = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Nom Établissement (Saisie)"
    )

    # 5. etablissement_id (bigint(20), Oui)
    # Supposé être une clé étrangère vers le modèle Etablissement
    etablissement_id = models.ForeignKey(
        'Etablissement', 
        on_delete=models.SET_NULL, # On choisit SET_NULL car null=True
        null=True, 
        verbose_name="ID Établissement (Lien)"
    )

    # 6. idannee (bigint(20), Oui)
    # Supposé être une clé étrangère vers le modèle Annee_scolaire
    idAnnee = models.ForeignKey(
        'Annee_scolaire', 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name="ID Année Scolaire"
    )

    # 7-9. IDs de localisation (bigint(20), Oui)
    # On utilise BigIntegerField car les modèles cibles ne sont pas encore définis.
    provinceId = models.BigIntegerField(null=True, verbose_name="Province ID")
    provedId = models.BigIntegerField(null=True, verbose_name="Proved ID")
    sousProvedId = models.BigIntegerField(null=True, verbose_name="Sous-Proved ID")

    # 10. type (varchar(255), Oui)
    type = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Type de Formulaire"
    )

    # 11. idUtilisateur (bigint(20), Oui)
    # Clé étrangère vers le modèle User de Django (ou un modèle personnalisé)
    idUtilisateur = models.BigIntegerField(null=True, verbose_name="ID Utilisateur")

    # 12. validated (tinyint(1), Non, Défaut: 0)
    validated = models.BooleanField(
        default=False, 
        null=False,
        verbose_name="Validé"
    )

    # 13. validatedBy (bigint(20), Oui)
    # ID de l'utilisateur qui a validé
    validatedBy = models.BigIntegerField(null=True, verbose_name="Validé Par ID")

    # 14. created_at (datetime(6), Non, Défaut: current_timestamp(6))
    created_at = models.DateTimeField(
        auto_now_add=True, # Ajoute la date/heure à la création de l'objet (correspond à current_timestamp)
        null=False, 
        verbose_name="Date de Création"
    )

    # 15. idetablissement (bigint(20), Oui)
    # Ce champ est un doublon potentiel de 'etablissement_id', je le garde mais notez le conflit.
    idEtablissement = models.BigIntegerField(null=True, verbose_name="ID Établissement (Duplicata)")

    # 16. date (varchar(255), Oui)
    # Utiliser CharField car le type est 'varchar' (si c'était une vraie date, on utiliserait DateField ou DateTimeField).
    date = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Champ Date"
    )
    
    # 17. identification_id (bigint(20), Oui)
    identification_id = models.BigIntegerField(null=True, verbose_name="Identification ID")

    # 18. nom_norm (varchar(255), Oui)
    nom_norm = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Nom Normalisé"
    )

    def __str__(self):
        # Une bonne chaîne de représentation
        return f"Formulaire pour {self.nomEtab or 'Inconnu'} ({self.id})"

    class Meta:
        verbose_name = "Formulaire"
        verbose_name_plural = "Formulaires"

class Identifications(models.Model):
    # 1. download (bit(1), Non, Défaut: 0)
    # bit(1) est généralement un BooleanField en Django.
    download = models.BooleanField(
        default=False, 
        verbose_name="Téléchargé"
    )

    # 2. finished (bit(1), Non)
    finished = models.BooleanField(
        default=False, 
        verbose_name="Terminé"
    )

    # 3. remplissage (int(11), Oui)
    # On utilise IntegerField pour int(11).
    remplissage = models.IntegerField(
        null=True, 
        verbose_name="Remplissage (%)"
    )

    # 4. submit (bit(1), Oui)
    submit = models.BooleanField(
        null=True, 
        verbose_name="Soumis"
    )

    # 5. fk_annee_id (bigint(20), Oui)
    # Clé étrangère vers Annee_scolaire
    fk_annee_id = models.ForeignKey(
        'Annee_scolaire', 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name="Année Scolaire ID"
    )

    # 6-11. Clés étrangères de localisation et autres (bigint(20), Oui)
    # On utilise BigIntegerField comme placeholder pour les FK qui seront probablement définies plus tard.
    fk_centre_reg_id = models.BigIntegerField(null=True, verbose_name="Centre Régional ID")
    fk_etab_id = models.BigIntegerField(null=True, verbose_name="Établissement ID")
    fk_proved_id = models.BigIntegerField(null=True, verbose_name="Proved ID")
    fk_province_id = models.BigIntegerField(null=True, verbose_name="Province ID")
    fk_territoire_id = models.BigIntegerField(null=True, verbose_name="Territoire ID")
    fk_ville_id = models.BigIntegerField(null=True, verbose_name="Ville ID")

    # 12. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 13. released_at (datetime(6), Oui)
    released_at = models.DateTimeField(
        null=True, 
        verbose_name="Date de Publication"
    )

    # 14. sous_proved_id (bigint(20), Oui)
    sous_proved_id = models.BigIntegerField(null=True, verbose_name="Sous-Proved ID")

    # 15. updated_at (datetime(6), Oui)
    updated_at = models.DateTimeField(
        auto_now=True,  # Met à jour à chaque sauvegarde
        null=True, 
        verbose_name="Date de Modification"
    )

    # 16. user_id (bigint(20), Oui)
    user_id = models.BigIntegerField(null=True, verbose_name="Utilisateur ID")

    # 17-33. Champs Varchar
    
    # 17. secteur_enseignement (varchar(150), Oui)
    secteur_enseignement = models.CharField(max_length=150, null=True, verbose_name="Secteur Enseignement")

    # 18. tel_chef_etab (varchar(150), Oui)
    tel_chef_etab = models.CharField(max_length=150, null=True, verbose_name="Téléphone Chef Établissement")

    # 19. adresse (varchar(191), Oui)
    adresse = models.CharField(max_length=191, null=True, verbose_name="Adresse")

    # 20. etab_est (varchar(191), Oui)
    etab_est = models.CharField(max_length=191, null=True, verbose_name="Établissement Est...")

    # 21. milieu (varchar(191), Oui)
    milieu = models.CharField(max_length=191, null=True, verbose_name="Milieu (Urbain/Rural)")

    # 22. nom_chef_etab (varchar(191), Oui)
    nom_chef_etab = models.CharField(max_length=191, null=True, verbose_name="Nom Chef Établissement")

    # 23. num_secope (varchar(191), Oui)
    num_secope = models.CharField(max_length=191, null=True, verbose_name="Numéro SECOPE")

    # 24. ref_juridique (varchar(191), Oui)
    ref_juridique = models.CharField(max_length=191, null=True, verbose_name="Référence Juridique")

    # 25. stat_occup_parcel (varchar(191), Oui)
    stat_occup_parcel = models.CharField(max_length=191, null=True, verbose_name="Statut Occupation Parcelle")

    # 26. center (varchar(255), Oui)
    center = models.CharField(max_length=255, null=True, verbose_name="Centre")

    # 27. code_centre_reg (varchar(255), Oui)
    code_centre_reg = models.CharField(max_length=255, null=True, verbose_name="Code Centre Régional")

    # 28. denomination (varchar(255), Oui)
    denomination = models.CharField(max_length=255, null=True, verbose_name="Dénomination")

    # 29. latitude (varchar(255), Oui)
    latitude = models.CharField(max_length=255, null=True, verbose_name="Latitude")

    # 30. longitude (varchar(255), Oui)
    longitude = models.CharField(max_length=255, null=True, verbose_name="Longitude")

    # 31. regime_gestion (varchar(255), Oui)
    regime_gestion = models.CharField(max_length=255, null=True, verbose_name="Régime de Gestion")

    # 32. slug (varchar(255), Oui)
    slug = models.CharField(max_length=255, null=True, verbose_name="Slug")

    # 33. type_enseignement (varchar(255), Oui)
    type_enseignement = models.CharField(max_length=255, null=True, verbose_name="Type d'Enseignement")


    def __str__(self):
        return f"Identification {self.id} - {self.denomination or 'Sans nom'}"

    class Meta:
        verbose_name = "Identification"
        verbose_name_plural = "Identifications"

class Informations_generale(models.Model):
    # 1. form_et_id (bigint(20), Oui)
    # Supposé être une clé étrangère vers le modèle Etablissement (via Formulaires ou Identifications)
    form_et_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire Établissement ID"
    )
    
    # 2. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 3. identification_id (bigint(20), Oui)
    # Clé étrangère vers le modèle Identifications
    identification_id = models.ForeignKey(
        'Identifications', 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name="Identification ID"
    )

    # 4. cloture (varchar(255), Oui)
    cloture = models.CharField(max_length=255, null=True, verbose_name="Clôture")

    # 5. coges (varchar(255), Oui)
    coges = models.CharField(max_length=255, null=True, verbose_name="CoGES")

    # 6. coges_operationnel (varchar(255), Oui)
    coges_operationnel = models.CharField(max_length=255, null=True, verbose_name="CoGES Opérationnel")

    # 7. compartiments_filles (varchar(255), Oui)
    compartiments_filles = models.CharField(max_length=255, null=True, verbose_name="Compartiments Filles")

    # 8. copa (varchar(255), Oui)
    copa = models.CharField(max_length=255, null=True, verbose_name="COPA")

    # 9. copa_operationnel (varchar(255), Oui)
    copa_operationnel = models.CharField(max_length=255, null=True, verbose_name="COPA Opérationnel")

    # 10. cour_recreation (varchar(255), Oui)
    cour_recreation = models.CharField(max_length=255, null=True, verbose_name="Cour de Récréation")

    # 11. etablissement_pris_en_charge_programme_refugies (varchar(255), Oui)
    etablissement_pris_en_charge_programme_refugies = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Établissement Programme Réfugiés"
    )

    # 12. internet (varchar(255), Oui)
    internet = models.CharField(max_length=255, null=True, verbose_name="Internet")

    # 13. latrines (varchar(255), Oui)
    latrines = models.CharField(max_length=255, null=True, verbose_name="Latrines")

    # 14. locaux_utilises (varchar(255), Oui)
    locaux_utilises = models.CharField(max_length=255, null=True, verbose_name="Locaux Utilisés")

    # 15. nature_cloture (varchar(255), Oui)
    nature_cloture = models.CharField(max_length=255, null=True, verbose_name="Nature Clôture")

    # 16. nbr_femmes_dans_copa (varchar(255), Oui)
    nbr_femmes_dans_copa = models.CharField(max_length=255, null=True, verbose_name="Nombre de Femmes dans COPA")

    # 17. nbr_femmes_dans_coges (varchar(255), Oui, Défaut: 0)
    nbr_femmes_dans_coges = models.CharField(
        max_length=255, 
        null=True, 
        default='0',
        verbose_name="Nombre de Femmes dans CoGES"
    )
    
    # 18. nom_second_etablissement (varchar(255), Oui)
    nom_second_etablissement = models.CharField(max_length=255, null=True, verbose_name="Nom Second Établissement")

    # 19. nombre_compartiments (varchar(255), Oui)
    nombre_compartiments = models.CharField(max_length=255, null=True, verbose_name="Nombre de Compartiments")

    # 20. organisme_projet (varchar(255), Oui)
    organisme_projet = models.CharField(max_length=255, null=True, verbose_name="Organisme / Projet")

    # 21. par_quel_organisme (varchar(255), Oui)
    par_quel_organisme = models.CharField(max_length=255, null=True, verbose_name="Par Quel Organisme")

    # 22. plan_action (varchar(255), Oui)
    plan_action = models.CharField(max_length=255, null=True, verbose_name="Plan d'Action")

    # 23. point_eau (varchar(255), Oui)
    point_eau = models.CharField(max_length=255, null=True, verbose_name="Point d'Eau")

    # 24. prevision_budgetaire (varchar(255), Oui)
    prevision_budgetaire = models.CharField(max_length=255, null=True, verbose_name="Prévision Budgétaire")

    # 25. programmes_officiels (varchar(255), Oui)
    programmes_officiels = models.CharField(max_length=255, null=True, verbose_name="Programmes Officiels")

    # 26. projet_etablissement (varchar(255), Oui)
    projet_etablissement = models.CharField(max_length=255, null=True, verbose_name="Projet d'Établissement")

    # 27. reunions_pv (varchar(255), Oui)
    reunions_pv = models.CharField(max_length=255, null=True, verbose_name="PV Réunions")

    # 28. reunions_rapport (varchar(255), Oui)
    reunions_rapport = models.CharField(max_length=255, null=True, verbose_name="Rapport Réunions")

    # 29. revue_performance (varchar(255), Oui)
    revue_performance = models.CharField(max_length=255, null=True, verbose_name="Revue Performance")

    # 30. sources_energie (varchar(255), Oui)
    sources_energie = models.CharField(max_length=255, null=True, verbose_name="Sources Énergie")

    # 31. tableau_bord (varchar(255), Oui)
    tableau_bord = models.CharField(max_length=255, null=True, verbose_name="Tableau de Bord")

    # 32. terrain_jeux (varchar(255), Oui)
    terrain_jeux = models.CharField(max_length=255, null=True, verbose_name="Terrain de Jeux")

    # 33. type_point_eau (varchar(255), Oui)
    type_point_eau = models.CharField(max_length=255, null=True, verbose_name="Type Point d'Eau")

    # 34. type_sources_energie (varchar(255), Oui)
    type_sources_energie = models.CharField(max_length=255, null=True, verbose_name="Type Sources Énergie")

    def __str__(self):
        return f"Infos Générales ID: {self.id}"

    class Meta:
        verbose_name = "Information Générale"
        verbose_name_plural = "Informations Générales"

class Proveds(models.Model):
    # 1. createdAt (datetime(6), Oui)
    createdAt = models.DateTimeField(
        auto_now_add=True, # Enregistre la date à la création (si l'application gère ça)
        null=True, 
        verbose_name="Date de Création"
    )

    # 2. fk_province_id (bigint(20), Oui)
    # Clé étrangère vers le modèle Province (qui n'existe pas encore mais on fait l'hypothèse)
    fk_province_id = models.ForeignKey(
        'Province', 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name="Province ID (FK)"
    )

    # 3. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 4. libelle (varchar(255), Oui)
    libelle = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Libellé"
    )

    # 5. slug (varchar(255), Oui)
    slug = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Slug"
    )

    def __str__(self):
        # Utilise le libellé pour une meilleure lecture
        return self.libelle or f"Proved ID: {self.id}"

    class Meta:
        verbose_name = "Proved"
        verbose_name_plural = "Proveds"

class Provinces(models.Model):
    # 1. is_deleted (tinyint(1), Oui, Défaut: 0)
    # tinyint(1) -> BooleanField, Défaut 0 -> False
    is_deleted = models.BooleanField(
        default=False, 
        null=True,  # Correspond à 'Oui' pour Null
        verbose_name="Est Supprimé"
    )

    # 2. created_at (datetime(6), Oui)
    created_at = models.DateTimeField(
        auto_now_add=True, # Optionnel : Gère la date de création par Django
        null=True, 
        verbose_name="Date de Création"
    )

    # 3. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 4. user_id (bigint(20), Oui)
    # Clé étrangère vers le modèle User (ou BigIntegerField si le modèle User n'est pas encore défini)
    user_id = models.BigIntegerField(
        null=True, 
        verbose_name="Utilisateur ID"
    )

    # 5. chef_lieu (varchar(255), Oui)
    chef_lieu = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Chef-Lieu"
    )

    # 6. libelle (varchar(255), Oui)
    libelle = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Libellé"
    )

    # 7. slug (varchar(255), Oui)
    slug = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Slug"
    )

    def __str__(self):
        # Utilise le libellé pour une meilleure lecture
        return self.libelle or f"Province ID: {self.id}"

    class Meta:
        verbose_name = "Province"
        verbose_name_plural = "Provinces"

class Regimes_gestion(models.Model):
    # 1. created_at (datetime(6), Non)
    created_at = models.DateTimeField(
        auto_now_add=True, 
        null=False,
        verbose_name="Date de Création"
    )

    # 2. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 3. updated_at (datetime(6), Non)
    updated_at = models.DateTimeField(
        auto_now=True, 
        null=False,
        verbose_name="Date de Dernière Mise à Jour"
    )

    # 4. code (varchar(255), Non)
    code = models.CharField(
        max_length=255, 
        null=False, 
        unique=True, # J'ajoute unique=True car un 'code' est souvent unique
        verbose_name="Code du Régime"
    )

    # 5. description (varchar(255), Non)
    description = models.CharField(
        max_length=255, 
        null=False, 
        verbose_name="Description"
    )

    def __str__(self):
        # Utilise le code ou la description
        return f"{self.code} - {self.description}"

    class Meta:
        verbose_name = "Régime de Gestion"
        verbose_name_plural = "Régimes de Gestion"

class Sous_proved(models.Model):
    # 1. created_at (datetime(6), Oui)
    created_at = models.DateTimeField(
        auto_now_add=True, 
        null=True,
        verbose_name="Date de Création"
    )

    # 2. fk_proved_id (bigint(20), Oui)
    # Clé étrangère vers Proveds (modèle créé précédemment)
    fk_proved_id = models.ForeignKey(
        'Proveds', 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name="Proved ID (FK)"
    )

    # 3. fk_territoire_id (bigint(20), Oui)
    # Clé étrangère vers Territoires (modèle à venir)
    fk_territoire_id = models.ForeignKey(
        'Territoires', # Assurez-vous que le nom du modèle est correct
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name="Territoire ID (FK)"
    )

    # 4. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 5. libelle (varchar(255), Oui)
    libelle = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Libellé"
    )

    # 6. lieu_implantation (varchar(255), Oui)
    lieu_implantation = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Lieu d'Implantation"
    )

    # 7. slug (varchar(255), Oui)
    slug = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Slug"
    )

    def __str__(self):
        return self.libelle or f"Sous-Proved ID: {self.id}"

    class Meta:
        verbose_name = "Sous-Proved"
        verbose_name_plural = "Sous-Proveds"

class St1_eefectifs_par_age(models.Model):
    # 1. form_st_id (bigint(20), Oui)
    # Clé étrangère vers le formulaire ou l'établissement principal
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 2. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 3-32. Champs d'effectifs (varchar(255), Oui)

    # Effective Filles (moins de 3 ans, 3 ans, plus de 3 ans) par année (1ere, 2eme, 3eme)
    
    # Filles 3 ans
    effectif_filles_3ans_1ere = models.CharField(max_length=255, null=True, verbose_name="Filles 3 ans (1ère)")
    effectif_filles_3ans_2eme = models.CharField(max_length=255, null=True, verbose_name="Filles 3 ans (2ème)")
    effectif_filles_3ans_3eme = models.CharField(max_length=255, null=True, verbose_name="Filles 3 ans (3ème)")
    
    # Filles 4 ans
    effectif_filles_4ans_1ere = models.CharField(max_length=255, null=True, verbose_name="Filles 4 ans (1ère)")
    effectif_filles_4ans_2eme = models.CharField(max_length=255, null=True, verbose_name="Filles 4 ans (2ème)")
    effectif_filles_4ans_3eme = models.CharField(max_length=255, null=True, verbose_name="Filles 4 ans (3ème)")
    
    # Filles 5 ans
    effectif_filles_5ans_1ere = models.CharField(max_length=255, null=True, verbose_name="Filles 5 ans (1ère)")
    effectif_filles_5ans_2eme = models.CharField(max_length=255, null=True, verbose_name="Filles 5 ans (2ème)")
    effectif_filles_5ans_3eme = models.CharField(max_length=255, null=True, verbose_name="Filles 5 ans (3ème)")
    
    # Filles moins de 3 ans
    effectif_filles_moins_3ans_1ere = models.CharField(max_length=255, null=True, verbose_name="Filles < 3 ans (1ère)")
    effectif_filles_moins_3ans_2eme = models.CharField(max_length=255, null=True, verbose_name="Filles < 3 ans (2ème)")
    effectif_filles_moins_3ans_3eme = models.CharField(max_length=255, null=True, verbose_name="Filles < 3 ans (3ème)")
    
    # Filles plus de 5 ans
    effectif_filles_plus_5ans_1ere = models.CharField(max_length=255, null=True, verbose_name="Filles > 5 ans (1ère)")
    effectif_filles_plus_5ans_2eme = models.CharField(max_length=255, null=True, verbose_name="Filles > 5 ans (2ème)")
    effectif_filles_plus_5ans_3eme = models.CharField(max_length=255, null=True, verbose_name="Filles > 5 ans (3ème)")

    # Effective Garçons (moins de 3 ans, 3 ans, plus de 3 ans) par année (1ere, 2eme, 3eme)

    # Garçons 3 ans
    effectif_garcons_3ans_1ere = models.CharField(max_length=255, null=True, verbose_name="Garçons 3 ans (1ère)")
    effectif_garcons_3ans_2eme = models.CharField(max_length=255, null=True, verbose_name="Garçons 3 ans (2ème)")
    effectif_garcons_3ans_3eme = models.CharField(max_length=255, null=True, verbose_name="Garçons 3 ans (3ème)")
    
    # Garçons 4 ans
    effectif_garcons_4ans_1ere = models.CharField(max_length=255, null=True, verbose_name="Garçons 4 ans (1ère)")
    effectif_garcons_4ans_2eme = models.CharField(max_length=255, null=True, verbose_name="Garçons 4 ans (2ème)")
    effectif_garcons_4ans_3eme = models.CharField(max_length=255, null=True, verbose_name="Garçons 4 ans (3ème)")

    # Garçons 5 ans
    effectif_garcons_5ans_1ere = models.CharField(max_length=255, null=True, verbose_name="Garçons 5 ans (1ère)")
    effectif_garcons_5ans_2eme = models.CharField(max_length=255, null=True, verbose_name="Garçons 5 ans (2ème)")
    effectif_garcons_5ans_3eme = models.CharField(max_length=255, null=True, verbose_name="Garçons 5 ans (3ème)")

    # Garçons moins de 3 ans
    effectif_garcons_moins_3ans_1ere = models.CharField(max_length=255, null=True, verbose_name="Garçons < 3 ans (1ère)")
    effectif_garcons_moins_3ans_2eme = models.CharField(max_length=255, null=True, verbose_name="Garçons < 3 ans (2ème)")
    effectif_garcons_moins_3ans_3eme = models.CharField(max_length=255, null=True, verbose_name="Garçons < 3 ans (3ème)")
    
    # Garçons plus de 5 ans
    effectif_garcons_plus_5ans_1ere = models.CharField(max_length=255, null=True, verbose_name="Garçons > 5 ans (1ère)")
    effectif_garcons_plus_5ans_2eme = models.CharField(max_length=255, null=True, verbose_name="Garçons > 5 ans (2ème)")
    effectif_garcons_plus_5ans_3eme = models.CharField(max_length=255, null=True, verbose_name="Garçons > 5 ans (3ème)")


    def __str__(self):
        return f"Effectifs par âge (ID: {self.id})"

    class Meta:
        verbose_name = "Effectif par Âge"
        verbose_name_plural = "Effectifs par Âge"

class St1_enseignant(models.Model):
    # 1. form_st_id (bigint(20), Oui)
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 2. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 3. enseignants_autres_femmes_1ere (varchar(255), Oui)
    enseignants_autres_femmes_1ere = models.CharField(max_length=255, null=True, verbose_name="Autres Femmes (1ère)")
    
    # 4. enseignants_autres_femmes_2eme (varchar(255), Oui)
    enseignants_autres_femmes_2eme = models.CharField(max_length=255, null=True, verbose_name="Autres Femmes (2ème)")
    
    # 5. enseignants_autres_femmes_3eme (varchar(255), Oui)
    enseignants_autres_femmes_3eme = models.CharField(max_length=255, null=True, verbose_name="Autres Femmes (3ème)")

    # 6. enseignants_autres_hommes_1ere (varchar(255), Oui)
    enseignants_autres_hommes_1ere = models.CharField(max_length=255, null=True, verbose_name="Autres Hommes (1ère)")
    
    # 7. enseignants_autres_hommes_2eme (varchar(255), Oui)
    enseignants_autres_hommes_2eme = models.CharField(max_length=255, null=True, verbose_name="Autres Hommes (2ème)")
    
    # 8. enseignants_autres_hommes_3eme (varchar(255), Oui)
    enseignants_autres_hommes_3eme = models.CharField(max_length=255, null=True, verbose_name="Autres Hommes (3ème)")

    # Enseignants D4 Femmes
    # 9. enseignants_d4_femmes_1ere (varchar(255), Oui)
    enseignants_d4_femmes_1ere = models.CharField(max_length=255, null=True, verbose_name="D4 Femmes (1ère)")
    # 10. enseignants_d4_femmes_2eme (varchar(255), Oui)
    enseignants_d4_femmes_2eme = models.CharField(max_length=255, null=True, verbose_name="D4 Femmes (2ème)")
    # 11. enseignants_d4_femmes_3eme (varchar(255), Oui)
    enseignants_d4_femmes_3eme = models.CharField(max_length=255, null=True, verbose_name="D4 Femmes (3ème)")

    # Enseignants D4 Hommes
    # 12. enseignants_d4_hommes_1ere (varchar(255), Oui)
    enseignants_d4_hommes_1ere = models.CharField(max_length=255, null=True, verbose_name="D4 Hommes (1ère)")
    # 13. enseignants_d4_hommes_2eme (varchar(255), Oui)
    enseignants_d4_hommes_2eme = models.CharField(max_length=255, null=True, verbose_name="D4 Hommes (2ème)")
    # 14. enseignants_d4_hommes_3eme (varchar(255), Oui)
    enseignants_d4_hommes_3eme = models.CharField(max_length=255, null=True, verbose_name="D4 Hommes (3ème)")

    # Enseignants D6 Femmes
    # 15. enseignants_d6_femmes_1ere (varchar(255), Oui)
    enseignants_d6_femmes_1ere = models.CharField(max_length=255, null=True, verbose_name="D6 Femmes (1ère)")
    # 16. enseignants_d6_femmes_2eme (varchar(255), Oui)
    enseignants_d6_femmes_2eme = models.CharField(max_length=255, null=True, verbose_name="D6 Femmes (2ème)")
    # 17. enseignants_d6_femmes_3eme (varchar(255), Oui)
    enseignants_d6_femmes_3eme = models.CharField(max_length=255, null=True, verbose_name="D6 Femmes (3ème)")
    
    # Enseignants D6 Hommes
    # 18. enseignants_d6_hommes_1ere (varchar(255), Oui)
    enseignants_d6_hommes_1ere = models.CharField(max_length=255, null=True, verbose_name="D6 Hommes (1ère)")
    # 19. enseignants_d6_hommes_2eme (varchar(255), Oui)
    enseignants_d6_hommes_2eme = models.CharField(max_length=255, null=True, verbose_name="D6 Hommes (2ème)")
    # 20. enseignants_d6_hommes_3eme (varchar(255), Oui)
    enseignants_d6_hommes_3eme = models.CharField(max_length=255, null=True, verbose_name="D6 Hommes (3ème)")

    # Enseignants EM Femmes
    # 21. enseignants_em_femmes_1ere (varchar(255), Oui)
    enseignants_em_femmes_1ere = models.CharField(max_length=255, null=True, verbose_name="EM Femmes (1ère)")
    # 22. enseignants_em_femmes_2eme (varchar(255), Oui)
    enseignants_em_femmes_2eme = models.CharField(max_length=255, null=True, verbose_name="EM Femmes (2ème)")
    # 23. enseignants_em_femmes_3eme (varchar(255), Oui)
    enseignants_em_femmes_3eme = models.CharField(max_length=255, null=True, verbose_name="EM Femmes (3ème)")

    # Enseignants EM Hommes
    # 24. enseignants_em_hommes_1ere (varchar(255), Oui)
    enseignants_em_hommes_1ere = models.CharField(max_length=255, null=True, verbose_name="EM Hommes (1ère)")
    # 25. enseignants_em_hommes_2eme (varchar(255), Oui)
    enseignants_em_hommes_2eme = models.CharField(max_length=255, null=True, verbose_name="EM Hommes (2ème)")
    # 26. enseignants_em_hommes_3eme (varchar(255), Oui)
    enseignants_em_hommes_3eme = models.CharField(max_length=255, null=True, verbose_name="EM Hommes (3ème)")

    # Enseignants P6 Femmes
    # 27. enseignants_p6_femmes_1ere (varchar(255), Oui)
    enseignants_p6_femmes_1ere = models.CharField(max_length=255, null=True, verbose_name="P6 Femmes (1ère)")
    # 28. enseignants_p6_femmes_2eme (varchar(255), Oui)
    enseignants_p6_femmes_2eme = models.CharField(max_length=255, null=True, verbose_name="P6 Femmes (2ème)")
    # 29. enseignants_p6_femmes_3eme (varchar(255), Oui)
    enseignants_p6_femmes_3eme = models.CharField(max_length=255, null=True, verbose_name="P6 Femmes (3ème)")
    
    # Enseignants P6 Hommes
    # 30. enseignants_p6_hommes_1ere (varchar(255), Oui)
    enseignants_p6_hommes_1ere = models.CharField(max_length=255, null=True, verbose_name="P6 Hommes (1ère)")
    # 31. enseignants_p6_hommes_2eme (varchar(255), Oui)
    enseignants_p6_hommes_2eme = models.CharField(max_length=255, null=True, verbose_name="P6 Hommes (2ème)")
    # 32. enseignants_p6_hommes_3eme (varchar(255), Oui)
    enseignants_p6_hommes_3eme = models.CharField(max_length=255, null=True, verbose_name="P6 Hommes (3ème)")
    
    # 33. personnel_eligible_retraite (varchar(255), Oui)
    personnel_eligible_retraite = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Personnel Éligible Retraite"
    )

    def __str__(self):
        return f"Personnel Enseignant (ID: {self.id})"

    class Meta:
        verbose_name = "Personnel Enseignant"
        verbose_name_plural = "Personnel Enseignants"

class St1_groupes_specifiques(models.Model):
    # 1. form_st_id (bigint(20), Oui)
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 2. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 3-50. Champs d'effectifs (varchar(255), Oui)
    
    # 3-8. Autochtones (Filles/Garçons, 1ère, 2ème, 3ème)
    autochtones_filles_1ere = models.CharField(max_length=255, null=True, verbose_name="Autochtones Filles (1ère)")
    autochtones_filles_2eme = models.CharField(max_length=255, null=True, verbose_name="Autochtones Filles (2ème)")
    autochtones_filles_3eme = models.CharField(max_length=255, null=True, verbose_name="Autochtones Filles (3ème)")
    autochtones_garcons_1ere = models.CharField(max_length=255, null=True, verbose_name="Autochtones Garçons (1ère)")
    autochtones_garcons_2eme = models.CharField(max_length=255, null=True, verbose_name="Autochtones Garçons (2ème)")
    autochtones_garcons_3eme = models.CharField(max_length=255, null=True, verbose_name="Autochtones Garçons (3ème)")

    # 9-14. Déplacés Externes (Filles/Garçons)
    deplaces_externes_filles_1ere = models.CharField(max_length=255, null=True, verbose_name="Déplacés Ext. Filles (1ère)")
    deplaces_externes_filles_2eme = models.CharField(max_length=255, null=True, verbose_name="Déplacés Ext. Filles (2ème)")
    deplaces_externes_filles_3eme = models.CharField(max_length=255, null=True, verbose_name="Déplacés Ext. Filles (3ème)")
    deplaces_externes_garcons_1ere = models.CharField(max_length=255, null=True, verbose_name="Déplacés Ext. Garçons (1ère)")
    deplaces_externes_garcons_2eme = models.CharField(max_length=255, null=True, verbose_name="Déplacés Ext. Garçons (2ème)")
    deplaces_externes_garcons_3eme = models.CharField(max_length=255, null=True, verbose_name="Déplacés Ext. Garçons (3ème)")
    
    # 15-20. Déplacés Internes (Filles/Garçons)
    deplaces_internes_filles_1ere = models.CharField(max_length=255, null=True, verbose_name="Déplacés Int. Filles (1ère)")
    deplaces_internes_filles_2eme = models.CharField(max_length=255, null=True, verbose_name="Déplacés Int. Filles (2ème)")
    deplaces_internes_filles_3eme = models.CharField(max_length=255, null=True, verbose_name="Déplacés Int. Filles (3ème)")
    deplaces_internes_garcons_1ere = models.CharField(max_length=255, null=True, verbose_name="Déplacés Int. Garçons (1ère)")
    deplaces_internes_garcons_2eme = models.CharField(max_length=255, null=True, verbose_name="Déplacés Int. Garçons (2ème)")
    deplaces_internes_garcons_3eme = models.CharField(max_length=255, null=True, verbose_name="Déplacés Int. Garçons (3ème)")

    # 21-26. Étrangers (Filles/Garçons)
    etrangers_filles_1ere = models.CharField(max_length=255, null=True, verbose_name="Étrangers Filles (1ère)")
    etrangers_filles_2eme = models.CharField(max_length=255, null=True, verbose_name="Étrangers Filles (2ème)")
    etrangers_filles_3eme = models.CharField(max_length=255, null=True, verbose_name="Étrangers Filles (3ème)")
    etrangers_garcons_1ere = models.CharField(max_length=255, null=True, verbose_name="Étrangers Garçons (1ère)")
    etrangers_garcons_2eme = models.CharField(max_length=255, null=True, verbose_name="Étrangers Garçons (2ème)")
    etrangers_garcons_3eme = models.CharField(max_length=255, null=True, verbose_name="Étrangers Garçons (3ème)")
    
    # 27-32. Handicapés (Filles/Garçons)
    handicapes_filles_1ere = models.CharField(max_length=255, null=True, verbose_name="Handicapés Filles (1ère)")
    handicapes_filles_2eme = models.CharField(max_length=255, null=True, verbose_name="Handicapés Filles (2ème)")
    handicapes_filles_3eme = models.CharField(max_length=255, null=True, verbose_name="Handicapés Filles (3ème)")
    handicapes_garcons_1ere = models.CharField(max_length=255, null=True, verbose_name="Handicapés Garçons (1ère)")
    handicapes_garcons_2eme = models.CharField(max_length=255, null=True, verbose_name="Handicapés Garçons (2ème)")
    handicapes_garcons_3eme = models.CharField(max_length=255, null=True, verbose_name="Handicapés Garçons (3ème)")

    # 33-38. Orphelins (Filles/Garçons)
    orphelins_filles_1ere = models.CharField(max_length=255, null=True, verbose_name="Orphelins Filles (1ère)")
    orphelins_filles_2eme = models.CharField(max_length=255, null=True, verbose_name="Orphelins Filles (2ème)")
    orphelins_filles_3eme = models.CharField(max_length=255, null=True, verbose_name="Orphelins Filles (3ème)")
    orphelins_garcons_1ere = models.CharField(max_length=255, null=True, verbose_name="Orphelins Garçons (1ère)")
    orphelins_garcons_2eme = models.CharField(max_length=255, null=True, verbose_name="Orphelins Garçons (2ème)")
    orphelins_garcons_3eme = models.CharField(max_length=255, null=True, verbose_name="Orphelins Garçons (3ème)")
    
    # 39-44. Réfugiés (Filles/Garçons)
    refugies_filles_1ere = models.CharField(max_length=255, null=True, verbose_name="Réfugiés Filles (1ère)")
    refugies_filles_2eme = models.CharField(max_length=255, null=True, verbose_name="Réfugiés Filles (2ème)")
    refugies_filles_3eme = models.CharField(max_length=255, null=True, verbose_name="Réfugiés Filles (3ème)")
    refugies_garcons_1ere = models.CharField(max_length=255, null=True, verbose_name="Réfugiés Garçons (1ère)")
    refugies_garcons_2eme = models.CharField(max_length=255, null=True, verbose_name="Réfugiés Garçons (2ème)")
    refugies_garcons_3eme = models.CharField(max_length=255, null=True, verbose_name="Réfugiés Garçons (3ème)")

    # 45-50. Réintégrants (Filles/Garçons)
    reintegrants_filles_1ere = models.CharField(max_length=255, null=True, verbose_name="Réintégrants Filles (1ère)")
    reintegrants_filles_2eme = models.CharField(max_length=255, null=True, verbose_name="Réintégrants Filles (2ème)")
    reintegrants_filles_3eme = models.CharField(max_length=255, null=True, verbose_name="Réintégrants Filles (3ème)")
    reintegrants_garcons_1ere = models.CharField(max_length=255, null=True, verbose_name="Réintégrants Garçons (1ère)")
    reintegrants_garcons_2eme = models.CharField(max_length=255, null=True, verbose_name="Réintégrants Garçons (2ème)")
    reintegrants_garcons_3eme = models.CharField(max_length=255, null=True, verbose_name="Réintégrants Garçons (3ème)")

    def __str__(self):
        return f"Groupes Spécifiques (ID: {self.id})"

    class Meta:
        verbose_name = "Groupe Spécifique"
        verbose_name_plural = "Groupes Spécifiques"

class St1_guides_educateurs(models.Model):
    # 1. form_st_id (bigint(20), Oui)
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 2. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 3-20. Champs pour les guides/éducateurs (varchar(255), Oui)

    # Guides 'autres'
    guides_autres_1ere = models.CharField(max_length=255, null=True, verbose_name="Autres Guides (1ère)")
    guides_autres_2eme = models.CharField(max_length=255, null=True, verbose_name="Autres Guides (2ème)")
    guides_autres_3eme = models.CharField(max_length=255, null=True, verbose_name="Autres Guides (3ème)")

    # Guides 'comptage'
    guides_comptage_1ere = models.CharField(max_length=255, null=True, verbose_name="Guides Comptage (1ère)")
    guides_comptage_2eme = models.CharField(max_length=255, null=True, verbose_name="Guides Comptage (2ème)")
    guides_comptage_3eme = models.CharField(max_length=255, null=True, verbose_name="Guides Comptage (3ème)")

    # Guides 'étude du milieu'
    guides_etude_du_milieu_1ere = models.CharField(max_length=255, null=True, verbose_name="Guides Étude Milieu (1ère)")
    guides_etude_du_milieu_2eme = models.CharField(max_length=255, null=True, verbose_name="Guides Étude Milieu (2ème)")
    guides_etude_du_milieu_3eme = models.CharField(max_length=255, null=True, verbose_name="Guides Étude Milieu (3ème)")

    # Guides 'éveil'
    guides_eveil_1ere = models.CharField(max_length=255, null=True, verbose_name="Guides Éveil (1ère)")
    guides_eveil_2eme = models.CharField(max_length=255, null=True, verbose_name="Guides Éveil (2ème)")
    guides_eveil_3eme = models.CharField(max_length=255, null=True, verbose_name="Guides Éveil (3ème)") # Note: Manque '1ere' dans l'image, j'ai supposé 'eveil_1ere'

    # Guides 'français'
    guides_francais_1ere = models.CharField(max_length=255, null=True, verbose_name="Guides Français (1ère)")
    guides_francais_2eme = models.CharField(max_length=255, null=True, verbose_name="Guides Français (2ème)")
    guides_francais_3eme = models.CharField(max_length=255, null=True, verbose_name="Guides Français (3ème)")

    # Guides 'thèmes transversaux'
    guides_themes_transversaux_1ere = models.CharField(max_length=255, null=True, verbose_name="Guides Thèmes Transversaux (1ère)")
    guides_themes_transversaux_2eme = models.CharField(max_length=255, null=True, verbose_name="Guides Thèmes Transversaux (2ème)")
    guides_themes_transversaux_3eme = models.CharField(max_length=255, null=True, verbose_name="Guides Thèmes Transversaux (3ème)")

    def __str__(self):
        return f"Guides/Éducateurs (ID: {self.id})"

    class Meta:
        verbose_name = "Guide/Éducateur"
        verbose_name_plural = "Guides/Éducateurs"

class St1_infrastuctures(models.Model):
    # 1. form_st_id (bigint(20), Oui)
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 2. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 3-8. Champs de salles de classe (varchar(255), Oui)

    # Nombre de salles autorisées
    nb_salles_autorisees_1ere = models.CharField(max_length=255, null=True, verbose_name="Salles Autorisées (1ère année)")
    nb_salles_autorisees_2eme = models.CharField(max_length=255, null=True, verbose_name="Salles Autorisées (2ème année)")
    nb_salles_autorisees_3eme = models.CharField(max_length=255, null=True, verbose_name="Salles Autorisées (3ème année)")

    # Nombre de salles organisées
    nb_salles_organisees_1ere = models.CharField(max_length=255, null=True, verbose_name="Salles Organisées (1ère année)")
    nb_salles_organisees_2eme = models.CharField(max_length=255, null=True, verbose_name="Salles Organisées (2ème année)")
    nb_salles_organisees_3eme = models.CharField(max_length=255, null=True, verbose_name="Salles Organisées (3ème année)")

    def __str__(self):
        return f"Infrastructure (ID: {self.id})"

    class Meta:
        verbose_name = "Infrastructure ST1"
        verbose_name_plural = "Infrastructures ST1"

class St1_locaux(models.Model):
    # 1. form_st_id (bigint(20), Oui)
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 2. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 3-62. Champs de locaux (varchar(255), Oui)

    # Locaux: Bureau
    bureau_dur_bon = models.CharField(max_length=255, null=True, verbose_name="Bureau Dur (Bon)")
    bureau_dur_mauvais = models.CharField(max_length=255, null=True, verbose_name="Bureau Dur (Mauvais)")
    bureau_paille_bon = models.CharField(max_length=255, null=True, verbose_name="Bureau Paille (Bon)")
    bureau_paille_mauvais = models.CharField(max_length=255, null=True, verbose_name="Bureau Paille (Mauvais)")
    bureau_semidur_bon = models.CharField(max_length=255, null=True, verbose_name="Bureau Semi-Dur (Bon)")
    bureau_semidur_mauvais = models.CharField(max_length=255, null=True, verbose_name="Bureau Semi-Dur (Mauvais)")
    bureau_terre_bon = models.CharField(max_length=255, null=True, verbose_name="Bureau Terre (Bon)")
    bureau_terre_mauvais = models.CharField(max_length=255, null=True, verbose_name="Bureau Terre (Mauvais)")

    # Locaux: Magasin
    magasin_dur_bon = models.CharField(max_length=255, null=True, verbose_name="Magasin Dur (Bon)")
    magasin_dur_mauvais = models.CharField(max_length=255, null=True, verbose_name="Magasin Dur (Mauvais)")
    magasin_paille_bon = models.CharField(max_length=255, null=True, verbose_name="Magasin Paille (Bon)")
    magasin_paille_mauvais = models.CharField(max_length=255, null=True, verbose_name="Magasin Paille (Mauvais)")
    magasin_semidur_bon = models.CharField(max_length=255, null=True, verbose_name="Magasin Semi-Dur (Bon)")
    magasin_semidur_mauvais = models.CharField(max_length=255, null=True, verbose_name="Magasin Semi-Dur (Mauvais)")
    magasin_terre_bon = models.CharField(max_length=255, null=True, verbose_name="Magasin Terre (Bon)")
    magasin_terre_mauvais = models.CharField(max_length=255, null=True, verbose_name="Magasin Terre (Mauvais)")

    # Locaux: Salle Activités
    salle_activites_dur_bon = models.CharField(max_length=255, null=True, verbose_name="Salle Activités Dur (Bon)")
    salle_activites_dur_mauvais = models.CharField(max_length=255, null=True, verbose_name="Salle Activités Dur (Mauvais)")
    salle_activites_paille_bon = models.CharField(max_length=255, null=True, verbose_name="Salle Activités Paille (Bon)")
    salle_activites_paille_mauvais = models.CharField(max_length=255, null=True, verbose_name="Salle Activités Paille (Mauvais)")
    salle_activites_semidur_bon = models.CharField(max_length=255, null=True, verbose_name="Salle Activités Semi-Dur (Bon)")
    salle_activites_semidur_mauvais = models.CharField(max_length=255, null=True, verbose_name="Salle Activités Semi-Dur (Mauvais)")
    salle_activites_terre_bon = models.CharField(max_length=255, null=True, verbose_name="Salle Activités Terre (Bon)")
    salle_activites_terre_mauvais = models.CharField(max_length=255, null=True, verbose_name="Salle Activités Terre (Mauvais)")

    # Locaux: Salle Attente
    salle_attente_dur_bon = models.CharField(max_length=255, null=True, verbose_name="Salle Attente Dur (Bon)")
    salle_attente_dur_mauvais = models.CharField(max_length=255, null=True, verbose_name="Salle Attente Dur (Mauvais)")
    salle_attente_paille_bon = models.CharField(max_length=255, null=True, verbose_name="Salle Attente Paille (Bon)")
    salle_attente_paille_mauvais = models.CharField(max_length=255, null=True, verbose_name="Salle Attente Paille (Mauvais)")
    salle_attente_semidur_bon = models.CharField(max_length=255, null=True, verbose_name="Salle Attente Semi-Dur (Bon)")
    salle_attente_semidur_mauvais = models.CharField(max_length=255, null=True, verbose_name="Salle Attente Semi-Dur (Mauvais)")
    salle_attente_terre_bon = models.CharField(max_length=255, null=True, verbose_name="Salle Attente Terre (Bon)")
    salle_attente_terre_mauvais = models.CharField(max_length=255, null=True, verbose_name="Salle Attente Terre (Mauvais)")

    # Locaux: Salle Jeux
    salle_jeux_dur_bon = models.CharField(max_length=255, null=True, verbose_name="Salle Jeux Dur (Bon)")
    salle_jeux_dur_mauvais = models.CharField(max_length=255, null=True, verbose_name="Salle Jeux Dur (Mauvais)")
    salle_jeux_paille_bon = models.CharField(max_length=255, null=True, verbose_name="Salle Jeux Paille (Bon)")
    salle_jeux_paille_mauvais = models.CharField(max_length=255, null=True, verbose_name="Salle Jeux Paille (Mauvais)")
    salle_jeux_semidur_bon = models.CharField(max_length=255, null=True, verbose_name="Salle Jeux Semi-Dur (Bon)")
    salle_jeux_semidur_mauvais = models.CharField(max_length=255, null=True, verbose_name="Salle Jeux Semi-Dur (Mauvais)")
    salle_jeux_terre_bon = models.CharField(max_length=255, null=True, verbose_name="Salle Jeux Terre (Bon)")
    salle_jeux_terre_mauvais = models.CharField(max_length=255, null=True, verbose_name="Salle Jeux Terre (Mauvais)")

    # Locaux: Salle Repos (Repos)
    salle_repos_dur_bon = models.CharField(max_length=255, null=True, verbose_name="Salle Repos Dur (Bon)")
    salle_repos_dur_mauvais = models.CharField(max_length=255, null=True, verbose_name="Salle Repos Dur (Mauvais)")
    salle_repos_paille_bon = models.CharField(max_length=255, null=True, verbose_name="Salle Repos Paille (Bon)")
    salle_repos_paille_mauvais = models.CharField(max_length=255, null=True, verbose_name="Salle Repos Paille (Mauvais)")
    salle_repos_semidur_bon = models.CharField(max_length=255, null=True, verbose_name="Salle Repos Semi-Dur (Bon)")
    salle_repos_semidur_mauvais = models.CharField(max_length=255, null=True, verbose_name="Salle Repos Semi-Dur (Mauvais)")
    salle_repos_terre_bon = models.CharField(max_length=255, null=True, verbose_name="Salle Repos Terre (Bon)")
    salle_repos_terre_mauvais = models.CharField(max_length=255, null=True, verbose_name="Salle Repos Terre (Mauvais)")


    def __str__(self):
        return f"Locaux (ID: {self.id})"

    class Meta:
        verbose_name = "Local ST1"
        verbose_name_plural = "Locaux ST1"

class St1_manuels_enfants(models.Model):
    # 1. form_st_id (bigint(20), Oui)
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 2. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 3-20. Champs pour les manuels des enfants (varchar(255), Oui)

    # Manuels 'autres'
    manuels_autres_1ere = models.CharField(max_length=255, null=True, verbose_name="Autres Manuels Enfants (1ère)")
    manuels_autres_2eme = models.CharField(max_length=255, null=True, verbose_name="Autres Manuels Enfants (2ème)")
    manuels_autres_3eme = models.CharField(max_length=255, null=True, verbose_name="Autres Manuels Enfants (3ème)")

    # Manuels 'comptage'
    manuels_comptage_1ere = models.CharField(max_length=255, null=True, verbose_name="Manuels Comptage (1ère)")
    manuels_comptage_2eme = models.CharField(max_length=255, null=True, verbose_name="Manuels Comptage (2ème)")
    manuels_comptage_3eme = models.CharField(max_length=255, null=True, verbose_name="Manuels Comptage (3ème)")

    # Manuels 'étude du milieu'
    manuels_etude_du_milieu_1ere = models.CharField(max_length=255, null=True, verbose_name="Manuels Étude Milieu (1ère)")
    manuels_etude_du_milieu_2eme = models.CharField(max_length=255, null=True, verbose_name="Manuels Étude Milieu (2ème)")
    manuels_etude_du_milieu_3eme = models.CharField(max_length=255, null=True, verbose_name="Manuels Étude Milieu (3ème)")

    # Manuels 'éveil'
    manuels_eveil_1ere = models.CharField(max_length=255, null=True, verbose_name="Manuels Éveil (1ère)")
    manuels_eveil_2eme = models.CharField(max_length=255, null=True, verbose_name="Manuels Éveil (2ème)")
    manuels_eveil_3eme = models.CharField(max_length=255, null=True, verbose_name="Manuels Éveil (3ème)")

    # Manuels 'français'
    manuels_francais_1ere = models.CharField(max_length=255, null=True, verbose_name="Manuels Français (1ère)")
    manuels_francais_2eme = models.CharField(max_length=255, null=True, verbose_name="Manuels Français (2ème)")
    manuels_francais_3eme = models.CharField(max_length=255, null=True, verbose_name="Manuels Français (3ème)")

    # Manuels 'thèmes transversaux'
    manuels_themes_transversaux_1ere = models.CharField(max_length=255, null=True, verbose_name="Manuels Thèmes Transversaux (1ère)")
    manuels_themes_transversaux_2eme = models.CharField(max_length=255, null=True, verbose_name="Manuels Thèmes Transversaux (2ème)")
    manuels_themes_transversaux_3eme = models.CharField(max_length=255, null=True, verbose_name="Manuels Thèmes Transversaux (3ème)")

    def __str__(self):
        return f"Manuels Enfants (ID: {self.id})"

    class Meta:
        verbose_name = "Manuel Enfant ST1"
        verbose_name_plural = "Manuels Enfants ST1"

class St1_personnel_administratif(models.Model):
    # 1. form_st_id (bigint(20), Oui)
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 2. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 3-42. Champs du personnel (varchar(255), Oui)

    # Catégorie 'autres'
    autres_directeur_f = models.CharField(max_length=255, null=True, verbose_name="Autres Directrices (F)")
    autres_directeur_h = models.CharField(max_length=255, null=True, verbose_name="Autres Directeurs (H)")
    autres_directeur_adjoint_f = models.CharField(max_length=255, null=True, verbose_name="Autres Directrices Adjointes (F)")
    autres_directeur_adjoint_h = models.CharField(max_length=255, null=True, verbose_name="Autres Directeurs Adjoints (H)")
    autres_ouvrier_f = models.CharField(max_length=255, null=True, verbose_name="Autres Ouvrières (F)")
    autres_ouvrier_h = models.CharField(max_length=255, null=True, verbose_name="Autres Ouvriers (H)")
    autres_surveillant_f = models.CharField(max_length=255, null=True, verbose_name="Autres Surveillantes (F)")
    autres_surveillant_h = models.CharField(max_length=255, null=True, verbose_name="Autres Surveillants (H)")

    # Catégorie D4
    d4_directeur_f = models.CharField(max_length=255, null=True, verbose_name="D4 Directrice (F)")
    d4_directeur_h = models.CharField(max_length=255, null=True, verbose_name="D4 Directeur (H)")
    d4_directeur_adjoint_f = models.CharField(max_length=255, null=True, verbose_name="D4 Directrice Adjointe (F)")
    d4_directeur_adjoint_h = models.CharField(max_length=255, null=True, verbose_name="D4 Directeur Adjoint (H)")
    d4_ouvrier_f = models.CharField(max_length=255, null=True, verbose_name="D4 Ouvrière (F)")
    d4_ouvrier_h = models.CharField(max_length=255, null=True, verbose_name="D4 Ouvrier (H)")
    d4_surveillant_f = models.CharField(max_length=255, null=True, verbose_name="D4 Surveillante (F)")
    d4_surveillant_h = models.CharField(max_length=255, null=True, verbose_name="D4 Surveillant (H)")

    # Catégorie D6
    d6_directeur_f = models.CharField(max_length=255, null=True, verbose_name="D6 Directrice (F)")
    d6_directeur_h = models.CharField(max_length=255, null=True, verbose_name="D6 Directeur (H)")
    d6_directeur_adjoint_f = models.CharField(max_length=255, null=True, verbose_name="D6 Directrice Adjointe (F)")
    d6_directeur_adjoint_h = models.CharField(max_length=255, null=True, verbose_name="D6 Directeur Adjoint (H)")
    d6_ouvrier_f = models.CharField(max_length=255, null=True, verbose_name="D6 Ouvrière (F)")
    d6_ouvrier_h = models.CharField(max_length=255, null=True, verbose_name="D6 Ouvrier (H)")
    d6_surveillant_f = models.CharField(max_length=255, null=True, verbose_name="D6 Surveillante (F)")
    d6_surveillant_h = models.CharField(max_length=255, null=True, verbose_name="D6 Surveillant (H)")
    
    # Catégorie EM
    em_directeur_f = models.CharField(max_length=255, null=True, verbose_name="EM Directrice (F)")
    em_directeur_h = models.CharField(max_length=255, null=True, verbose_name="EM Directeur (H)")
    em_directeur_adjoint_f = models.CharField(max_length=255, null=True, verbose_name="EM Directrice Adjointe (F)")
    em_directeur_adjoint_h = models.CharField(max_length=255, null=True, verbose_name="EM Directeur Adjoint (H)")
    em_ouvrier_f = models.CharField(max_length=255, null=True, verbose_name="EM Ouvrière (F)")
    em_ouvrier_h = models.CharField(max_length=255, null=True, verbose_name="EM Ouvrier (H)")
    em_surveillant_f = models.CharField(max_length=255, null=True, verbose_name="EM Surveillante (F)")
    em_surveillant_h = models.CharField(max_length=255, null=True, verbose_name="EM Surveillant (H)")

    # Catégorie P6
    p6_directeur_f = models.CharField(max_length=255, null=True, verbose_name="P6 Directrice (F)")
    p6_directeur_h = models.CharField(max_length=255, null=True, verbose_name="P6 Directeur (H)")
    p6_directeur_adjoint_f = models.CharField(max_length=255, null=True, verbose_name="P6 Directrice Adjointe (F)")
    p6_directeur_adjoint_h = models.CharField(max_length=255, null=True, verbose_name="P6 Directeur Adjoint (H)")
    p6_ouvrier_f = models.CharField(max_length=255, null=True, verbose_name="P6 Ouvrière (F)")
    p6_ouvrier_h = models.CharField(max_length=255, null=True, verbose_name="P6 Ouvrier (H)")
    p6_surveillant_f = models.CharField(max_length=255, null=True, verbose_name="P6 Surveillante (F)")
    p6_surveillant_h = models.CharField(max_length=255, null=True, verbose_name="P6 Surveillant (H)")

    def __str__(self):
        return f"Personnel Administratif (ID: {self.id})"

    class Meta:
        verbose_name = "Personnel Administratif ST1"
        verbose_name_plural = "Personnel Administratif ST1"

class St2_classes_autorisees_et_organisees(models.Model):
    # 1. form_st_id (bigint(20), Oui)
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 2. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 3-16. Champs de classes autorisées et organisées (varchar(255), Oui)

    # Nombre de classes autorisées (Niveaux 0 à 6)
    st2_nombre_classes_autorise_0 = models.CharField(max_length=255, null=True, verbose_name="Classes Autorisées (Niveau 0)")
    st2_nombre_classes_autorise_1 = models.CharField(max_length=255, null=True, verbose_name="Classes Autorisées (Niveau 1)")
    st2_nombre_classes_autorise_2 = models.CharField(max_length=255, null=True, verbose_name="Classes Autorisées (Niveau 2)")
    st2_nombre_classes_autorise_3 = models.CharField(max_length=255, null=True, verbose_name="Classes Autorisées (Niveau 3)")
    st2_nombre_classes_autorise_4 = models.CharField(max_length=255, null=True, verbose_name="Classes Autorisées (Niveau 4)")
    st2_nombre_classes_autorise_5 = models.CharField(max_length=255, null=True, verbose_name="Classes Autorisées (Niveau 5)")
    st2_nombre_classes_autorise_6 = models.CharField(max_length=255, null=True, verbose_name="Classes Autorisées (Niveau 6)")

    # Nombre de classes organisées (Niveaux 0 à 6)
    st2_nombre_classes_organise_0 = models.CharField(max_length=255, null=True, verbose_name="Classes Organisées (Niveau 0)")
    st2_nombre_classes_organise_1 = models.CharField(max_length=255, null=True, verbose_name="Classes Organisées (Niveau 1)")
    st2_nombre_classes_organise_2 = models.CharField(max_length=255, null=True, verbose_name="Classes Organisées (Niveau 2)")
    st2_nombre_classes_organise_3 = models.CharField(max_length=255, null=True, verbose_name="Classes Organisées (Niveau 3)")
    st2_nombre_classes_organise_4 = models.CharField(max_length=255, null=True, verbose_name="Classes Organisées (Niveau 4)")
    st2_nombre_classes_organise_5 = models.CharField(max_length=255, null=True, verbose_name="Classes Organisées (Niveau 5)")
    st2_nombre_classes_organise_6 = models.CharField(max_length=255, null=True, verbose_name="Classes Organisées (Niveau 6)")

    def __str__(self):
        return f"Classes Autorisées et Organisées ST2 (ID: {self.id})"

    class Meta:
        verbose_name = "Classes ST2"
        verbose_name_plural = "Classes ST2"

class St2_effectifs_eleve_ciquieme(models.Model):
    # 1. form_st_id (bigint(20), Oui)
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 2. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 3-30. Champs d'effectifs (varchar(255), Oui)

    # Filles - Répartition par âge (9 à plus de 11 ans)
    st2_nombre_cinquieme_f_10 = models.CharField(max_length=255, null=True, verbose_name="Filles 10 ans (5ème)")
    st2_nombre_cinquieme_f_11 = models.CharField(max_length=255, null=True, verbose_name="Filles 11 ans (5ème)")
    st2_nombre_cinquieme_f_8 = models.CharField(max_length=255, null=True, verbose_name="Filles 8 ans (5ème)")
    st2_nombre_cinquieme_f_9 = models.CharField(max_length=255, null=True, verbose_name="Filles 9 ans (5ème)")
    
    # Filles - Groupes spécifiques
    st2_nombre_cinquieme_f_dont_autochtone = models.CharField(max_length=255, null=True, verbose_name="Filles dont Autochtones (5ème)")
    st2_nombre_cinquieme_f_dont_avec_handicap = models.CharField(max_length=255, null=True, verbose_name="Filles dont avec Handicap (5ème)")
    st2_nombre_cinquieme_f_dont_deplaces = models.CharField(max_length=255, null=True, verbose_name="Filles dont Déplacés (5ème)")
    st2_nombre_cinquieme_f_dont_etrangers = models.CharField(max_length=255, null=True, verbose_name="Filles dont Étrangers (5ème)")
    st2_nombre_cinquieme_f_dont_internants = models.CharField(max_length=255, null=True, verbose_name="Filles dont Internants (5ème)")
    st2_nombre_cinquieme_f_dont_orphelins = models.CharField(max_length=255, null=True, verbose_name="Filles dont Orphelins (5ème)")
    st2_nombre_cinquieme_f_dont_redoublons = models.CharField(max_length=255, null=True, verbose_name="Filles dont Redoublants (5ème)")
    st2_nombre_cinquieme_f_dont_refugies = models.CharField(max_length=255, null=True, verbose_name="Filles dont Réfugiés (5ème)")
    st2_nombre_cinquieme_f_dont_reintegrants = models.CharField(max_length=255, null=True, verbose_name="Filles dont Réintégrants (5ème)")
    st2_nombre_cinquieme_f_g_plus11 = models.CharField(max_length=255, null=True, verbose_name="Filles > 11 ans (5ème)")

    # Garçons - Répartition par âge (9 à plus de 11 ans)
    st2_nombre_cinquieme_g_10 = models.CharField(max_length=255, null=True, verbose_name="Garçons 10 ans (5ème)")
    st2_nombre_cinquieme_g_11 = models.CharField(max_length=255, null=True, verbose_name="Garçons 11 ans (5ème)")
    st2_nombre_cinquieme_g_8 = models.CharField(max_length=255, null=True, verbose_name="Garçons 8 ans (5ème)")
    st2_nombre_cinquieme_g_9 = models.CharField(max_length=255, null=True, verbose_name="Garçons 9 ans (5ème)")
    
    # Garçons - Groupes spécifiques
    st2_nombre_cinquieme_g_dont_autochtone = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Autochtones (5ème)")
    st2_nombre_cinquieme_g_dont_avec_handicap = models.CharField(max_length=255, null=True, verbose_name="Garçons dont avec Handicap (5ème)")
    st2_nombre_cinquieme_g_dont_deplaces = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Déplacés (5ème)")
    st2_nombre_cinquieme_g_dont_etrangers = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Étrangers (5ème)")
    st2_nombre_cinquieme_g_dont_internants = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Internants (5ème)")
    st2_nombre_cinquieme_g_dont_orphelins = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Orphelins (5ème)")
    st2_nombre_cinquieme_g_dont_redoublons = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Redoublants (5ème)")
    st2_nombre_cinquieme_g_dont_refugies = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Réfugiés (5ème)")
    st2_nombre_cinquieme_g_dont_reintegrants = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Réintégrants (5ème)")
    st2_nombre_cinquieme_g_g_plus11 = models.CharField(max_length=255, null=True, verbose_name="Garçons > 11 ans (5ème)")


    def __str__(self):
        return f"Effectifs 5ème année ST2 (ID: {self.id})"

    class Meta:
        verbose_name = "Effectif Élève 5ème ST2"
        verbose_name_plural = "Effectifs Élèves 5ème ST2"

class St2_effectifs_eleve_deuxieme(models.Model):
    # 1. form_st_id (bigint(20), Oui)
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 2. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 3-36. Champs d'effectifs (varchar(255), Oui)

    # Filles - Répartition par âge (6 à plus de 11 ans)
    st2_nombre_deuxieme_f_10 = models.CharField(max_length=255, null=True, verbose_name="Filles 10 ans (2ème)")
    st2_nombre_deuxieme_f_11 = models.CharField(max_length=255, null=True, verbose_name="Filles 11 ans (2ème)")
    st2_nombre_deuxieme_f_6 = models.CharField(max_length=255, null=True, verbose_name="Filles 6 ans (2ème)")
    st2_nombre_deuxieme_f_7 = models.CharField(max_length=255, null=True, verbose_name="Filles 7 ans (2ème)")
    st2_nombre_deuxieme_f_8 = models.CharField(max_length=255, null=True, verbose_name="Filles 8 ans (2ème)")
    st2_nombre_deuxieme_f_9 = models.CharField(max_length=255, null=True, verbose_name="Filles 9 ans (2ème)")
    
    # Filles - Groupes spécifiques
    st2_nombre_deuxieme_f_dont_autochtone = models.CharField(max_length=255, null=True, verbose_name="Filles dont Autochtones (2ème)")
    st2_nombre_deuxieme_f_dont_avec_handicap = models.CharField(max_length=255, null=True, verbose_name="Filles dont avec Handicap (2ème)")
    st2_nombre_deuxieme_f_dont_deplaces = models.CharField(max_length=255, null=True, verbose_name="Filles dont Déplacés (2ème)")
    st2_nombre_deuxieme_f_dont_etrangers = models.CharField(max_length=255, null=True, verbose_name="Filles dont Étrangers (2ème)")
    st2_nombre_deuxieme_f_dont_internants = models.CharField(max_length=255, null=True, verbose_name="Filles dont Internants (2ème)")
    st2_nombre_deuxieme_f_dont_orphelins = models.CharField(max_length=255, null=True, verbose_name="Filles dont Orphelins (2ème)")
    st2_nombre_deuxieme_f_dont_redoublons = models.CharField(max_length=255, null=True, verbose_name="Filles dont Redoublants (2ème)")
    st2_nombre_deuxieme_f_dont_refugies = models.CharField(max_length=255, null=True, verbose_name="Filles dont Réfugiés (2ème)")
    st2_nombre_deuxieme_f_dont_reintegrants = models.CharField(max_length=255, null=True, verbose_name="Filles dont Réintégrants (2ème)")
    st2_nombre_deuxieme_f_g_moins6 = models.CharField(max_length=255, null=True, verbose_name="Filles < 6 ans (2ème)")
    st2_nombre_deuxieme_f_g_plus11 = models.CharField(max_length=255, null=True, verbose_name="Filles > 11 ans (2ème)")

    # Garçons - Répartition par âge (6 à plus de 11 ans)
    st2_nombre_deuxieme_g_10 = models.CharField(max_length=255, null=True, verbose_name="Garçons 10 ans (2ème)")
    st2_nombre_deuxieme_g_11 = models.CharField(max_length=255, null=True, verbose_name="Garçons 11 ans (2ème)")
    st2_nombre_deuxieme_g_6 = models.CharField(max_length=255, null=True, verbose_name="Garçons 6 ans (2ème)")
    st2_nombre_deuxieme_g_7 = models.CharField(max_length=255, null=True, verbose_name="Garçons 7 ans (2ème)")
    st2_nombre_deuxieme_g_8 = models.CharField(max_length=255, null=True, verbose_name="Garçons 8 ans (2ème)")
    st2_nombre_deuxieme_g_9 = models.CharField(max_length=255, null=True, verbose_name="Garçons 9 ans (2ème)")
    
    # Garçons - Groupes spécifiques
    st2_nombre_deuxieme_g_dont_autochtone = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Autochtones (2ème)")
    st2_nombre_deuxieme_g_dont_avec_handicap = models.CharField(max_length=255, null=True, verbose_name="Garçons dont avec Handicap (2ème)")
    st2_nombre_deuxieme_g_dont_deplaces = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Déplacés (2ème)")
    st2_nombre_deuxieme_g_dont_etrangers = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Étrangers (2ème)")
    st2_nombre_deuxieme_g_dont_internants = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Internants (2ème)")
    st2_nombre_deuxieme_g_dont_orphelins = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Orphelins (2ème)")
    st2_nombre_deuxieme_g_dont_redoublons = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Redoublants (2ème)")
    st2_nombre_deuxieme_g_dont_refugies = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Réfugiés (2ème)")
    st2_nombre_deuxieme_g_dont_reintegrants = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Réintégrants (2ème)")
    st2_nombre_deuxieme_g_g_moins6 = models.CharField(max_length=255, null=True, verbose_name="Garçons < 6 ans (2ème)")
    st2_nombre_deuxieme_g_g_plus11 = models.CharField(max_length=255, null=True, verbose_name="Garçons > 11 ans (2ème)")

    def __str__(self):
        return f"Effectifs 2ème année ST2 (ID: {self.id})"

    class Meta:
        verbose_name = "Effectif Élève 2ème ST2"
        verbose_name_plural = "Effectifs Élèves 2ème ST2"

class St2_effectifs_eleve_premiere(models.Model):
    # 1. form_st_id (bigint(20), Oui)
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    ) #

    # 2. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 3-36. Champs d'effectifs (varchar(255), Oui)

    # Filles - Répartition par âge (6 à plus de 11 ans)
    st2_nombre_premiere_f_10 = models.CharField(max_length=255, null=True, verbose_name="Filles 10 ans (1ère)") #
    st2_nombre_premiere_f_11 = models.CharField(max_length=255, null=True, verbose_name="Filles 11 ans (1ère)") #
    st2_nombre_premiere_f_6 = models.CharField(max_length=255, null=True, verbose_name="Filles 6 ans (1ère)") #
    st2_nombre_premiere_f_7 = models.CharField(max_length=255, null=True, verbose_name="Filles 7 ans (1ère)") #
    st2_nombre_premiere_f_8 = models.CharField(max_length=255, null=True, verbose_name="Filles 8 ans (1ère)") #
    st2_nombre_premiere_f_9 = models.CharField(max_length=255, null=True, verbose_name="Filles 9 ans (1ère)") #
    
    # Filles - Groupes spécifiques
    st2_nombre_premiere_f_dont_autochtone = models.CharField(max_length=255, null=True, verbose_name="Filles dont Autochtones (1ère)") #
    st2_nombre_premiere_f_dont_avec_handicap = models.CharField(max_length=255, null=True, verbose_name="Filles dont avec Handicap (1ère)") #
    st2_nombre_premiere_f_dont_deplaces = models.CharField(max_length=255, null=True, verbose_name="Filles dont Déplacés (1ère)") #
    st2_nombre_premiere_f_dont_etrangers = models.CharField(max_length=255, null=True, verbose_name="Filles dont Étrangers (1ère)") #
    st2_nombre_premiere_f_dont_internants = models.CharField(max_length=255, null=True, verbose_name="Filles dont Internants (1ère)") #
    st2_nombre_premiere_f_dont_orphelins = models.CharField(max_length=255, null=True, verbose_name="Filles dont Orphelins (1ère)") #
    st2_nombre_premiere_f_dont_redoublons = models.CharField(max_length=255, null=True, verbose_name="Filles dont Redoublants (1ère)") #
    st2_nombre_premiere_f_dont_refugies = models.CharField(max_length=255, null=True, verbose_name="Filles dont Réfugiés (1ère)") #
    st2_nombre_premiere_f_dont_reintegrants = models.CharField(max_length=255, null=True, verbose_name="Filles dont Réintégrants (1ère)") #
    st2_nombre_premiere_f_moins6 = models.CharField(max_length=255, null=True, verbose_name="Filles < 6 ans (1ère)") #
    st2_nombre_premiere_f_plus11 = models.CharField(max_length=255, null=True, verbose_name="Filles > 11 ans (1ère)") #

    # Garçons - Répartition par âge (6 à plus de 11 ans)
    st2_nombre_premiere_g_10 = models.CharField(max_length=255, null=True, verbose_name="Garçons 10 ans (1ère)") #
    st2_nombre_premiere_g_11 = models.CharField(max_length=255, null=True, verbose_name="Garçons 11 ans (1ère)") #
    st2_nombre_premiere_g_6 = models.CharField(max_length=255, null=True, verbose_name="Garçons 6 ans (1ère)") #
    st2_nombre_premiere_g_7 = models.CharField(max_length=255, null=True, verbose_name="Garçons 7 ans (1ère)") #
    st2_nombre_premiere_g_8 = models.CharField(max_length=255, null=True, verbose_name="Garçons 8 ans (1ère)") #
    st2_nombre_premiere_g_9 = models.CharField(max_length=255, null=True, verbose_name="Garçons 9 ans (1ère)") #
    
    # Garçons - Groupes spécifiques
    st2_nombre_premiere_g_dont_autochtone = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Autochtones (1ère)") #
    st2_nombre_premiere_g_dont_avec_handicap = models.CharField(max_length=255, null=True, verbose_name="Garçons dont avec Handicap (1ère)") #
    st2_nombre_premiere_g_dont_deplaces = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Déplacés (1ère)") #
    st2_nombre_premiere_g_dont_etrangers = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Étrangers (1ère)") #
    st2_nombre_premiere_g_dont_internants = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Internants (1ère)") #
    st2_nombre_premiere_g_dont_orphelins = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Orphelins (1ère)") #
    st2_nombre_premiere_g_dont_redoublons = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Redoublants (1ère)") #
    st2_nombre_premiere_g_dont_refugies = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Réfugiés (1ère)") #
    st2_nombre_premiere_g_dont_reintegrants = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Réintégrants (1ère)") #
    st2_nombre_premiere_g_moins6 = models.CharField(max_length=255, null=True, verbose_name="Garçons < 6 ans (1ère)") #
    st2_nombre_premiere_g_plus11 = models.CharField(max_length=255, null=True, verbose_name="Garçons > 11 ans (1ère)") #

    def __str__(self):
        return f"Effectifs 1ère année ST2 (ID: {self.id})"

    class Meta:
        verbose_name = "Effectif Élève 1ère ST2"
        verbose_name_plural = "Effectifs Élèves 1ère ST2"

class St2_effectifs_eleve_preprimaaire(models.Model):
    # 1. form_st_id (bigint(20), Oui)
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 2. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 3-30. Champs d'effectifs (varchar(255), Oui)

    # Filles - Répartition par âge (3 à 5 ans)
    st2_nombre_preprimaire_f_3ans = models.CharField(max_length=255, null=True, verbose_name="Filles 3 ans")
    st2_nombre_preprimaire_f_4ans = models.CharField(max_length=255, null=True, verbose_name="Filles 4 ans")
    st2_nombre_preprimaire_f_5ans = models.CharField(max_length=255, null=True, verbose_name="Filles 5 ans")
    
    # Filles - Groupes spéciaux
    st2_nombre_preprimaire_f_moins3ans = models.CharField(max_length=255, null=True, verbose_name="Filles moins de 3 ans")
    st2_nombre_preprimaire_f_plus5ans = models.CharField(max_length=255, null=True, verbose_name="Filles plus de 5 ans")

    # Garçons - Répartition par âge (3 à 5 ans)
    st2_nombre_preprimaire_g_3ans = models.CharField(max_length=255, null=True, verbose_name="Garçons 3 ans")
    st2_nombre_preprimaire_g_4ans = models.CharField(max_length=255, null=True, verbose_name="Garçons 4 ans")
    st2_nombre_preprimaire_g_5ans = models.CharField(max_length=255, null=True, verbose_name="Garçons 5 ans")

    # Garçons - Groupes spéciaux
    st2_nombre_preprimaire_g_moins3ans = models.CharField(max_length=255, null=True, verbose_name="Garçons moins de 3 ans")
    st2_nombre_preprimaire_g_plus5ans = models.CharField(max_length=255, null=True, verbose_name="Garçons plus de 5 ans")
    
    # Les autres champs que vous avez pu avoir dans l'image précédente qui n'a pas chargé entièrement :
    # Ces champs sont basés sur le modèle St1_groupes_specifiques et sont inclus ici pour être complet :

    st2_nombre_preprimaire_f_dont_autochtone = models.CharField(max_length=255, null=True, verbose_name="Filles dont Autochtones")
    st2_nombre_preprimaire_f_dont_avec_handicap = models.CharField(max_length=255, null=True, verbose_name="Filles dont avec Handicap")
    st2_nombre_preprimaire_f_dont_deplaces = models.CharField(max_length=255, null=True, verbose_name="Filles dont Déplacés")
    st2_nombre_preprimaire_f_dont_etrangers = models.CharField(max_length=255, null=True, verbose_name="Filles dont Étrangers")
    st2_nombre_preprimaire_f_dont_internants = models.CharField(max_length=255, null=True, verbose_name="Filles dont Internants")
    st2_nombre_preprimaire_f_dont_orphelins = models.CharField(max_length=255, null=True, verbose_name="Filles dont Orphelins")
    st2_nombre_preprimaire_f_dont_redoublons = models.CharField(max_length=255, null=True, verbose_name="Filles dont Redoublants")
    st2_nombre_preprimaire_f_dont_refugies = models.CharField(max_length=255, null=True, verbose_name="Filles dont Réfugiés")
    st2_nombre_preprimaire_f_dont_reintegrants = models.CharField(max_length=255, null=True, verbose_name="Filles dont Réintégrants")

    st2_nombre_preprimaire_g_dont_autochtone = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Autochtones")
    st2_nombre_preprimaire_g_dont_avec_handicap = models.CharField(max_length=255, null=True, verbose_name="Garçons dont avec Handicap")
    st2_nombre_preprimaire_g_dont_deplaces = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Déplacés")
    st2_nombre_preprimaire_g_dont_etrangers = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Étrangers")
    st2_nombre_preprimaire_g_dont_internants = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Internants")
    st2_nombre_preprimaire_g_dont_orphelins = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Orphelins")
    st2_nombre_preprimaire_g_dont_redoublons = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Redoublants")
    st2_nombre_preprimaire_g_dont_refugies = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Réfugiés")
    st2_nombre_preprimaire_g_dont_reintegrants = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Réintégrants")


    def __str__(self):
        return f"Effectifs Pré-Primaire ST2 (ID: {self.id})"

    class Meta:
        verbose_name = "Effectif Élève Pré-Primaire ST2"
        verbose_name_plural = "Effectifs Élèves Pré-Primaire ST2"

class St2_effectifs_eleve_quatrieme(models.Model):
    # 1. form_st_id (bigint(20), Oui)
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 2. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 3-32. Champs d'effectifs (varchar(255), Oui)

    # Filles - Répartition par âge (7 à plus de 11 ans)
    st2_nombre_quatrieme_f_10 = models.CharField(max_length=255, null=True, verbose_name="Filles 10 ans (4ème)")
    st2_nombre_quatrieme_f_11 = models.CharField(max_length=255, null=True, verbose_name="Filles 11 ans (4ème)")
    st2_nombre_quatrieme_f_7 = models.CharField(max_length=255, null=True, verbose_name="Filles 7 ans (4ème)")
    st2_nombre_quatrieme_f_8 = models.CharField(max_length=255, null=True, verbose_name="Filles 8 ans (4ème)")
    st2_nombre_quatrieme_f_9 = models.CharField(max_length=255, null=True, verbose_name="Filles 9 ans (4ème)")
    
    # Filles - Groupes spécifiques
    st2_nombre_quatrieme_f_dont_autochtone = models.CharField(max_length=255, null=True, verbose_name="Filles dont Autochtones (4ème)")
    st2_nombre_quatrieme_f_dont_avec_handicap = models.CharField(max_length=255, null=True, verbose_name="Filles dont avec Handicap (4ème)")
    st2_nombre_quatrieme_f_dont_deplaces = models.CharField(max_length=255, null=True, verbose_name="Filles dont Déplacés (4ème)")
    st2_nombre_quatrieme_f_dont_etrangers = models.CharField(max_length=255, null=True, verbose_name="Filles dont Étrangers (4ème)")
    st2_nombre_quatrieme_f_dont_internants = models.CharField(max_length=255, null=True, verbose_name="Filles dont Internants (4ème)")
    st2_nombre_quatrieme_f_dont_orphelins = models.CharField(max_length=255, null=True, verbose_name="Filles dont Orphelins (4ème)")
    st2_nombre_quatrieme_f_dont_redoublons = models.CharField(max_length=255, null=True, verbose_name="Filles dont Redoublants (4ème)")
    st2_nombre_quatrieme_f_dont_refugies = models.CharField(max_length=255, null=True, verbose_name="Filles dont Réfugiés (4ème)")
    st2_nombre_quatrieme_f_dont_reintegrants = models.CharField(max_length=255, null=True, verbose_name="Filles dont Réintégrants (4ème)")
    st2_nombre_quatrieme_f_plus11 = models.CharField(max_length=255, null=True, verbose_name="Filles > 11 ans (4ème)")

    # Garçons - Répartition par âge (7 à plus de 11 ans)
    st2_nombre_quatrieme_g_10 = models.CharField(max_length=255, null=True, verbose_name="Garçons 10 ans (4ème)")
    st2_nombre_quatrieme_g_11 = models.CharField(max_length=255, null=True, verbose_name="Garçons 11 ans (4ème)")
    st2_nombre_quatrieme_g_7 = models.CharField(max_length=255, null=True, verbose_name="Garçons 7 ans (4ème)")
    st2_nombre_quatrieme_g_8 = models.CharField(max_length=255, null=True, verbose_name="Garçons 8 ans (4ème)")
    st2_nombre_quatrieme_g_9 = models.CharField(max_length=255, null=True, verbose_name="Garçons 9 ans (4ème)")
    
    # Garçons - Groupes spécifiques
    st2_nombre_quatrieme_g_dont_autochtone = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Autochtones (4ème)")
    st2_nombre_quatrieme_g_dont_avec_handicap = models.CharField(max_length=255, null=True, verbose_name="Garçons dont avec Handicap (4ème)")
    st2_nombre_quatrieme_g_dont_deplaces = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Déplacés (4ème)")
    st2_nombre_quatrieme_g_dont_etrangers = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Étrangers (4ème)")
    st2_nombre_quatrieme_g_dont_internants = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Internants (4ème)")
    st2_nombre_quatrieme_g_dont_orphelins = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Orphelins (4ème)")
    st2_nombre_quatrieme_g_dont_redoublons = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Redoublants (4ème)")
    st2_nombre_quatrieme_g_dont_refugies = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Réfugiés (4ème)")
    st2_nombre_quatrieme_g_dont_reintegrants = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Réintégrants (4ème)")
    st2_nombre_quatrieme_g_plus11 = models.CharField(max_length=255, null=True, verbose_name="Garçons > 11 ans (4ème)")


    def __str__(self):
        return f"Effectifs 4ème année ST2 (ID: {self.id})"

    class Meta:
        verbose_name = "Effectif Élève 4ème ST2"
        verbose_name_plural = "Effectifs Élèves 4ème ST2"

class St2_effectifs_eleve_sixieme(models.Model):
    # 1. form_st_id (bigint(20), Oui)
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 2. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 3-28. Champs d'effectifs (varchar(255), Oui)

    # Filles - Répartition par âge (9 à plus de 11 ans)
    st2_nombre_sixieme_f_10 = models.CharField(max_length=255, null=True, verbose_name="Filles 10 ans (6ème)")
    st2_nombre_sixieme_f_11 = models.CharField(max_length=255, null=True, verbose_name="Filles 11 ans (6ème)")
    st2_nombre_sixieme_f_9 = models.CharField(max_length=255, null=True, verbose_name="Filles 9 ans (6ème)")
    
    # Filles - Groupes spécifiques
    st2_nombre_sixieme_f_dont_autochtone = models.CharField(max_length=255, null=True, verbose_name="Filles dont Autochtones (6ème)")
    st2_nombre_sixieme_f_dont_avec_handicap = models.CharField(max_length=255, null=True, verbose_name="Filles dont avec Handicap (6ème)")
    st2_nombre_sixieme_f_dont_deplaces = models.CharField(max_length=255, null=True, verbose_name="Filles dont Déplacés (6ème)")
    st2_nombre_sixieme_f_dont_etrangers = models.CharField(max_length=255, null=True, verbose_name="Filles dont Étrangers (6ème)")
    st2_nombre_sixieme_f_dont_internants = models.CharField(max_length=255, null=True, verbose_name="Filles dont Internants (6ème)")
    st2_nombre_sixieme_f_dont_orphelins = models.CharField(max_length=255, null=True, verbose_name="Filles dont Orphelins (6ème)")
    st2_nombre_sixieme_f_dont_redoublons = models.CharField(max_length=255, null=True, verbose_name="Filles dont Redoublants (6ème)")
    st2_nombre_sixieme_f_dont_refugies = models.CharField(max_length=255, null=True, verbose_name="Filles dont Réfugiés (6ème)")
    st2_nombre_sixieme_f_dont_reintegrants = models.CharField(max_length=255, null=True, verbose_name="Filles dont Réintégrants (6ème)")
    st2_nombre_sixieme_f_plus11 = models.CharField(max_length=255, null=True, verbose_name="Filles > 11 ans (6ème)")

    # Garçons - Répartition par âge (9 à plus de 11 ans)
    st2_nombre_sixieme_g_10 = models.CharField(max_length=255, null=True, verbose_name="Garçons 10 ans (6ème)")
    st2_nombre_sixieme_g_11 = models.CharField(max_length=255, null=True, verbose_name="Garçons 11 ans (6ème)")
    st2_nombre_sixieme_g_9 = models.CharField(max_length=255, null=True, verbose_name="Garçons 9 ans (6ème)")
    
    # Garçons - Groupes spécifiques
    st2_nombre_sixieme_g_dont_autochtone = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Autochtones (6ème)")
    st2_nombre_sixieme_g_dont_avec_handicap = models.CharField(max_length=255, null=True, verbose_name="Garçons dont avec Handicap (6ème)")
    st2_nombre_sixieme_g_dont_deplaces = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Déplacés (6ème)")
    st2_nombre_sixieme_g_dont_etrangers = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Étrangers (6ème)")
    st2_nombre_sixieme_g_dont_internants = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Internants (6ème)")
    st2_nombre_sixieme_g_dont_orphelins = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Orphelins (6ème)")
    st2_nombre_sixieme_g_dont_redoublons = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Redoublants (6ème)")
    st2_nombre_sixieme_g_dont_refugies = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Réfugiés (6ème)")
    st2_nombre_sixieme_g_dont_reintegrants = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Réintégrants (6ème)")
    st2_nombre_sixieme_g_plus11 = models.CharField(max_length=255, null=True, verbose_name="Garçons > 11 ans (6ème)")

    def __str__(self):
        return f"Effectifs 6ème année ST2 (ID: {self.id})"

    class Meta:
        verbose_name = "Effectif Élève 6ème ST2"
        verbose_name_plural = "Effectifs Élèves 6ème ST2"

class St2_effectifs_eleve_troisieme(models.Model):
    # 1. form_st_id (bigint(20), Oui)
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 2. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 3-36. Champs d'effectifs (varchar(255), Oui)

    # Filles - Répartition par âge (6 à plus de 11 ans)
    st2_nombre_troisieme_f_6 = models.CharField(max_length=255, null=True, verbose_name="Filles 6 ans (3ème)")
    st2_nombre_troisieme_f_7 = models.CharField(max_length=255, null=True, verbose_name="Filles 7 ans (3ème)")
    st2_nombre_troisieme_f_8 = models.CharField(max_length=255, null=True, verbose_name="Filles 8 ans (3ème)")
    st2_nombre_troisieme_f_9 = models.CharField(max_length=255, null=True, verbose_name="Filles 9 ans (3ème)")
    st2_nombre_troisieme_f_10 = models.CharField(max_length=255, null=True, verbose_name="Filles 10 ans (3ème)")
    st2_nombre_troisieme_f_11 = models.CharField(max_length=255, null=True, verbose_name="Filles 11 ans (3ème)")

    # Filles - Groupes spéciaux et âges extrêmes
    st2_nombre_troisieme_f_dont_autochtone = models.CharField(max_length=255, null=True, verbose_name="Filles dont Autochtones (3ème)")
    st2_nombre_troisieme_f_dont_avec_handicap = models.CharField(max_length=255, null=True, verbose_name="Filles dont avec Handicap (3ème)")
    st2_nombre_troisieme_f_dont_deplaces = models.CharField(max_length=255, null=True, verbose_name="Filles dont Déplacés (3ème)")
    st2_nombre_troisieme_f_dont_etrangers = models.CharField(max_length=255, null=True, verbose_name="Filles dont Étrangers (3ème)")
    st2_nombre_troisieme_f_dont_internants = models.CharField(max_length=255, null=True, verbose_name="Filles dont Internants (3ème)")
    st2_nombre_troisieme_f_dont_orphelins = models.CharField(max_length=255, null=True, verbose_name="Filles dont Orphelins (3ème)")
    st2_nombre_troisieme_f_dont_redoublons = models.CharField(max_length=255, null=True, verbose_name="Filles dont Redoublants (3ème)")
    st2_nombre_troisieme_f_dont_refugies = models.CharField(max_length=255, null=True, verbose_name="Filles dont Réfugiés (3ème)")
    st2_nombre_troisieme_f_dont_reintegrants = models.CharField(max_length=255, null=True, verbose_name="Filles dont Réintégrants (3ème)")
    st2_nombre_troisieme_f_moins6 = models.CharField(max_length=255, null=True, verbose_name="Filles < 6 ans (3ème)")
    st2_nombre_troisieme_f_plus11 = models.CharField(max_length=255, null=True, verbose_name="Filles > 11 ans (3ème)")

    # Garçons - Répartition par âge (6 à plus de 11 ans)
    st2_nombre_troisieme_g_6 = models.CharField(max_length=255, null=True, verbose_name="Garçons 6 ans (3ème)")
    st2_nombre_troisieme_g_7 = models.CharField(max_length=255, null=True, verbose_name="Garçons 7 ans (3ème)")
    st2_nombre_troisieme_g_8 = models.CharField(max_length=255, null=True, verbose_name="Garçons 8 ans (3ème)")
    st2_nombre_troisieme_g_9 = models.CharField(max_length=255, null=True, verbose_name="Garçons 9 ans (3ème)")
    st2_nombre_troisieme_g_10 = models.CharField(max_length=255, null=True, verbose_name="Garçons 10 ans (3ème)")
    st2_nombre_troisieme_g_11 = models.CharField(max_length=255, null=True, verbose_name="Garçons 11 ans (3ème)")

    # Garçons - Groupes spéciaux et âges extrêmes
    st2_nombre_troisieme_g_dont_autochtone = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Autochtones (3ème)")
    st2_nombre_troisieme_g_dont_avec_handicap = models.CharField(max_length=255, null=True, verbose_name="Garçons dont avec Handicap (3ème)")
    st2_nombre_troisieme_g_dont_deplaces = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Déplacés (3ème)")
    st2_nombre_troisieme_g_dont_etrangers = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Étrangers (3ème)")
    st2_nombre_troisieme_g_dont_internants = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Internants (3ème)")
    st2_nombre_troisieme_g_dont_orphelins = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Orphelins (3ème)")
    st2_nombre_troisieme_g_dont_redoublons = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Redoublants (3ème)")
    st2_nombre_troisieme_g_dont_refugies = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Réfugiés (3ème)")
    st2_nombre_troisieme_g_dont_reintegrants = models.CharField(max_length=255, null=True, verbose_name="Garçons dont Réintégrants (3ème)")
    st2_nombre_troisieme_g_moins6 = models.CharField(max_length=255, null=True, verbose_name="Garçons < 6 ans (3ème)")
    st2_nombre_troisieme_g_plus11 = models.CharField(max_length=255, null=True, verbose_name="Garçons > 11 ans (3ème)")


    def __str__(self):
        return f"Effectifs 3ème année ST2 (ID: {self.id})"

    class Meta:
        verbose_name = "Effectif Élève 3ème ST2"
        verbose_name_plural = "Effectifs Élèves 3ème ST2"

class St2_environnement_et_developpement(models.Model):
    # 1. form_st_id (bigint(20), Oui)
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    ) #

    # 2. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 3-17. Champs de données (varchar(255), Oui)
    st2_activites_parascolaires = models.CharField(max_length=255, null=True, verbose_name="Activités parascolaires") #
    st2_coíns_dechets = models.CharField(max_length=255, null=True, verbose_name="Coins/aires de déchets") #
    st2_dispose_arbres = models.CharField(max_length=255, null=True, verbose_name="Dispose d'arbres/espaces verts") #
    st2_enseignants_formes_genre = models.CharField(max_length=255, null=True, verbose_name="Enseignants formés genre") #
    st2_enseignants_formes_premiers_soins = models.CharField(max_length=255, null=True, verbose_name="Enseignants formés premiers soins") #
    st2_etablissement_locaux_directeurs_rid = models.CharField(max_length=255, null=True, verbose_name="Établissement, locaux, directeurs, RID") #
    st2_femmes_enseignantes_recrutees = models.CharField(max_length=255, null=True, verbose_name="Femmes enseignantes recrutées") #
    st2_gouvernement_eleves = models.CharField(max_length=255, null=True, verbose_name="Gouvernement des élèves") #
    st2_manuel_procedure = models.CharField(max_length=255, null=True, verbose_name="Manuel de procédure/règlement") #
    st2_nombre_arbres_plantes = models.CharField(max_length=255, null=True, verbose_name="Nombre d'arbres plantés") #
    st2_participation_rep = models.CharField(max_length=255, null=True, verbose_name="Participation aux réunions/décisions REP") #
    st2_plan_communication = models.CharField(max_length=255, null=True, verbose_name="Plan de communication") #
    st2_pv_eleves = models.CharField(max_length=255, null=True, verbose_name="Procès-verbaux des élèves") #
    st2_reseaux_locaux_directeurs = models.CharField(max_length=255, null=True, verbose_name="Réseaux locaux des directeurs") #
    st2_unite_pedagogique = models.CharField(max_length=255, null=True, verbose_name="Unité pédagogique") #

    def __str__(self):
        return f"Environnement & Développement ST2 (ID: {self.id})"

    class Meta:
        verbose_name = "Environnement et Développement ST2"
        verbose_name_plural = "Environnement et Développement ST2"

class St2_equipements_ateliers_ou_laboratoires(models.Model):
    # 1. form_st_id (bigint(20), Oui)
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 2. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 3-6. Champs d'équipements (varchar(255), Oui)
    st2_NomEquipement = models.CharField(max_length=255, null=True, verbose_name="Nom de l'équipement")
    st2_NombreEquipementsMauvais = models.CharField(max_length=255, null=True, verbose_name="Nombre d'équipements en mauvais état")
    st2_NombreEquipementsBon = models.CharField(max_length=255, null=True, verbose_name="Nombre d'équipements en bon état")
    st2_TypeAtelierOuLabo = models.CharField(max_length=255, null=True, verbose_name="Type d'atelier ou laboratoire")

    def __str__(self):
        return f"Équipements, Ateliers ou Labos ST2 (ID: {self.id})"

    class Meta:
        verbose_name = "Équipements Ateliers Labos ST2"
        verbose_name_plural = "Équipements Ateliers Labos ST2"

class St2_etat_des_locaux(models.Model):
    # 1. form_st_id (bigint(20), Oui)
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 2. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 3-42. Champs des locaux (varchar(255), Oui)

    # Latrines
    locaux_latrine_dur_bon = models.CharField(max_length=255, null=True, verbose_name="Latrine Dur Bon") #
    locaux_latrine_paille_feuillage_mauvais = models.CharField(max_length=255, null=True, verbose_name="Latrine Paille Feuillage Mauvais") #
    locaux_latrine_semidur_bon = models.CharField(max_length=255, null=True, verbose_name="Latrine Semi-dur Bon") #
    locaux_latrine_semidur_mauvais = models.CharField(max_length=255, null=True, verbose_name="Latrine Semi-dur Mauvais") #
    locaux_latrine_terre_bon = models.CharField(max_length=255, null=True, verbose_name="Latrine Terre Bon") #
    locaux_latrine_terre_mauvais = models.CharField(max_length=255, null=True, verbose_name="Latrine Terre Mauvais") #

    # Magasins
    locaux_magasin_dur_bon = models.CharField(max_length=255, null=True, verbose_name="Magasin Dur Bon") #
    locaux_magasin_dur_mauvais = models.CharField(max_length=255, null=True, verbose_name="Magasin Dur Mauvais") #
    locaux_magasin_paille_feuillage_mauvais = models.CharField(max_length=255, null=True, verbose_name="Magasin Paille Feuillage Mauvais") #
    locaux_magasin_semidur_bon = models.CharField(max_length=255, null=True, verbose_name="Magasin Semi-dur Bon") #
    locaux_magasin_semidur_mauvais = models.CharField(max_length=255, null=True, verbose_name="Magasin Semi-dur Mauvais") #
    locaux_magasin_terre_bon = models.CharField(max_length=255, null=True, verbose_name="Magasin Terre Bon") #
    locaux_magasin_terre_mauvais = models.CharField(max_length=255, null=True, verbose_name="Magasin Terre Mauvais") #

    # Locaux/Salle de Bureau Administratif
    locaux_salle_bureau_administratif_dur_bon = models.CharField(max_length=255, null=True, verbose_name="Bureau Admin Dur Bon") #
    locaux_salle_bureau_administratif_paille_feuillage_mauvais = models.CharField(max_length=255, null=True, verbose_name="Bureau Admin Paille Feuillage Mauvais") #
    locaux_salle_bureau_administratif_semidur_mauvais = models.CharField(max_length=255, null=True, verbose_name="Bureau Admin Semi-dur Mauvais") #
    locaux_salle_bureau_administratif_terre_bon = models.CharField(max_length=255, null=True, verbose_name="Bureau Admin Terre Bon") #
    locaux_salle_bureau_administratif_terre_mauvais = models.CharField(max_length=255, null=True, verbose_name="Bureau Admin Terre Mauvais") #

    # Salles de Cours
    locaux_salle_de_cours_dur_bon = models.CharField(max_length=255, null=True, verbose_name="Salle Cours Dur Bon") #
    locaux_salle_de_cours_dur_mauvais = models.CharField(max_length=255, null=True, verbose_name="Salle Cours Dur Mauvais") #
    locaux_salle_de_cours_paille_feuillage_bon = models.CharField(max_length=255, null=True, verbose_name="Salle Cours Paille Feuillage Bon") #
    locaux_salle_de_cours_paille_feuillage_mauvais = models.CharField(max_length=255, null=True, verbose_name="Salle Cours Paille Feuillage Mauvais") #
    locaux_salle_de_cours_semidur_bon = models.CharField(max_length=255, null=True, verbose_name="Salle Cours Semi-dur Bon") #
    locaux_salle_de_cours_semidur_mauvais = models.CharField(max_length=255, null=True, verbose_name="Salle Cours Semi-dur Mauvais") #
    locaux_salle_de_cours_terre_bon = models.CharField(max_length=255, null=True, verbose_name="Salle Cours Terre Bon") #
    locaux_salle_de_cours_terre_mauvais = models.CharField(max_length=255, null=True, verbose_name="Salle Cours Terre Mauvais") #
    
    # Salles Spécialisées
    locaux_salle_specialisees_dur_bon = models.CharField(max_length=255, null=True, verbose_name="Salle Spécialisée Dur Bon") #
    locaux_salle_specialisees_dur_mauvais = models.CharField(max_length=255, null=True, verbose_name="Salle Spécialisée Dur Mauvais") #
    locaux_salle_specialisees_paille_feuillage_bon = models.CharField(max_length=255, null=True, verbose_name="Salle Spécialisée Paille Feuillage Bon") #
    locaux_salle_specialisees_paille_feuillage_mauvais = models.CharField(max_length=255, null=True, verbose_name="Salle Spécialisée Paille Feuillage Mauvais") #
    locaux_salle_specialisees_semidur_bon = models.CharField(max_length=255, null=True, verbose_name="Salle Spécialisée Semi-dur Bon") #
    locaux_salle_specialisees_semidur_mauvais = models.CharField(max_length=255, null=True, verbose_name="Salle Spécialisée Semi-dur Mauvais") #
    locaux_salle_specialisees_terre_bon = models.CharField(max_length=255, null=True, verbose_name="Salle Spécialisée Terre Bon") #
    locaux_salle_specialisees_terre_mauvais = models.CharField(max_length=255, null=True, verbose_name="Salle Spécialisée Terre Mauvais") #
    
    # (Note: Certains champs de l'image de St1_locaux semblent se chevaucher ou avoir été renommés/déplacés dans votre structure. J'ai utilisé l'image St2_etat_des_locaux fournie en dernier pour cette structure)

    def __str__(self):
        return f"État des Locaux ST2 (ID: {self.id})"

    class Meta:
        verbose_name = "État des Locaux ST2"
        verbose_name_plural = "État des Locaux ST2"

class St2_etat_des_locaux_specifiques(models.Model):
    # 1. form_st_id (bigint(20), Oui)
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 2. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 3-24. Champs des locaux spécifiques (varchar(255), Oui)

    # Locaux/Salles d'Activité
    locaux_activite_entole_bon = models.CharField(max_length=255, null=True, verbose_name="Activité Entôlé Bon")
    locaux_activite_entole_mauvais = models.CharField(max_length=255, null=True, verbose_name="Activité Entôlé Mauvais")
    locaux_activite_paille_feuillage_bon = models.CharField(max_length=255, null=True, verbose_name="Activité Paille/Feuillage Bon")
    locaux_activite_paille_feuillage_mauvais = models.CharField(max_length=255, null=True, verbose_name="Activité Paille/Feuillage Mauvais")

    # Locaux/Salles de Bureau
    locaux_bureau_entole_bon = models.CharField(max_length=255, null=True, verbose_name="Bureau Entôlé Bon")
    locaux_bureau_entole_mauvais = models.CharField(max_length=255, null=True, verbose_name="Bureau Entôlé Mauvais")
    locaux_bureau_paille_feuillage_bon = models.CharField(max_length=255, null=True, verbose_name="Bureau Paille/Feuillage Bon")
    locaux_bureau_paille_feuillage_mauvais = models.CharField(max_length=255, null=True, verbose_name="Bureau Paille/Feuillage Mauvais")

    # Locaux/Magasin
    locaux_magasin_entole_bon = models.CharField(max_length=255, null=True, verbose_name="Magasin Entôlé Bon")
    locaux_magasin_entole_mauvais = models.CharField(max_length=255, null=True, verbose_name="Magasin Entôlé Mauvais")
    locaux_magasin_paille_feuillage_bon = models.CharField(max_length=255, null=True, verbose_name="Magasin Paille/Feuillage Bon")
    locaux_magasin_paille_feuillage_mauvais = models.CharField(max_length=255, null=True, verbose_name="Magasin Paille/Feuillage Mauvais")

    # Locaux/Salle d'Attente
    locaux_salle_attente_paille_feuillage_bon = models.CharField(max_length=255, null=True, verbose_name="Salle Attente Paille/Feuillage Bon")
    locaux_salle_attente_paille_feuillage_mauvais = models.CharField(max_length=255, null=True, verbose_name="Salle Attente Paille/Feuillage Mauvais")
    
    # Locaux/Salles de Jeux/Sport
    locaux_salle_jeux_sport_entole_bon = models.CharField(max_length=255, null=True, verbose_name="Salle Jeux/Sport Entôlé Bon")
    locaux_salle_jeux_sport_entole_mauvais = models.CharField(max_length=255, null=True, verbose_name="Salle Jeux/Sport Entôlé Mauvais")
    locaux_salle_jeux_sport_paille_feuillage_bon = models.CharField(max_length=255, null=True, verbose_name="Salle Jeux/Sport Paille/Feuillage Bon")
    locaux_salle_jeux_sport_paille_feuillage_mauvais = models.CharField(max_length=255, null=True, verbose_name="Salle Jeux/Sport Paille/Feuillage Mauvais")
    
    # Locaux/Salles de Repos
    locaux_salle_repos_entole_bon = models.CharField(max_length=255, null=True, verbose_name="Salle Repos Entôlé Bon")
    locaux_salle_repos_entole_mauvais = models.CharField(max_length=255, null=True, verbose_name="Salle Repos Entôlé Mauvais")
    locaux_salle_repos_paille_feuillage_bon = models.CharField(max_length=255, null=True, verbose_name="Salle Repos Paille/Feuillage Bon")
    locaux_salle_repos_paille_feuillage_mauvais = models.CharField(max_length=255, null=True, verbose_name="Salle Repos Paille/Feuillage Mauvais")

    def __str__(self):
        return f"État des Locaux Spécifiques ST2 (ID: {self.id})"

    class Meta:
        verbose_name = "État des Locaux Spécifiques ST2"
        verbose_name_plural = "État des Locaux Spécifiques ST2"

class St2_guides_pedagogiques_disponibles(models.Model):
    # 1. form_st_id (bigint(20), Oui)
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 2. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 3-51. Champs des guides (varchar(255), Oui)

    # Guides 'autres' (manuel, 4eme, 5eme, 6eme, Pre-primaire)
    guide_autres_manuel = models.CharField(max_length=255, null=True, verbose_name="Autres Guides - Manuel") #
    guide_autres_4eme = models.CharField(max_length=255, null=True, verbose_name="Autres Guides - 4ème") #
    guide_autres_5eme = models.CharField(max_length=255, null=True, verbose_name="Autres Guides - 5ème") #
    guide_autres_6eme = models.CharField(max_length=255, null=True, verbose_name="Autres Guides - 6ème") #
    guide_autres_pre_primaire = models.CharField(max_length=255, null=True, verbose_name="Autres Guides - Pré-Primaire") #

    # Guides 'éducation civique, morale, paix' (2eme, 3eme, 4eme, 5eme)
    guide_education_civique_morale_2eme = models.CharField(max_length=255, null=True, verbose_name="Éduc. Civique/Morale - 2ème") #
    guide_education_civique_morale_3eme = models.CharField(max_length=255, null=True, verbose_name="Éduc. Civique/Morale - 3ème") #
    guide_education_civique_morale_4eme = models.CharField(max_length=255, null=True, verbose_name="Éduc. Civique/Morale - 4ème") #
    guide_education_civique_morale_5eme = models.CharField(max_length=255, null=True, verbose_name="Éduc. Civique/Morale - 5ème") #
    guide_education_pour_la_paix_2eme = models.CharField(max_length=255, null=True, verbose_name="Éduc. pour la Paix - 2ème") #
    guide_education_pour_la_paix_3eme = models.CharField(max_length=255, null=True, verbose_name="Éduc. pour la Paix - 3ème") #
    guide_education_pour_la_paix_4eme = models.CharField(max_length=255, null=True, verbose_name="Éduc. pour la Paix - 4ème") #
    guide_education_pour_la_paix_5eme = models.CharField(max_length=255, null=True, verbose_name="Éduc. pour la Paix - 5ème") #

    # Guides 'éveil' (2eme, 3eme, 4eme, 5eme, pre-primaire)
    guide_eveil_2eme = models.CharField(max_length=255, null=True, verbose_name="Éveil - 2ème") #
    guide_eveil_3eme = models.CharField(max_length=255, null=True, verbose_name="Éveil - 3ème") #
    guide_eveil_4eme = models.CharField(max_length=255, null=True, verbose_name="Éveil - 4ème") #
    guide_eveil_5eme = models.CharField(max_length=255, null=True, verbose_name="Éveil - 5ème") #
    guide_eveil_pre_primaire = models.CharField(max_length=255, null=True, verbose_name="Éveil - Pré-Primaire") #

    # Guides 'français' (2eme, 3eme, 4eme, 5eme, 6eme, pre-primaire)
    guide_francais_2eme = models.CharField(max_length=255, null=True, verbose_name="Français - 2ème") #
    guide_francais_3eme = models.CharField(max_length=255, null=True, verbose_name="Français - 3ème") #
    guide_francais_4eme = models.CharField(max_length=255, null=True, verbose_name="Français - 4ème") #
    guide_francais_5eme = models.CharField(max_length=255, null=True, verbose_name="Français - 5ème") #
    guide_francais_6eme = models.CharField(max_length=255, null=True, verbose_name="Français - 6ème") #
    guide_francais_pre_primaire = models.CharField(max_length=255, null=True, verbose_name="Français - Pré-Primaire") #

    # Guides 'mathématiques' (2eme, 3eme, 4eme, 5eme, 6eme, pre-primaire)
    guide_mathematique_2eme = models.CharField(max_length=255, null=True, verbose_name="Mathématiques - 2ème") #
    guide_mathematique_3eme = models.CharField(max_length=255, null=True, verbose_name="Mathématiques - 3ème") #
    guide_mathematique_4eme = models.CharField(max_length=255, null=True, verbose_name="Mathématiques - 4ème") #
    guide_mathematique_5eme = models.CharField(max_length=255, null=True, verbose_name="Mathématiques - 5ème") #
    guide_mathematique_6eme = models.CharField(max_length=255, null=True, verbose_name="Mathématiques - 6ème") #
    guide_mathematique_pre_primaire = models.CharField(max_length=255, null=True, verbose_name="Mathématiques - Pré-Primaire") #

    # Guides 'thèmes transversaux' (2eme, 3eme, 4eme, 5eme, pre-primaire)
    guide_themes_transversaux_2eme = models.CharField(max_length=255, null=True, verbose_name="Thèmes Transversaux - 2ème") #
    guide_themes_transversaux_3eme = models.CharField(max_length=255, null=True, verbose_name="Thèmes Transversaux - 3ème") #
    guide_themes_transversaux_4eme = models.CharField(max_length=255, null=True, verbose_name="Thèmes Transversaux - 4ème") #
    guide_themes_transversaux_5eme = models.CharField(max_length=255, null=True, verbose_name="Thèmes Transversaux - 5ème") #
    guide_themes_transversaux_pre_primaire = models.CharField(max_length=255, null=True, verbose_name="Thèmes Transversaux - Pré-Primaire") #

    def __str__(self):
        return f"Guides Pédagogiques Disponibles ST2 (ID: {self.id})"

    class Meta:
        verbose_name = "Guides Pédagogiques ST2"
        verbose_name_plural = "Guides Pédagogiques ST2"

class St2_manuels_disponibles(models.Model):
    # 1. form_st_id (bigint(20), Oui)
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 2. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 3-50. Champs des manuels (varchar(255), Oui)

    # Manuels 'autres' (manuel, 4eme, 5eme, 6eme)
    manuels_autres_manuel = models.CharField(max_length=255, null=True, verbose_name="Autres Manuels - Manuel") #
    manuels_autres_4eme = models.CharField(max_length=255, null=True, verbose_name="Autres Manuels - 4ème") #
    manuels_autres_5eme = models.CharField(max_length=255, null=True, verbose_name="Autres Manuels - 5ème") #
    manuels_autres_6eme = models.CharField(max_length=255, null=True, verbose_name="Autres Manuels - 6ème") #

    # Manuels 'éducation civique, morale, paix' (1ere à 5eme, pre-primaire)
    manuels_education_civique_morale_1ere = models.CharField(max_length=255, null=True, verbose_name="Éduc. Civique/Morale - 1ère") #
    manuels_education_civique_morale_2eme = models.CharField(max_length=255, null=True, verbose_name="Éduc. Civique/Morale - 2ème") #
    manuels_education_civique_morale_3eme = models.CharField(max_length=255, null=True, verbose_name="Éduc. Civique/Morale - 3ème") #
    manuels_education_civique_morale_4eme = models.CharField(max_length=255, null=True, verbose_name="Éduc. Civique/Morale - 4ème") #
    manuels_education_civique_morale_5eme = models.CharField(max_length=255, null=True, verbose_name="Éduc. Civique/Morale - 5ème") #
    manuels_education_civique_morale_pre_primaire = models.CharField(max_length=255, null=True, verbose_name="Éduc. Civique/Morale - Pré-Primaire") #
    manuels_education_pour_la_paix_1ere = models.CharField(max_length=255, null=True, verbose_name="Éduc. pour la Paix - 1ère") #
    manuels_education_pour_la_paix_2eme = models.CharField(max_length=255, null=True, verbose_name="Éduc. pour la Paix - 2ème") #
    manuels_education_pour_la_paix_3eme = models.CharField(max_length=255, null=True, verbose_name="Éduc. pour la Paix - 3ème") #
    manuels_education_pour_la_paix_4eme = models.CharField(max_length=255, null=True, verbose_name="Éduc. pour la Paix - 4ème") #
    manuels_education_pour_la_paix_5eme = models.CharField(max_length=255, null=True, verbose_name="Éduc. pour la Paix - 5ème") #
    manuels_education_pour_la_paix_pre_primaire = models.CharField(max_length=255, null=True, verbose_name="Éduc. pour la Paix - Pré-Primaire") #

    # Manuels 'éveil' (1ere à 4eme, pre-primaire)
    manuels_eveil_1ere = models.CharField(max_length=255, null=True, verbose_name="Éveil - 1ère") #
    manuels_eveil_2eme = models.CharField(max_length=255, null=True, verbose_name="Éveil - 2ème") #
    manuels_eveil_3eme = models.CharField(max_length=255, null=True, verbose_name="Éveil - 3ème") #
    manuels_eveil_4eme = models.CharField(max_length=255, null=True, verbose_name="Éveil - 4ème") #
    manuels_eveil_pre_primaire = models.CharField(max_length=255, null=True, verbose_name="Éveil - Pré-Primaire") #

    # Manuels 'français' (1ere à 6eme, pre-primaire)
    manuels_francais_1ere = models.CharField(max_length=255, null=True, verbose_name="Français - 1ère") #
    manuels_francais_2eme = models.CharField(max_length=255, null=True, verbose_name="Français - 2ème") #
    manuels_francais_3eme = models.CharField(max_length=255, null=True, verbose_name="Français - 3ème") #
    manuels_francais_4eme = models.CharField(max_length=255, null=True, verbose_name="Français - 4ème") #
    manuels_francais_5eme = models.CharField(max_length=255, null=True, verbose_name="Français - 5ème") #
    manuels_francais_6eme = models.CharField(max_length=255, null=True, verbose_name="Français - 6ème") #
    manuels_francais_pre_primaire = models.CharField(max_length=255, null=True, verbose_name="Français - Pré-Primaire") #

    # Manuels 'mathématiques' (1ere à 6eme, pre-primaire)
    manuels_mathematique_1ere = models.CharField(max_length=255, null=True, verbose_name="Mathématiques - 1ère") #
    manuels_mathematique_2eme = models.CharField(max_length=255, null=True, verbose_name="Mathématiques - 2ème") #
    manuels_mathematique_3eme = models.CharField(max_length=255, null=True, verbose_name="Mathématiques - 3ème") #
    manuels_mathematique_4eme = models.CharField(max_length=255, null=True, verbose_name="Mathématiques - 4ème") #
    manuels_mathematique_5eme = models.CharField(max_length=255, null=True, verbose_name="Mathématiques - 5ème") #
    manuels_mathematique_6eme = models.CharField(max_length=255, null=True, verbose_name="Mathématiques - 6ème") #
    manuels_mathematique_pre_primaire = models.CharField(max_length=255, null=True, verbose_name="Mathématiques - Pré-Primaire") #

    # Manuels 'thèmes transversaux' (1ere à 5eme, pre-primaire)
    manuels_themes_transversaux_1ere = models.CharField(max_length=255, null=True, verbose_name="Thèmes Transversaux - 1ère") #
    manuels_themes_transversaux_2eme = models.CharField(max_length=255, null=True, verbose_name="Thèmes Transversaux - 2ème") #
    manuels_themes_transversaux_3eme = models.CharField(max_length=255, null=True, verbose_name="Thèmes Transversaux - 3ème") #
    manuels_themes_transversaux_4eme = models.CharField(max_length=255, null=True, verbose_name="Thèmes Transversaux - 4ème") #
    manuels_themes_transversaux_5eme = models.CharField(max_length=255, null=True, verbose_name="Thèmes Transversaux - 5ème") #
    manuels_themes_transversaux_pre_primaire = models.CharField(max_length=255, null=True, verbose_name="Thèmes Transversaux - Pré-Primaire") #

    def __str__(self):
        return f"Manuels Disponibles ST2 (ID: {self.id})"

    class Meta:
        verbose_name = "Manuels Disponibles ST2"
        verbose_name_plural = "Manuels Disponibles ST2"

class St2_personnel_administratif_et_ouvrier(models.Model):
    # 1. form_st_id (bigint(20), Oui)
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 2. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 3-50. Champs du personnel (varchar(255), Oui)

    # Statut 'autres'
    autres_directeur_adjoint_f = models.CharField(max_length=255, null=True, verbose_name="Autres Dir. Adj. F")
    autres_directeur_f = models.CharField(max_length=255, null=True, verbose_name="Autres Directeur F")
    autres_directeur_h = models.CharField(max_length=255, null=True, verbose_name="Autres Directeur H")
    autres_ouvrier_autre_f = models.CharField(max_length=255, null=True, verbose_name="Autres Ouvrier Autre F")
    autres_ouvrier_autre_h = models.CharField(max_length=255, null=True, verbose_name="Autres Ouvrier Autre H")
    autres_surveillant_f = models.CharField(max_length=255, null=True, verbose_name="Autres Surveillant F")
    autres_surveillant_h = models.CharField(max_length=255, null=True, verbose_name="Autres Surveillant H")
    
    # Statut 'admin' (Administration - personnel autre que DID, MOI, PD)
    admin_directeur_adjoint_f = models.CharField(max_length=255, null=True, verbose_name="Admin Dir. Adj. F")
    admin_directeur_adjoint_h = models.CharField(max_length=255, null=True, verbose_name="Admin Dir. Adj. H")
    admin_directeur_f = models.CharField(max_length=255, null=True, verbose_name="Admin Directeur F")
    admin_directeur_h = models.CharField(max_length=255, null=True, verbose_name="Admin Directeur H")
    admin_ouvrier_autre_f = models.CharField(max_length=255, null=True, verbose_name="Admin Ouvrier Autre F")
    admin_ouvrier_autre_h = models.CharField(max_length=255, null=True, verbose_name="Admin Ouvrier Autre H")
    admin_surveillant_f = models.CharField(max_length=255, null=True, verbose_name="Admin Surveillant F")
    admin_surveillant_h = models.CharField(max_length=255, null=True, verbose_name="Admin Surveillant H")

    # Statut 'admin_did' (Administration - Directeurs/Inspecteurs de District)
    admin_did_directeur_adjoint_f = models.CharField(max_length=255, null=True, verbose_name="Admin DID Dir. Adj. F")
    admin_did_directeur_adjoint_h = models.CharField(max_length=255, null=True, verbose_name="Admin DID Dir. Adj. H")
    admin_did_directeur_f = models.CharField(max_length=255, null=True, verbose_name="Admin DID Directeur F")
    admin_did_directeur_h = models.CharField(max_length=255, null=True, verbose_name="Admin DID Directeur H")
    admin_did_ouvrier_autre_f = models.CharField(max_length=255, null=True, verbose_name="Admin DID Ouvrier Autre F")
    admin_did_ouvrier_autre_h = models.CharField(max_length=255, null=True, verbose_name="Admin DID Ouvrier Autre H")
    admin_did_surveillant_f = models.CharField(max_length=255, null=True, verbose_name="Admin DID Surveillant F")
    admin_did_surveillant_h = models.CharField(max_length=255, null=True, verbose_name="Admin DID Surveillant H")

    # Statut 'admin_moi' (Administration - Ministère de l'Intérieur)
    admin_moi_directeur_adjoint_f = models.CharField(max_length=255, null=True, verbose_name="Admin MOI Dir. Adj. F")
    admin_moi_directeur_adjoint_h = models.CharField(max_length=255, null=True, verbose_name="Admin MOI Dir. Adj. H")
    admin_moi_directeur_f = models.CharField(max_length=255, null=True, verbose_name="Admin MOI Directeur F")
    admin_moi_directeur_h = models.CharField(max_length=255, null=True, verbose_name="Admin MOI Directeur H")
    admin_moi_ouvrier_autre_f = models.CharField(max_length=255, null=True, verbose_name="Admin MOI Ouvrier Autre F")
    admin_moi_ouvrier_autre_h = models.CharField(max_length=255, null=True, verbose_name="Admin MOI Ouvrier Autre H")
    admin_moi_surveillant_f = models.CharField(max_length=255, null=True, verbose_name="Admin MOI Surveillant F")
    admin_moi_surveillant_h = models.CharField(max_length=255, null=True, verbose_name="Admin MOI Surveillant H")

    # Statut 'admin_pd' (Administration - Personnel Détaché)
    admin_pd_directeur_adjoint_f = models.CharField(max_length=255, null=True, verbose_name="Admin PD Dir. Adj. F")
    admin_pd_directeur_adjoint_h = models.CharField(max_length=255, null=True, verbose_name="Admin PD Dir. Adj. H")
    admin_pd_directeur_f = models.CharField(max_length=255, null=True, verbose_name="Admin PD Directeur F")
    admin_pd_directeur_h = models.CharField(max_length=255, null=True, verbose_name="Admin PD Directeur H")
    admin_pd_ouvrier_autre_f = models.CharField(max_length=255, null=True, verbose_name="Admin PD Ouvrier Autre F")
    admin_pd_ouvrier_autre_h = models.CharField(max_length=255, null=True, verbose_name="Admin PD Ouvrier Autre H")
    admin_pd_surveillant_f = models.CharField(max_length=255, null=True, verbose_name="Admin PD Surveillant F")
    admin_pd_surveillant_h = models.CharField(max_length=255, null=True, verbose_name="Admin PD Surveillant H")

    def __str__(self):
        return f"Personnel Administratif et Ouvrier ST2 (ID: {self.id})"

    class Meta:
        verbose_name = "Personnel Administratif/Ouvrier ST2"
        verbose_name_plural = "Personnel Administratif/Ouvrier ST2"

class St2_repartition_et_affectations(models.Model):
    # 1. form_st_id (bigint(20), Oui)
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 2. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # Affectation du personnel par statut et fonction (D: Directeur, DA: Directeur Adjoint, PD: Personnel Détaché, PRED: Pré-détachement)
    
    # TITULAIRE (TI)
    st2_classe_affectation_ti_d4 = models.CharField(max_length=255, null=True, verbose_name="Titulaire D4")
    st2_classe_affectation_ti_d6 = models.CharField(max_length=255, null=True, verbose_name="Titulaire D6")
    st2_classe_affectation_ti_da = models.CharField(max_length=255, null=True, verbose_name="Titulaire DA")
    st2_classe_affectation_ti_autres = models.CharField(max_length=255, null=True, verbose_name="Titulaire Autres")
    
    # DETACHEMENT (DI)
    st2_classe_affectation_di_d4 = models.CharField(max_length=255, null=True, verbose_name="Détachement D4")
    st2_classe_affectation_di_d6 = models.CharField(max_length=255, null=True, verbose_name="Détachement D6")
    st2_classe_affectation_di_da = models.CharField(max_length=255, null=True, verbose_name="Détachement DA")
    st2_classe_affectation_di_autres = models.CharField(max_length=255, null=True, verbose_name="Détachement Autres")
    
    # PRE-DETACHEMENT (PRED)
    st2_classe_affectation_pred_d4 = models.CharField(max_length=255, null=True, verbose_name="Pré-Détachement D4")
    st2_classe_affectation_pred_d6 = models.CharField(max_length=255, null=True, verbose_name="Pré-Détachement D6")
    st2_classe_affectation_pred_da = models.CharField(max_length=255, null=True, verbose_name="Pré-Détachement DA")
    st2_classe_affectation_pred_autres = models.CharField(max_length=255, null=True, verbose_name="Pré-Détachement Autres")
    
    # PERSONNEL DETACHE (PD)
    st2_classe_affectation_pd_d4 = models.CharField(max_length=255, null=True, verbose_name="Personnel Détaché D4")
    st2_classe_affectation_pd_d6 = models.CharField(max_length=255, null=True, verbose_name="Personnel Détaché D6")
    st2_classe_affectation_pd_da = models.CharField(max_length=255, null=True, verbose_name="Personnel Détaché DA")
    st2_classe_affectation_pd_autres = models.CharField(max_length=255, null=True, verbose_name="Personnel Détaché Autres")

    # Note: L'image suggère que ces champs sont répétés pour chaque niveau (2e, 3e, 4e, 5e, 6e, et 'autres' - correspondant probablement à 'PRED', 'PD', etc.)
    # Étant donné le nombre élevé, nous avons listé les 4 premières séries (2e, 3e, 4e, 5e) qui correspondent à l'image fournie, mais la nomenclature est plus complexe qu'une simple classe.
    # Les champs visibles dans l'image semblent être une répartition par classe (1ère, 2ème, etc.) et par statut/fonction (TI, DI, PD, PRED - D4, D6, DA, autres).

    # Représentation des champs basés sur la nomenclature complète visible dans la table (ex: st2_classe_affectation_ti_d4 pour la 2e, 3e, 4e, 5e, 6e, autres)
    
    # --- Affectation pour la 2ème Classe (2E) ---
    st2_classe_affectation_2e_ti_d4 = models.CharField(max_length=255, null=True, verbose_name="Affect. 2e - Titulaire D4")
    st2_classe_affectation_2e_ti_d6 = models.CharField(max_length=255, null=True, verbose_name="Affect. 2e - Titulaire D6")
    st2_classe_affectation_2e_ti_da = models.CharField(max_length=255, null=True, verbose_name="Affect. 2e - Titulaire DA")
    st2_classe_affectation_2e_ti_autres = models.CharField(max_length=255, null=True, verbose_name="Affect. 2e - Titulaire Autres")
    st2_classe_affectation_2e_di_d4 = models.CharField(max_length=255, null=True, verbose_name="Affect. 2e - Détachement D4")
    st2_classe_affectation_2e_di_d6 = models.CharField(max_length=255, null=True, verbose_name="Affect. 2e - Détachement D6")
    st2_classe_affectation_2e_di_da = models.CharField(max_length=255, null=True, verbose_name="Affect. 2e - Détachement DA")
    st2_classe_affectation_2e_di_autres = models.CharField(max_length=255, null=True, verbose_name="Affect. 2e - Détachement Autres")
    st2_classe_affectation_2e_pred_d4 = models.CharField(max_length=255, null=True, verbose_name="Affect. 2e - Pré-Détachement D4")
    st2_classe_affectation_2e_pred_d6 = models.CharField(max_length=255, null=True, verbose_name="Affect. 2e - Pré-Détachement D6")
    st2_classe_affectation_2e_pred_da = models.CharField(max_length=255, null=True, verbose_name="Affect. 2e - Pré-Détachement DA")
    st2_classe_affectation_2e_pred_autres = models.CharField(max_length=255, null=True, verbose_name="Affect. 2e - Pré-Détachement Autres")
    st2_classe_affectation_2e_pd_d4 = models.CharField(max_length=255, null=True, verbose_name="Affect. 2e - Personnel Détaché D4")
    st2_classe_affectation_2e_pd_d6 = models.CharField(max_length=255, null=True, verbose_name="Affect. 2e - Personnel Détaché D6")
    st2_classe_affectation_2e_pd_da = models.CharField(max_length=255, null=True, verbose_name="Affect. 2e - Personnel Détaché DA")
    st2_classe_affectation_2e_pd_autres = models.CharField(max_length=255, null=True, verbose_name="Affect. 2e - Personnel Détaché Autres")

    # --- Affectation pour la 3ème Classe (3E) ---
    st2_classe_affectation_3e_ti_d4 = models.CharField(max_length=255, null=True, verbose_name="Affect. 3e - Titulaire D4")
    st2_classe_affectation_3e_ti_d6 = models.CharField(max_length=255, null=True, verbose_name="Affect. 3e - Titulaire D6")
    st2_classe_affectation_3e_ti_da = models.CharField(max_length=255, null=True, verbose_name="Affect. 3e - Titulaire DA")
    st2_classe_affectation_3e_ti_autres = models.CharField(max_length=255, null=True, verbose_name="Affect. 3e - Titulaire Autres")
    st2_classe_affectation_3e_di_d4 = models.CharField(max_length=255, null=True, verbose_name="Affect. 3e - Détachement D4")
    st2_classe_affectation_3e_di_d6 = models.CharField(max_length=255, null=True, verbose_name="Affect. 3e - Détachement D6")
    st2_classe_affectation_3e_di_da = models.CharField(max_length=255, null=True, verbose_name="Affect. 3e - Détachement DA")
    st2_classe_affectation_3e_di_autres = models.CharField(max_length=255, null=True, verbose_name="Affect. 3e - Détachement Autres")
    st2_classe_affectation_3e_pred_d4 = models.CharField(max_length=255, null=True, verbose_name="Affect. 3e - Pré-Détachement D4")
    st2_classe_affectation_3e_pred_d6 = models.CharField(max_length=255, null=True, verbose_name="Affect. 3e - Pré-Détachement D6")
    st2_classe_affectation_3e_pred_da = models.CharField(max_length=255, null=True, verbose_name="Affect. 3e - Pré-Détachement DA")
    st2_classe_affectation_3e_pred_autres = models.CharField(max_length=255, null=True, verbose_name="Affect. 3e - Pré-Détachement Autres")
    st2_classe_affectation_3e_pd_d4 = models.CharField(max_length=255, null=True, verbose_name="Affect. 3e - Personnel Détaché D4")
    st2_classe_affectation_3e_pd_d6 = models.CharField(max_length=255, null=True, verbose_name="Affect. 3e - Personnel Détaché D6")
    st2_classe_affectation_3e_pd_da = models.CharField(max_length=255, null=True, verbose_name="Affect. 3e - Personnel Détaché DA")
    st2_classe_affectation_3e_pd_autres = models.CharField(max_length=255, null=True, verbose_name="Affect. 3e - Personnel Détaché Autres")

    # --- Affectation pour la 4ème Classe (4E) ---
    st2_classe_affectation_4e_ti_d4 = models.CharField(max_length=255, null=True, verbose_name="Affect. 4e - Titulaire D4")
    st2_classe_affectation_4e_ti_d6 = models.CharField(max_length=255, null=True, verbose_name="Affect. 4e - Titulaire D6")
    st2_classe_affectation_4e_ti_da = models.CharField(max_length=255, null=True, verbose_name="Affect. 4e - Titulaire DA")
    st2_classe_affectation_4e_ti_autres = models.CharField(max_length=255, null=True, verbose_name="Affect. 4e - Titulaire Autres")
    st2_classe_affectation_4e_di_d4 = models.CharField(max_length=255, null=True, verbose_name="Affect. 4e - Détachement D4")
    st2_classe_affectation_4e_di_d6 = models.CharField(max_length=255, null=True, verbose_name="Affect. 4e - Détachement D6")
    st2_classe_affectation_4e_di_da = models.CharField(max_length=255, null=True, verbose_name="Affect. 4e - Détachement DA")
    st2_classe_affectation_4e_di_autres = models.CharField(max_length=255, null=True, verbose_name="Affect. 4e - Détachement Autres")
    st2_classe_affectation_4e_pred_d4 = models.CharField(max_length=255, null=True, verbose_name="Affect. 4e - Pré-Détachement D4")
    st2_classe_affectation_4e_pred_d6 = models.CharField(max_length=255, null=True, verbose_name="Affect. 4e - Pré-Détachement D6")
    st2_classe_affectation_4e_pred_da = models.CharField(max_length=255, null=True, verbose_name="Affect. 4e - Pré-Détachement DA")
    st2_classe_affectation_4e_pred_autres = models.CharField(max_length=255, null=True, verbose_name="Affect. 4e - Pré-Détachement Autres")
    st2_classe_affectation_4e_pd_d4 = models.CharField(max_length=255, null=True, verbose_name="Affect. 4e - Personnel Détaché D4")
    st2_classe_affectation_4e_pd_d6 = models.CharField(max_length=255, null=True, verbose_name="Affect. 4e - Personnel Détaché D6")
    st2_classe_affectation_4e_pd_da = models.CharField(max_length=255, null=True, verbose_name="Affect. 4e - Personnel Détaché DA")
    st2_classe_affectation_4e_pd_autres = models.CharField(max_length=255, null=True, verbose_name="Affect. 4e - Personnel Détaché Autres")
    
    # --- Affectation pour la 5ème Classe (5E) ---
    st2_classe_affectation_5e_ti_d4 = models.CharField(max_length=255, null=True, verbose_name="Affect. 5e - Titulaire D4")
    st2_classe_affectation_5e_ti_d6 = models.CharField(max_length=255, null=True, verbose_name="Affect. 5e - Titulaire D6")
    st2_classe_affectation_5e_ti_da = models.CharField(max_length=255, null=True, verbose_name="Affect. 5e - Titulaire DA")
    st2_classe_affectation_5e_ti_autres = models.CharField(max_length=255, null=True, verbose_name="Affect. 5e - Titulaire Autres")
    st2_classe_affectation_5e_di_d4 = models.CharField(max_length=255, null=True, verbose_name="Affect. 5e - Détachement D4")
    st2_classe_affectation_5e_di_d6 = models.CharField(max_length=255, null=True, verbose_name="Affect. 5e - Détachement D6")
    st2_classe_affectation_5e_di_da = models.CharField(max_length=255, null=True, verbose_name="Affect. 5e - Détachement DA")
    st2_classe_affectation_5e_di_autres = models.CharField(max_length=255, null=True, verbose_name="Affect. 5e - Détachement Autres")
    st2_classe_affectation_5e_pred_d4 = models.CharField(max_length=255, null=True, verbose_name="Affect. 5e - Pré-Détachement D4")
    st2_classe_affectation_5e_pred_d6 = models.CharField(max_length=255, null=True, verbose_name="Affect. 5e - Pré-Détachement D6")
    st2_classe_affectation_5e_pred_da = models.CharField(max_length=255, null=True, verbose_name="Affect. 5e - Pré-Détachement DA")
    st2_classe_affectation_5e_pred_autres = models.CharField(max_length=255, null=True, verbose_name="Affect. 5e - Pré-Détachement Autres")
    st2_classe_affectation_5e_pd_d4 = models.CharField(max_length=255, null=True, verbose_name="Affect. 5e - Personnel Détaché D4")
    st2_classe_affectation_5e_pd_d6 = models.CharField(max_length=255, null=True, verbose_name="Affect. 5e - Personnel Détaché D6")
    st2_classe_affectation_5e_pd_da = models.CharField(max_length=255, null=True, verbose_name="Affect. 5e - Personnel Détaché DA")
    st2_classe_affectation_5e_pd_autres = models.CharField(max_length=255, null=True, verbose_name="Affect. 5e - Personnel Détaché Autres")

    # Il manque dans l'image les affectations pour la 1ère et 6ème, mais le pattern est clair. 
    # Pour ne pas inventer de champs, nous nous arrêtons aux 5èmes classes. 
    # Le pattern pour la 1ère classe (1E) et 6ème classe (6E) serait le même:
    # st2_classe_affectation_1e_ti_d4, st2_classe_affectation_6e_ti_d4, etc.

    def __str__(self):
        return f"Répartition et Affectations ST2 (ID: {self.id})"

    class Meta:
        verbose_name = "Répartition et Affectations ST2"
        verbose_name_plural = "Répartition et Affectations ST2"

class St2_repartition_enseignants_et_eligibles(models.Model):
    # 1. form_st_id (bigint(20), Oui)
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )
    # 3. NbEnseignantsEligiblesRetraite (varchar(255), Oui)
    nb_enseignants_eligibles_retraite = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Nombre Enseignants Éligibles à la Retraite"
    )

    def __str__(self):
        return f"Éligibilité Retraite ST2 (ID: {self.id})"

    class Meta:
        verbose_name = "Répartition Enseignants et Éligibles ST2"
        verbose_name_plural = "Répartition Enseignants et Éligibles ST2"

class St2_repartition_releve(models.Model):
    # 1. form_st_id (bigint(20), Oui) - Clé étrangère vers le formulaire d'enquête
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 2. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 3. releveAutresF (varchar(255), Oui)
    releve_autres_f = models.CharField(max_length=255, null=True, verbose_name="Relevé Autres Femmes")
    
    # 4. releveAutresH (varchar(255), Oui)
    releve_autres_h = models.CharField(max_length=255, null=True, verbose_name="Relevé Autres Hommes")
    
    # 5. releveD4F (varchar(255), Oui)
    releve_d4_f = models.CharField(max_length=255, null=True, verbose_name="Relevé D4 Femmes")
    
    # 6. releveD4H (varchar(255), Oui)
    releve_d4_h = models.CharField(max_length=255, null=True, verbose_name="Relevé D4 Hommes")
    
    # 7. releveD6F (varchar(255), Oui)
    releve_d6_f = models.CharField(max_length=255, null=True, verbose_name="Relevé D6 Femmes")
    
    # 8. releveD6H (varchar(255), Oui)
    releve_d6_h = models.CharField(max_length=255, null=True, verbose_name="Relevé D6 Hommes")
    
    # 9. releveP6F (varchar(255), Oui)
    releve_p6_f = models.CharField(max_length=255, null=True, verbose_name="Relevé P6 Femmes")
    
    # 10. releveP6H (varchar(255), Oui)
    releve_p6_h = models.CharField(max_length=255, null=True, verbose_name="Relevé P6 Hommes")
    
    # 11. relevePred4F (varchar(255), Oui)
    releve_pred4_f = models.CharField(max_length=255, null=True, verbose_name="Relevé PRE D4 Femmes")
    
    # 12. relevePred4H (varchar(255), Oui)
    releve_pred4_h = models.CharField(max_length=255, null=True, verbose_name="Relevé PRE D4 Hommes")

    def __str__(self):
        return f"Répartition Relevé ST2 (ID: {self.id})"

    class Meta:
        verbose_name = "Répartition Relevé ST2"
        verbose_name_plural = "Répartition Relevé ST2"

class St2_resultat_enaf_epsante(models.Model):
    # 44. form_st_id (bigint(20), Non)
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 45. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 1-8. Résultats d'examen (Admis, Inscrit, Présent)
    st2_effectif_eleves_admins_francais_f = models.IntegerField(null=True, verbose_name="Admis Français Filles")
    st2_effectif_eleves_admins_francais_g = models.IntegerField(null=True, verbose_name="Admis Français Garçons")
    st2_effectif_eleves_admins_maths_f = models.IntegerField(null=True, verbose_name="Admis Maths Filles")
    st2_effectif_eleves_admins_maths_g = models.IntegerField(null=True, verbose_name="Admis Maths Garçons")
    st2_effectif_eleves_inscrit_f = models.IntegerField(null=True, verbose_name="Inscrits Filles")
    st2_effectif_eleves_inscrit_g = models.IntegerField(null=True, verbose_name="Inscrits Garçons")
    st2_effectif_eleves_present_f = models.IntegerField(null=True, verbose_name="Présents Filles")
    st2_effectif_eleves_present_g = models.IntegerField(null=True, verbose_name="Présents Garçons")

    # 9-14. Nombre d'absences par classe (1ère à 6ème)
    st2_nombre_absences_eleves_1 = models.IntegerField(null=True, verbose_name="Absences Classe 1")
    st2_nombre_absences_eleves_2 = models.IntegerField(null=True, verbose_name="Absences Classe 2")
    st2_nombre_absences_eleves_3 = models.IntegerField(null=True, verbose_name="Absences Classe 3")
    st2_nombre_absences_eleves_4 = models.IntegerField(null=True, verbose_name="Absences Classe 4")
    st2_nombre_absences_eleves_5 = models.IntegerField(null=True, verbose_name="Absences Classe 5")
    st2_nombre_absences_eleves_6 = models.IntegerField(null=True, verbose_name="Absences Classe 6")

    # 15-20. Bénéficiaires du déparasitage par classe (1ère à 6ème)
    st2_nombre_eleves_beneficiants_deparasitage_1 = models.IntegerField(null=True, verbose_name="Bénéf. Déparasitage Classe 1")
    st2_nombre_eleves_beneficiants_deparasitage_2 = models.IntegerField(null=True, verbose_name="Bénéf. Déparasitage Classe 2")
    st2_nombre_eleves_beneficiants_deparasitage_3 = models.IntegerField(null=True, verbose_name="Bénéf. Déparasitage Classe 3")
    st2_nombre_eleves_beneficiants_deparasitage_4 = models.IntegerField(null=True, verbose_name="Bénéf. Déparasitage Classe 4")
    st2_nombre_eleves_beneficiants_deparasitage_5 = models.IntegerField(null=True, verbose_name="Bénéf. Déparasitage Classe 5")
    st2_nombre_eleves_beneficiants_deparasitage_6 = models.IntegerField(null=True, verbose_name="Bénéf. Déparasitage Classe 6")

    # 21-26. Bénéficiaires de visites médicales par classe (1ère à 6ème)
    st2_nombre_eleves_beneficiants_visite_medicales_1 = models.IntegerField(null=True, verbose_name="Bénéf. Visite Méd. Classe 1")
    st2_nombre_eleves_beneficiants_visite_medicales_2 = models.IntegerField(null=True, verbose_name="Bénéf. Visite Méd. Classe 2")
    st2_nombre_eleves_beneficiants_visite_medicales_3 = models.IntegerField(null=True, verbose_name="Bénéf. Visite Méd. Classe 3")
    st2_nombre_eleves_beneficiants_visite_medicales_4 = models.IntegerField(null=True, verbose_name="Bénéf. Visite Méd. Classe 4")
    st2_nombre_eleves_beneficiants_visite_medicales_5 = models.IntegerField(null=True, verbose_name="Bénéf. Visite Méd. Classe 5")
    st2_nombre_eleves_beneficiants_visite_medicales_6 = models.IntegerField(null=True, verbose_name="Bénéf. Visite Méd. Classe 6")

    # 27-32. Nombre de jours ouvrables par classe (1ère à 6ème)
    st2_nombre_jours_ouvrables_1 = models.IntegerField(null=True, verbose_name="Jours Ouvrables Classe 1")
    st2_nombre_jours_ouvrables_2 = models.IntegerField(null=True, verbose_name="Jours Ouvrables Classe 2")
    st2_nombre_jours_ouvrables_3 = models.IntegerField(null=True, verbose_name="Jours Ouvrables Classe 3")
    st2_nombre_jours_ouvrables_4 = models.IntegerField(null=True, verbose_name="Jours Ouvrables Classe 4")
    st2_nombre_jours_ouvrables_5 = models.IntegerField(null=True, verbose_name="Jours Ouvrables Classe 5")
    st2_nombre_jours_ouvrables_6 = models.IntegerField(null=True, verbose_name="Jours Ouvrables Classe 6")

    # 33-38. Nombre total d'élèves par classe (1ère à 6ème)
    st2_nombre_total_eleves_1 = models.IntegerField(null=True, verbose_name="Total Élèves Classe 1")
    st2_nombre_total_eleves_2 = models.IntegerField(null=True, verbose_name="Total Élèves Classe 2")
    st2_nombre_total_eleves_3 = models.IntegerField(null=True, verbose_name="Total Élèves Classe 3")
    st2_nombre_total_eleves_4 = models.IntegerField(null=True, verbose_name="Total Élèves Classe 4")
    st2_nombre_total_eleves_5 = models.IntegerField(null=True, verbose_name="Total Élèves Classe 5")
    st2_nombre_total_eleves_6 = models.IntegerField(null=True, verbose_name="Total Élèves Classe 6")

    # 39-43. Statistiques générales
    st2_taux_abandon = models.FloatField(null=True, verbose_name="Taux Abandon (Double)")
    st2_taux_reussite_analof = models.FloatField(null=True, verbose_name="Taux Réussite Analphabétisme (Double)")
    st2_total_admins_g_reussite_test = models.IntegerField(null=True, verbose_name="Total Admis Test Réussite Garçons")
    st2_total_admins_f_reussite_test = models.IntegerField(null=True, verbose_name="Total Admis Test Réussite Filles")

    def __str__(self):
        return f"Résultats ENAF & EPSANTÉ ST2 (ID: {self.id})"

    class Meta:
        verbose_name = "Résultats ENAF & EPSANTÉ ST2"
        verbose_name_plural = "Résultats ENAF & EPSANTÉ ST2"

class St3_disponible_programme_national(models.Model):
    # 2. form_st_id (bigint(20), Oui) - Clé étrangère vers le formulaire d'enquête ST3
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 3. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 1. EstDisponibiliteDansLeProgrammeNational (bit(1), Oui)
    est_disponibilite_dans_le_programme_national = models.BooleanField(
        null=True, 
        verbose_name="Est Disponible dans le Programme National"
    )

    # 4. NomDuFiliere (varchar(255), Oui)
    nom_du_filiere = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Nom de la Filière"
    )
    
    # 5. TypeDeProgrammeNational (varchar(255), Oui)
    type_de_programme_national = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Type de Programme National"
    )

    def __str__(self):
        return f"Programme National ST3 (ID: {self.id})"

    class Meta:
        verbose_name = "Disponibilité Programme National ST3"
        verbose_name_plural = "Disponibilités Programme National ST3"

class St3_documentation(models.Model):
    # 3. form_st_id (bigint(20), Oui) - Clé étrangère vers le formulaire d'enquête ST3
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 4. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 1. st3_manuel_procedure (bit(1), Oui)
    st3_manuel_procedure = models.BooleanField(
        null=True, 
        verbose_name="Manuel de Procédure Disponible"
    )

    # 2. st3_plan_communication (bit(1), Oui)
    st3_plan_communication = models.BooleanField(
        null=True, 
        verbose_name="Plan de Communication Disponible"
    )

    def __str__(self):
        return f"Documentation ST3 (ID: {self.id})"

    class Meta:
        verbose_name = "Documentation ST3"
        verbose_name_plural = "Documentation ST3"

class St3_dual_input_section(models.Model):
    # 3. form_st_id (bigint(20), Oui) - Clé étrangère vers le formulaire d'enquête
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 4. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 1. st3_enseignants_formes_genre (int(11), Oui)
    st3_enseignants_formes_genre = models.IntegerField(
        null=True, 
        verbose_name="Nombre d'Enseignants Formés (Genre)"
    )

    # 2. st3_femmes_enseignantes_recrutees (int(11), Oui)
    st3_femmes_enseignantes_recrutees = models.IntegerField(
        null=True, 
        verbose_name="Nombre de Femmes Enseignantes Recrutées"
    )

    def __str__(self):
        return f"Section Double Entrée ST3 (ID: {self.id})"

    class Meta:
        verbose_name = "Section Double Entrée ST3"
        verbose_name_plural = "Sections Double Entrée ST3"

class St3_effectif_eleve_inscrit_sexe_annee_etude_age_revolu(models.Model):
    # 1. effectifParAgeEtSexe_id (bigint(20), Oui)
    effectif_par_age_sexe_id = models.BigIntegerField(
        null=True, 
        verbose_name="ID Effectif par Âge et Sexe (FK)"
    )

    # 2. effectifParCategorieParticuliere_id (bigint(20), Oui)
    effectif_par_categorie_particuliere_id = models.BigIntegerField(
        null=True, 
        verbose_name="ID Effectif par Catégorie Particulière (FK)"
    )

    # 3. form_st_id (bigint(20), Oui) - Clé étrangère vers le formulaire d'enquête
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 4. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    def __str__(self):
        return f"Liaison Effectif Élèves ST3 (ID: {self.id})"

    class Meta:
        verbose_name = "Liaison Effectif Élèves ST3"
        verbose_name_plural = "Liaisons Effectif Élèves ST3"   

class St3_effectif_eleve_type_enseignant(models.Model):
    pass

# Modèle pour 'st3_effectif_par_age_sexe'
class St3_effectif_par_age_sexe(models.Model):
    pass

# Modèle pour 'st3_effectif_par_categorie_particuliere'
class St3_effectif_par_categorie_particuliere(models.Model):
    pass

class St3_eleve(models.Model):
    # 1. form_st_id (bigint(20), Oui) - Clé étrangère vers le formulaire d'enquête
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 2. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 3. Adresse (varchar(255), Oui)
    adresse = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Adresse de l'Élève"
    )

    # 4. DateNaissance (varchar(255), Oui)
    date_naissance = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Date de Naissance"
    )

    # 5. Edition (varchar(255), Oui)
    edition = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Édition"
    )

    # 6. Filiere (varchar(255), Oui)
    filiere = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Filière"
    )

    # 7. Nom (varchar(255), Oui)
    nom = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Nom de l'Élève"
    )

    # 8. Observation (varchar(255), Oui)
    observation = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Observation"
    )

    # 9. Sexe (varchar(255), Oui)
    sexe = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Sexe"
    )

    # 10. Telephone (varchar(255), Oui)
    telephone = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Téléphone Élève"
    )

    # 11. TelephoneParent (varchar(255), Oui)
    telephone_parent = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Téléphone Parent"
    )

    def __str__(self):
        return f"Élève ST3 - {self.nom} (ID: {self.id})"

    class Meta:
        verbose_name = "Élève ST3"
        verbose_name_plural = "Élèves ST3"

class St3_enregistrement_equipement(models.Model):
    # 3. form_st_id (bigint(20), Oui) - Clé étrangère vers le formulaire d'enquête
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 4. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 1. NombreEquipementsBon (int(11), Oui)
    nombre_equipements_bon = models.IntegerField(
        null=True, 
        verbose_name="Nombre Équipements Bon État"
    )

    # 2. NombreEquipementsMauvais (int(11), Oui)
    nombre_equipements_mauvais = models.IntegerField(
        null=True, 
        verbose_name="Nombre Équipements Mauvais État"
    )

    # 5. NomEquipement (varchar(255), Oui)
    nom_equipement = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Nom de l'Équipement"
    )
    
    # 6. TypeAtelierOuLabo (varchar(255), Oui)
    type_atelier_ou_labo = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Type d'Atelier ou Laboratoire"
    )

    def __str__(self):
        return f"Équipement ST3 - {self.nom_equipement} (ID: {self.id})"

    class Meta:
        verbose_name = "Enregistrement Équipement ST3"
        verbose_name_plural = "Enregistrements Équipement ST3"

class St3_equipement_existant(models.Model):
    # 3. form_st_id (bigint(20), Oui) - Clé étrangère vers le formulaire d'enquête
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    )

    # 4. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 1. NombreEquipementsBon (int(11), Oui)
    nombre_equipements_bon = models.IntegerField(
        null=True, 
        verbose_name="Nombre Équipements Bon État"
    ) #

    # 2. NombreEquipementsMauvais (int(11), Oui)
    nombre_equipements_mauvais = models.IntegerField(
        null=True, 
        verbose_name="Nombre Équipements Mauvais État"
    ) #

    # 5. NomEquipement (varchar(255), Oui)
    nom_equipement = models.CharField(
        max_length=255, 
        null=True, 
        verbose_name="Nom de l'Équipement"
    ) #
    
    # Le champ TypeAtelierOuLabo est absent ici

    def __str__(self):
        return f"Équipement Existant ST3 - {self.nom_equipement} (ID: {self.id})"

    class Meta:
        verbose_name = "Équipement Existant ST3"
        verbose_name_plural = "Équipements Existants ST3"

class St3_formation(models.Model):
    # 2. form_st_id (bigint(20), Oui) - Clé étrangère vers le formulaire d'enquête
    form_st_id = models.BigIntegerField(
        null=True, 
        verbose_name="Formulaire ST ID"
    ) #

    # 3. id (bigint(20), AUTO_INCREMENT, Non)
    # Géré automatiquement par Django.

    # 1. st3_enseignants_formes_genre (int(11), Oui)
    st3_enseignants_formes_genre = models.IntegerField(
        null=True, 
        verbose_name="Nombre d'Enseignants Formés (Genre)"
    ) #

    def __str__(self):
        return f"Formation ST3 (ID: {self.id})"

    class Meta:
        verbose_name = "Formation ST"

# Modèle pour 'st3_infrastructure_activites'
class St3_infrastructure_activites(models.Model):
    pass

# Modèle pour 'st3_manuel_disponible_niveau'
class St3_manuel_disponible_niveau(models.Model):
    pass

# Modèle pour 'st3_nombre_locaux_caracteristique_etat_mur'
class St3_nombre_locaux_caracteristique_etat_mur(models.Model):
    pass

# Modèle pour 'st3_nombre_locaux_caracteristique_etat_nature_toilette'
class St3_nombre_locaux_caracteristique_etat_nature_toilette(models.Model):
    pass

# Modèle pour 'st3_note_section'
class St3_note_section(models.Model):
    pass

# Modèle pour 'st3_personnel_administratif_fonction_sexe'
class St3_personnel_administratif_fonction_sexe(models.Model):
    pass

# Modèle pour 'st3_personnel_enseignant'
class St3_personnel_enseignant(models.Model):
    pass

# Modèle pour 'st3_personnel_enseignant_sexe_qualification'
class St3_personnel_enseignant_sexe_qualification(models.Model):
    pass

# Modèle pour 'st3_repartition_temps_formation'
class St3_repartition_temps_formation(models.Model):
    pass

# Modèle pour 'st3_reseaux_environnement'
class St3_reseaux_environnement(models.Model):
    pass

# Modèle pour 'st3_resultat_examen_etat'
class St3_resultat_examen_etat(models.Model):
    pass

class St3_resultat_jury_national(models.Model):
    pass
