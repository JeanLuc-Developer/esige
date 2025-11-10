# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AnneeScolaire(models.Model):
    active = models.TextField(blank=True, null=True)  # This field type is a guess.
    generate = models.TextField(blank=True, null=True)  # This field type is a guess.
    open = models.TextField(blank=True, null=True)  # This field type is a guess.
    valid = models.TextField(blank=True, null=True)  # This field type is a guess.
    id = models.BigIntegerField(primary_key=True)
    lib_annee_scolaire = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'annee_scolaire'


class AnneeScolaireSeq(models.Model):
    next_val = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'annee_scolaire_seq'


class Annuaires(models.Model):
    nouveauentrantpremieragerevolumoins6 = models.IntegerField(db_column='nouveauEntrantPremierAgeRevoluMoins6')  # Field name made lowercase.
    nouveauentrantpremieragerevolumoins7 = models.IntegerField(db_column='nouveauEntrantPremierAgeRevoluMoins7')  # Field name made lowercase.
    nouveauentrantpremieragerevolumoins8 = models.IntegerField(db_column='nouveauEntrantPremierAgeRevoluMoins8')  # Field name made lowercase.
    nouveauentrantpremieragerevolumoins9 = models.IntegerField(db_column='nouveauEntrantPremierAgeRevoluMoins9')  # Field name made lowercase.
    nouveauentrantpremieragerevoluplus9 = models.IntegerField(db_column='nouveauEntrantPremierAgeRevoluPlus9')  # Field name made lowercase.
    nouveauinscritpremierautre = models.IntegerField(db_column='nouveauInscritPremierAUTRE')  # Field name made lowercase.
    nouveauinscritpremierecc = models.IntegerField(db_column='nouveauInscritPremierECC')  # Field name made lowercase.
    nouveauinscritpremierecf = models.IntegerField(db_column='nouveauInscritPremierECF')  # Field name made lowercase.
    nouveauinscritpremiereci = models.IntegerField(db_column='nouveauInscritPremierECI')  # Field name made lowercase.
    nouveauinscritpremiereck = models.IntegerField(db_column='nouveauInscritPremierECK')  # Field name made lowercase.
    nouveauinscritpremierecp = models.IntegerField(db_column='nouveauInscritPremierECP')  # Field name made lowercase.
    nouveauinscritpremierecs = models.IntegerField(db_column='nouveauInscritPremierECS')  # Field name made lowercase.
    nouveauinscritpremierenc = models.IntegerField(db_column='nouveauInscritPremierENC')  # Field name made lowercase.
    nouveauinscritpremierprive = models.IntegerField(db_column='nouveauInscritPremierPRIVE')  # Field name made lowercase.
    participationpersonnelfemmeautre = models.IntegerField(db_column='participationpersonnelFemmeAUTRE')  # Field name made lowercase.
    participationpersonnelfemmeenc = models.IntegerField(db_column='participationpersonnelFemmeENC')  # Field name made lowercase.
    participationpersonnelfemmeepr = models.IntegerField(db_column='participationpersonnelFemmeEPR')  # Field name made lowercase.
    participationpersonnelfemmefemmeecc = models.IntegerField(db_column='participationpersonnelFemmeFemmeECC')  # Field name made lowercase.
    participationpersonnelfemmefemmeecf = models.IntegerField(db_column='participationpersonnelFemmeFemmeECF')  # Field name made lowercase.
    participationpersonnelfemmefemmeeci = models.IntegerField(db_column='participationpersonnelFemmeFemmeECI')  # Field name made lowercase.
    participationpersonnelfemmefemmeeck = models.IntegerField(db_column='participationpersonnelFemmeFemmeECK')  # Field name made lowercase.
    participationpersonnelfemmefemmeecp = models.IntegerField(db_column='participationpersonnelFemmeFemmeECP')  # Field name made lowercase.
    participationpersonnelfemmefemmeecs = models.IntegerField(db_column='participationpersonnelFemmeFemmeECS')  # Field name made lowercase.
    participationpersonnelfemmefemmesecondaireecc = models.IntegerField(db_column='participationpersonnelFemmeFemmeSecondaireECC')  # Field name made lowercase.
    participationpersonnelfemmefemmesecondaireecf = models.IntegerField(db_column='participationpersonnelFemmeFemmeSecondaireECF')  # Field name made lowercase.
    participationpersonnelfemmefemmesecondaireeci = models.IntegerField(db_column='participationpersonnelFemmeFemmeSecondaireECI')  # Field name made lowercase.
    participationpersonnelfemmefemmesecondaireeck = models.IntegerField(db_column='participationpersonnelFemmeFemmeSecondaireECK')  # Field name made lowercase.
    participationpersonnelfemmefemmesecondaireecp = models.IntegerField(db_column='participationpersonnelFemmeFemmeSecondaireECP')  # Field name made lowercase.
    participationpersonnelfemmefemmesecondaireecs = models.IntegerField(db_column='participationpersonnelFemmeFemmeSecondaireECS')  # Field name made lowercase.
    participationpersonnelfemmeprive = models.IntegerField(db_column='participationpersonnelFemmePRIVE')  # Field name made lowercase.
    participationpersonnelfemmesecondaireautre = models.IntegerField(db_column='participationpersonnelFemmeSecondaireAUTRE')  # Field name made lowercase.
    participationpersonnelfemmesecondaireenc = models.IntegerField(db_column='participationpersonnelFemmeSecondaireENC')  # Field name made lowercase.
    proportionsaleactivite = models.IntegerField(db_column='proportionSaleActivite')  # Field name made lowercase.
    proportionsaleactivitebonetat = models.IntegerField(db_column='proportionSaleActiviteBonEtat')  # Field name made lowercase.
    proportionsaleactiviteendure = models.IntegerField(db_column='proportionSaleActiviteEnDure')  # Field name made lowercase.
    proportionsaleactiviteenpaillefeuillage = models.IntegerField(db_column='proportionSaleActiviteEnPailleFeuillage')  # Field name made lowercase.
    proportionsaleactiviteenterrebattu = models.IntegerField(db_column='proportionSaleActiviteEnTerreBattu')  # Field name made lowercase.
    proportionsaleactivitesemidure = models.IntegerField(db_column='proportionSaleActiviteSemiDure')  # Field name made lowercase.
    proportionsallecoursecondaire = models.IntegerField(db_column='proportionSallecourSecondaire')  # Field name made lowercase.
    proportionsallecoursecondairecourbonetat = models.IntegerField(db_column='proportionSallecourSecondairecourbonetat')  # Field name made lowercase.
    proportionsallecoursecondairecourendur = models.IntegerField(db_column='proportionSallecourSecondairecourendur')  # Field name made lowercase.
    proportionsallecoursecondairecourpaillefeuillage = models.IntegerField(db_column='proportionSallecourSecondairecourpaillefeuillage')  # Field name made lowercase.
    proportionsallecoursecondairecoursemidur = models.IntegerField(db_column='proportionSallecourSecondairecoursemidur')  # Field name made lowercase.
    proportionsallecoursecondairecourterrebattue = models.IntegerField(db_column='proportionSallecourSecondairecourterrebattue')  # Field name made lowercase.
    proportioncour = models.IntegerField()
    proportioncourbonetat = models.IntegerField()
    proportioncourendur = models.IntegerField()
    proportioncourpaillefeuillage = models.IntegerField()
    proportioncoursemidur = models.IntegerField()
    proportioncourterrebattue = models.IntegerField()
    repartitionclassematernelautre = models.IntegerField(db_column='repartitionClasseMaternelAUTRE')  # Field name made lowercase.
    repartitionclassematernelecc = models.IntegerField(db_column='repartitionClasseMaternelECC')  # Field name made lowercase.
    repartitionclassematernelecf = models.IntegerField(db_column='repartitionClasseMaternelECF')  # Field name made lowercase.
    repartitionclassematerneleci = models.IntegerField(db_column='repartitionClasseMaternelECI')  # Field name made lowercase.
    repartitionclassematerneleck = models.IntegerField(db_column='repartitionClasseMaternelECK')  # Field name made lowercase.
    repartitionclassematernelecp = models.IntegerField(db_column='repartitionClasseMaternelECP')  # Field name made lowercase.
    repartitionclassematernelecs = models.IntegerField(db_column='repartitionClasseMaternelECS')  # Field name made lowercase.
    repartitionclassematernelenc = models.IntegerField(db_column='repartitionClasseMaternelENC')  # Field name made lowercase.
    repartitionclassematernelprive = models.IntegerField(db_column='repartitionClasseMaternelPRIVE')  # Field name made lowercase.
    repartitionclasseprimaireautre = models.IntegerField(db_column='repartitionClassePrimaireAUTRE')  # Field name made lowercase.
    repartitionclasseprimaireecc = models.IntegerField(db_column='repartitionClassePrimaireECC')  # Field name made lowercase.
    repartitionclasseprimaireecf = models.IntegerField(db_column='repartitionClassePrimaireECF')  # Field name made lowercase.
    repartitionclasseprimaireeci = models.IntegerField(db_column='repartitionClassePrimaireECI')  # Field name made lowercase.
    repartitionclasseprimaireeck = models.IntegerField(db_column='repartitionClassePrimaireECK')  # Field name made lowercase.
    repartitionclasseprimaireecp = models.IntegerField(db_column='repartitionClassePrimaireECP')  # Field name made lowercase.
    repartitionclasseprimaireecs = models.IntegerField(db_column='repartitionClassePrimaireECS')  # Field name made lowercase.
    repartitionclasseprimaireenc = models.IntegerField(db_column='repartitionClassePrimaireENC')  # Field name made lowercase.
    repartitionclasseprimaireprive = models.IntegerField(db_column='repartitionClassePrimairePRIVE')  # Field name made lowercase.
    repartitionclassesecondaireautre = models.IntegerField(db_column='repartitionClasseSecondaireAUTRE')  # Field name made lowercase.
    repartitionclassesecondaireecc = models.IntegerField(db_column='repartitionClasseSecondaireECC')  # Field name made lowercase.
    repartitionclassesecondaireecf = models.IntegerField(db_column='repartitionClasseSecondaireECF')  # Field name made lowercase.
    repartitionclassesecondaireeci = models.IntegerField(db_column='repartitionClasseSecondaireECI')  # Field name made lowercase.
    repartitionclassesecondaireeck = models.IntegerField(db_column='repartitionClasseSecondaireECK')  # Field name made lowercase.
    repartitionclassesecondaireecp = models.IntegerField(db_column='repartitionClasseSecondaireECP')  # Field name made lowercase.
    repartitionclassesecondaireecs = models.IntegerField(db_column='repartitionClasseSecondaireECS')  # Field name made lowercase.
    repartitionclassesecondaireenc = models.IntegerField(db_column='repartitionClasseSecondaireENC')  # Field name made lowercase.
    repartitionecolematernelautre = models.IntegerField(db_column='repartitionEcoleMaternelAUTRE')  # Field name made lowercase.
    repartitionecolematernelecc = models.IntegerField(db_column='repartitionEcoleMaternelECC')  # Field name made lowercase.
    repartitionecolematernelecf = models.IntegerField(db_column='repartitionEcoleMaternelECF')  # Field name made lowercase.
    repartitionecolematerneleci = models.IntegerField(db_column='repartitionEcoleMaternelECI')  # Field name made lowercase.
    repartitionecolematerneleck = models.IntegerField(db_column='repartitionEcoleMaternelECK')  # Field name made lowercase.
    repartitionecolematernelecp = models.IntegerField(db_column='repartitionEcoleMaternelECP')  # Field name made lowercase.
    repartitionecolematernelecs = models.IntegerField(db_column='repartitionEcoleMaternelECS')  # Field name made lowercase.
    repartitionecolematernelenc = models.IntegerField(db_column='repartitionEcoleMaternelENC')  # Field name made lowercase.
    repartitionecolematernelprive = models.IntegerField(db_column='repartitionEcoleMaternelPRIVE')  # Field name made lowercase.
    repartitionecoleprimaireautre = models.IntegerField(db_column='repartitionEcolePrimaireAUTRE')  # Field name made lowercase.
    repartitionecoleprimaireecc = models.IntegerField(db_column='repartitionEcolePrimaireECC')  # Field name made lowercase.
    repartitionecoleprimaireecf = models.IntegerField(db_column='repartitionEcolePrimaireECF')  # Field name made lowercase.
    repartitionecoleprimaireeci = models.IntegerField(db_column='repartitionEcolePrimaireECI')  # Field name made lowercase.
    repartitionecoleprimaireeck = models.IntegerField(db_column='repartitionEcolePrimaireECK')  # Field name made lowercase.
    repartitionecoleprimaireecp = models.IntegerField(db_column='repartitionEcolePrimaireECP')  # Field name made lowercase.
    repartitionecoleprimaireecs = models.IntegerField(db_column='repartitionEcolePrimaireECS')  # Field name made lowercase.
    repartitionecoleprimaireprive = models.IntegerField(db_column='repartitionEcolePrimairePRIVE')  # Field name made lowercase.
    repartitionecoleprimairelenc = models.IntegerField(db_column='repartitionEcolePrimairelENC')  # Field name made lowercase.
    repartitionecolesecondaireautre = models.IntegerField(db_column='repartitionEcoleSecondaireAUTRE')  # Field name made lowercase.
    repartitionecolesecondaireecc = models.IntegerField(db_column='repartitionEcoleSecondaireECC')  # Field name made lowercase.
    repartitionecolesecondaireecf = models.IntegerField(db_column='repartitionEcoleSecondaireECF')  # Field name made lowercase.
    repartitionecolesecondaireeci = models.IntegerField(db_column='repartitionEcoleSecondaireECI')  # Field name made lowercase.
    repartitionecolesecondaireeck = models.IntegerField(db_column='repartitionEcoleSecondaireECK')  # Field name made lowercase.
    repartitionecolesecondaireecp = models.IntegerField(db_column='repartitionEcoleSecondaireECP')  # Field name made lowercase.
    repartitionecolesecondaireecs = models.IntegerField(db_column='repartitionEcoleSecondaireECS')  # Field name made lowercase.
    repartitionecolesecondaireenc = models.IntegerField(db_column='repartitionEcoleSecondaireENC')  # Field name made lowercase.
    repartitioneducateurautre = models.IntegerField(db_column='repartitionEducateurAUTRE')  # Field name made lowercase.
    repartitioneducateurfemmematernelautre = models.IntegerField(db_column='repartitionEducateurFemmeMaternelAUTRE')  # Field name made lowercase.
    repartitioneducateurfemmematernelecc = models.IntegerField(db_column='repartitionEducateurFemmeMaternelECC')  # Field name made lowercase.
    repartitioneducateurfemmematernelecf = models.IntegerField(db_column='repartitionEducateurFemmeMaternelECF')  # Field name made lowercase.
    repartitioneducateurfemmematerneleci = models.IntegerField(db_column='repartitionEducateurFemmeMaternelECI')  # Field name made lowercase.
    repartitioneducateurfemmematerneleck = models.IntegerField(db_column='repartitionEducateurFemmeMaternelECK')  # Field name made lowercase.
    repartitioneducateurfemmematernelecp = models.IntegerField(db_column='repartitionEducateurFemmeMaternelECP')  # Field name made lowercase.
    repartitioneducateurfemmematernelecs = models.IntegerField(db_column='repartitionEducateurFemmeMaternelECS')  # Field name made lowercase.
    repartitioneducateurfemmematernelenc = models.IntegerField(db_column='repartitionEducateurFemmeMaternelENC')  # Field name made lowercase.
    repartitioneducateurfemmematernelprive = models.IntegerField(db_column='repartitionEducateurFemmeMaternelPRIVE')  # Field name made lowercase.
    repartitioneducateurfemmequalificationd6 = models.IntegerField(db_column='repartitionEducateurFemmeQualificationD6')  # Field name made lowercase.
    repartitioneducateurmaternelautre = models.IntegerField(db_column='repartitionEducateurMaternelAUTRE')  # Field name made lowercase.
    repartitioneducateurmaternelecc = models.IntegerField(db_column='repartitionEducateurMaternelECC')  # Field name made lowercase.
    repartitioneducateurmaternelecf = models.IntegerField(db_column='repartitionEducateurMaternelECF')  # Field name made lowercase.
    repartitioneducateurmaterneleci = models.IntegerField(db_column='repartitionEducateurMaternelECI')  # Field name made lowercase.
    repartitioneducateurmaterneleck = models.IntegerField(db_column='repartitionEducateurMaternelECK')  # Field name made lowercase.
    repartitioneducateurmaternelecp = models.IntegerField(db_column='repartitionEducateurMaternelECP')  # Field name made lowercase.
    repartitioneducateurmaternelecs = models.IntegerField(db_column='repartitionEducateurMaternelECS')  # Field name made lowercase.
    repartitioneducateurmaternelenc = models.IntegerField(db_column='repartitionEducateurMaternelENC')  # Field name made lowercase.
    repartitioneducateurmaternelprive = models.IntegerField(db_column='repartitionEducateurMaternelPRIVE')  # Field name made lowercase.
    repartitioneducateurprive = models.IntegerField(db_column='repartitionEducateurPRIVE')  # Field name made lowercase.
    repartitioneducateurqualificationd4 = models.IntegerField(db_column='repartitionEducateurQualificationD4')  # Field name made lowercase.
    repartitioneducateurqualificationem = models.IntegerField(db_column='repartitionEducateurQualificationEM')  # Field name made lowercase.
    repartitioneducateurqualificationg3a1 = models.IntegerField(db_column='repartitionEducateurQualificationG3A1')  # Field name made lowercase.
    repartitioneducateurqualificationmoind4 = models.IntegerField(db_column='repartitionEducateurQualificationMoinD4')  # Field name made lowercase.
    repartitioneducateurqualificationp6 = models.IntegerField(db_column='repartitionEducateurQualificationP6')  # Field name made lowercase.
    repartitioneleveinscritsecondaireautre = models.IntegerField(db_column='repartitionEleveinscritSecondaireAUTRE')  # Field name made lowercase.
    repartitioneleveinscritsecondaireecc = models.IntegerField(db_column='repartitionEleveinscritSecondaireECC')  # Field name made lowercase.
    repartitioneleveinscritsecondaireecf = models.IntegerField(db_column='repartitionEleveinscritSecondaireECF')  # Field name made lowercase.
    repartitioneleveinscritsecondaireeci = models.IntegerField(db_column='repartitionEleveinscritSecondaireECI')  # Field name made lowercase.
    repartitioneleveinscritsecondaireeck = models.IntegerField(db_column='repartitionEleveinscritSecondaireECK')  # Field name made lowercase.
    repartitioneleveinscritsecondaireecp = models.IntegerField(db_column='repartitionEleveinscritSecondaireECP')  # Field name made lowercase.
    repartitioneleveinscritsecondaireecs = models.IntegerField(db_column='repartitionEleveinscritSecondaireECS')  # Field name made lowercase.
    repartitioneleveinscritsecondaireenc = models.IntegerField(db_column='repartitionEleveinscritSecondaireENC')  # Field name made lowercase.
    repartitioneleveinscritsecondairefilleautre = models.IntegerField(db_column='repartitionEleveinscritSecondaireFilleAUTRE')  # Field name made lowercase.
    repartitioneleveinscritsecondairefilleecc = models.IntegerField(db_column='repartitionEleveinscritSecondaireFilleECC')  # Field name made lowercase.
    repartitioneleveinscritsecondairefilleecf = models.IntegerField(db_column='repartitionEleveinscritSecondaireFilleECF')  # Field name made lowercase.
    repartitioneleveinscritsecondairefilleeci = models.IntegerField(db_column='repartitionEleveinscritSecondaireFilleECI')  # Field name made lowercase.
    repartitioneleveinscritsecondairefilleeck = models.IntegerField(db_column='repartitionEleveinscritSecondaireFilleECK')  # Field name made lowercase.
    repartitioneleveinscritsecondairefilleecp = models.IntegerField(db_column='repartitionEleveinscritSecondaireFilleECP')  # Field name made lowercase.
    repartitioneleveinscritsecondairefilleecs = models.IntegerField(db_column='repartitionEleveinscritSecondaireFilleECS')  # Field name made lowercase.
    repartitioneleveinscritsecondairefilleenc = models.IntegerField(db_column='repartitionEleveinscritSecondaireFilleENC')  # Field name made lowercase.
    repartitioneleveinscrittypenseignementechnique = models.IntegerField(db_column='repartitionEleveinscritTypenseignemenTechnique')  # Field name made lowercase.
    repartitioneleveinscrittypenseignementartmetier = models.IntegerField(db_column='repartitionEleveinscritTypenseignementArtMetier')  # Field name made lowercase.
    repartitioneleveinscrittypenseignementgeneral = models.IntegerField(db_column='repartitionEleveinscritTypenseignementGeneral')  # Field name made lowercase.
    repartitioneleveinscrittypenseignementnormal = models.IntegerField(db_column='repartitionEleveinscritTypenseignementNormal')  # Field name made lowercase.
    repartitioneleveinscrittypenseignementprofessionel = models.IntegerField(db_column='repartitionEleveinscritTypenseignementProfessionel')  # Field name made lowercase.
    repartitionenfantfillematernelautre = models.IntegerField(db_column='repartitionEnfantFilleMaternelAUTRE')  # Field name made lowercase.
    repartitionenfantfillematernelecc = models.IntegerField(db_column='repartitionEnfantFilleMaternelECC')  # Field name made lowercase.
    repartitionenfantfillematernelecf = models.IntegerField(db_column='repartitionEnfantFilleMaternelECF')  # Field name made lowercase.
    repartitionenfantfillematerneleci = models.IntegerField(db_column='repartitionEnfantFilleMaternelECI')  # Field name made lowercase.
    repartitionenfantfillematerneleck = models.IntegerField(db_column='repartitionEnfantFilleMaternelECK')  # Field name made lowercase.
    repartitionenfantfillematernelecp = models.IntegerField(db_column='repartitionEnfantFilleMaternelECP')  # Field name made lowercase.
    repartitionenfantfillematernelecs = models.IntegerField(db_column='repartitionEnfantFilleMaternelECS')  # Field name made lowercase.
    repartitionenfantfillematernelenc = models.IntegerField(db_column='repartitionEnfantFilleMaternelENC')  # Field name made lowercase.
    repartitionenfantfillematernelprive = models.IntegerField(db_column='repartitionEnfantFilleMaternelPRIVE')  # Field name made lowercase.
    repartitionenfantmaternelautre = models.IntegerField(db_column='repartitionEnfantMaternelAUTRE')  # Field name made lowercase.
    repartitionenfantmaternelecc = models.IntegerField(db_column='repartitionEnfantMaternelECC')  # Field name made lowercase.
    repartitionenfantmaternelecf = models.IntegerField(db_column='repartitionEnfantMaternelECF')  # Field name made lowercase.
    repartitionenfantmaterneleci = models.IntegerField(db_column='repartitionEnfantMaternelECI')  # Field name made lowercase.
    repartitionenfantmaterneleck = models.IntegerField(db_column='repartitionEnfantMaternelECK')  # Field name made lowercase.
    repartitionenfantmaternelecp = models.IntegerField(db_column='repartitionEnfantMaternelECP')  # Field name made lowercase.
    repartitionenfantmaternelecs = models.IntegerField(db_column='repartitionEnfantMaternelECS')  # Field name made lowercase.
    repartitionenfantmaternelenc = models.IntegerField(db_column='repartitionEnfantMaternelENC')  # Field name made lowercase.
    repartitionenfantmaternelprive = models.IntegerField(db_column='repartitionEnfantMaternelPRIVE')  # Field name made lowercase.
    repartitionenfantprimaireautre = models.IntegerField(db_column='repartitionEnfantPrimaireAUTRE')  # Field name made lowercase.
    repartitionenfantprimaireecc = models.IntegerField(db_column='repartitionEnfantPrimaireECC')  # Field name made lowercase.
    repartitionenfantprimaireecf = models.IntegerField(db_column='repartitionEnfantPrimaireECF')  # Field name made lowercase.
    repartitionenfantprimaireeci = models.IntegerField(db_column='repartitionEnfantPrimaireECI')  # Field name made lowercase.
    repartitionenfantprimaireeck = models.IntegerField(db_column='repartitionEnfantPrimaireECK')  # Field name made lowercase.
    repartitionenfantprimaireecp = models.IntegerField(db_column='repartitionEnfantPrimaireECP')  # Field name made lowercase.
    repartitionenfantprimaireecs = models.IntegerField(db_column='repartitionEnfantPrimaireECS')  # Field name made lowercase.
    repartitionenfantprimaireenc = models.IntegerField(db_column='repartitionEnfantPrimaireENC')  # Field name made lowercase.
    repartitionenfantprimaireprive = models.IntegerField(db_column='repartitionEnfantPrimairePRIVE')  # Field name made lowercase.
    repartitionfilleinscritautre = models.IntegerField(db_column='repartitionFilleinscritAUTRE')  # Field name made lowercase.
    repartitionfilleinscritecc = models.IntegerField(db_column='repartitionFilleinscritECC')  # Field name made lowercase.
    repartitionfilleinscritecf = models.IntegerField(db_column='repartitionFilleinscritECF')  # Field name made lowercase.
    repartitionfilleinscriteci = models.IntegerField(db_column='repartitionFilleinscritECI')  # Field name made lowercase.
    repartitionfilleinscriteck = models.IntegerField(db_column='repartitionFilleinscritECK')  # Field name made lowercase.
    repartitionfilleinscritecp = models.IntegerField(db_column='repartitionFilleinscritECP')  # Field name made lowercase.
    repartitionfilleinscritecs = models.IntegerField(db_column='repartitionFilleinscritECS')  # Field name made lowercase.
    repartitionfilleinscritenc = models.IntegerField(db_column='repartitionFilleinscritENC')  # Field name made lowercase.
    repartitionfilleinscritepr = models.IntegerField(db_column='repartitionFilleinscritEPR')  # Field name made lowercase.
    repartitionfilleinscritprive = models.IntegerField(db_column='repartitionFilleinscritPRIVE')  # Field name made lowercase.
    repartitioninscriteleveautre = models.IntegerField(db_column='repartitionInscritEleveAUTRE')  # Field name made lowercase.
    repartitioninscriteleveecc = models.IntegerField(db_column='repartitionInscritEleveECC')  # Field name made lowercase.
    repartitioninscriteleveecf = models.IntegerField(db_column='repartitionInscritEleveECF')  # Field name made lowercase.
    repartitioninscriteleveeci = models.IntegerField(db_column='repartitionInscritEleveECI')  # Field name made lowercase.
    repartitioninscriteleveeck = models.IntegerField(db_column='repartitionInscritEleveECK')  # Field name made lowercase.
    repartitioninscriteleveecp = models.IntegerField(db_column='repartitionInscritEleveECP')  # Field name made lowercase.
    repartitioninscriteleveecs = models.IntegerField(db_column='repartitionInscritEleveECS')  # Field name made lowercase.
    repartitioninscriteleveenc = models.IntegerField(db_column='repartitionInscritEleveENC')  # Field name made lowercase.
    repartitioninscriteleveprive = models.IntegerField(db_column='repartitionInscritElevePRIVE')  # Field name made lowercase.
    repartitiontitulaireenseignaautre = models.IntegerField(db_column='repartitionTitulaireEnseignaAUTRE')  # Field name made lowercase.
    repartitiontitulaireenseignand4 = models.IntegerField(db_column='repartitionTitulaireEnseignanD4')  # Field name made lowercase.
    repartitiontitulaireenseignand6 = models.IntegerField(db_column='repartitionTitulaireEnseignanD6')  # Field name made lowercase.
    repartitiontitulaireenseignanmoind4 = models.IntegerField(db_column='repartitionTitulaireEnseignanMoinD4')  # Field name made lowercase.
    repartitiontitulaireenseignanp6 = models.IntegerField(db_column='repartitionTitulaireEnseignanP6')  # Field name made lowercase.
    repartitionpersonnelenseignanautre = models.IntegerField(db_column='repartitionpersonnelEnseignanAUTRE')  # Field name made lowercase.
    repartitionpersonnelenseignanecc = models.IntegerField(db_column='repartitionpersonnelEnseignanECC')  # Field name made lowercase.
    repartitionpersonnelenseignanecf = models.IntegerField(db_column='repartitionpersonnelEnseignanECF')  # Field name made lowercase.
    repartitionpersonnelenseignaneci = models.IntegerField(db_column='repartitionpersonnelEnseignanECI')  # Field name made lowercase.
    repartitionpersonnelenseignaneck = models.IntegerField(db_column='repartitionpersonnelEnseignanECK')  # Field name made lowercase.
    repartitionpersonnelenseignanecp = models.IntegerField(db_column='repartitionpersonnelEnseignanECP')  # Field name made lowercase.
    repartitionpersonnelenseignanecs = models.IntegerField(db_column='repartitionpersonnelEnseignanECS')  # Field name made lowercase.
    repartitionpersonnelenseignanenc = models.IntegerField(db_column='repartitionpersonnelEnseignanENC')  # Field name made lowercase.
    repartitionpersonnelenseignanprive = models.IntegerField(db_column='repartitionpersonnelEnseignanPRIVE')  # Field name made lowercase.
    repartitionpersonnelenseignansecondaireautre = models.IntegerField(db_column='repartitionpersonnelEnseignanSecondaireAUTRE')  # Field name made lowercase.
    repartitionpersonnelenseignansecondaireecc = models.IntegerField(db_column='repartitionpersonnelEnseignanSecondaireECC')  # Field name made lowercase.
    repartitionpersonnelenseignansecondaireecf = models.IntegerField(db_column='repartitionpersonnelEnseignanSecondaireECF')  # Field name made lowercase.
    repartitionpersonnelenseignansecondaireeci = models.IntegerField(db_column='repartitionpersonnelEnseignanSecondaireECI')  # Field name made lowercase.
    repartitionpersonnelenseignansecondaireeck = models.IntegerField(db_column='repartitionpersonnelEnseignanSecondaireECK')  # Field name made lowercase.
    repartitionpersonnelenseignansecondaireecp = models.IntegerField(db_column='repartitionpersonnelEnseignanSecondaireECP')  # Field name made lowercase.
    repartitionpersonnelenseignansecondaireecs = models.IntegerField(db_column='repartitionpersonnelEnseignanSecondaireECS')  # Field name made lowercase.
    repartitionpersonnelenseignansecondaireenc = models.IntegerField(db_column='repartitionpersonnelEnseignanSecondaireENC')  # Field name made lowercase.
    repartitionpersonnelenseignantqualificationa1 = models.IntegerField(db_column='repartitionpersonnelenseignantqualificationA1')  # Field name made lowercase.
    repartitionpersonnelenseignantqualificationautre = models.IntegerField(db_column='repartitionpersonnelenseignantqualificationAUTRE')  # Field name made lowercase.
    repartitionpersonnelenseignantqualificationd6 = models.IntegerField(db_column='repartitionpersonnelenseignantqualificationD6')  # Field name made lowercase.
    repartitionpersonnelenseignantqualificationdr = models.IntegerField(db_column='repartitionpersonnelenseignantqualificationDR')  # Field name made lowercase.
    repartitionpersonnelenseignantqualificationg3 = models.IntegerField(db_column='repartitionpersonnelenseignantqualificationG3')  # Field name made lowercase.
    repartitionpersonnelenseignantqualificationir = models.IntegerField(db_column='repartitionpersonnelenseignantqualificationIR')  # Field name made lowercase.
    repartitionpersonnelenseignantqualificationl2 = models.IntegerField(db_column='repartitionpersonnelenseignantqualificationL2')  # Field name made lowercase.
    repartitionpersonnelenseignantqualificationl2a = models.IntegerField(db_column='repartitionpersonnelenseignantqualificationL2A')  # Field name made lowercase.
    repartitionpersonnelenseignantqualificationla = models.IntegerField(db_column='repartitionpersonnelenseignantqualificationLA')  # Field name made lowercase.
    repartitionpersonnelenseignantqualificationmoind6p6 = models.IntegerField(db_column='repartitionpersonnelenseignantqualificationMoinD6P6')  # Field name made lowercase.
    repartitionpersonnelenseignantqualificationp6 = models.IntegerField(db_column='repartitionpersonnelenseignantqualificationP6')  # Field name made lowercase.
    tauxcouverture = models.FloatField(db_column='tauxCouverture')  # Field name made lowercase.
    etablissementid = models.BigIntegerField(db_column='etablissementId', blank=True, null=True)  # Field name made lowercase.
    id = models.BigAutoField(primary_key=True)
    provedid = models.BigIntegerField(db_column='provedId', blank=True, null=True)  # Field name made lowercase.
    provinceid = models.BigIntegerField(db_column='provinceId', blank=True, null=True)  # Field name made lowercase.
    sousprovedid = models.BigIntegerField(db_column='sousProvedId', blank=True, null=True)  # Field name made lowercase.
    etablissement = models.CharField(max_length=255, blank=True, null=True)
    proved = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    regimegestion = models.CharField(db_column='regimeGestion', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sousproved = models.CharField(db_column='sousProved', max_length=255, blank=True, null=True)  # Field name made lowercase.
    typeenseignement = models.CharField(db_column='typeEnseignement', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'annuaires'


class CelluleOrientationFormation(models.Model):
    cellule_orientation_evf = models.TextField(blank=True, null=True)  # This field type is a guess.
    enseignants_evf_formes = models.TextField(blank=True, null=True)  # This field type is a guess.
    form_st = models.ForeignKey('Formulaires', models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'cellule_orientation_formation'


class Cycle(models.Model):
    duree_annees = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    id = models.BigAutoField(primary_key=True)
    niveau = models.ForeignKey('NiveauEnseignement', models.DO_NOTHING, blank=True, null=True)
    updated_at = models.DateTimeField()
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cycle'


class DoublonsFormulaires(models.Model):
    id_a_garder = models.BigIntegerField(blank=True, null=True)
    ids_doublons = models.TextField(blank=True, null=True)
    nombre_doublons = models.BigIntegerField()
    idutilisateur = models.BigIntegerField(db_column='idUtilisateur', blank=True, null=True)  # Field name made lowercase.
    idannee = models.BigIntegerField(blank=True, null=True)
    idetablissement = models.BigIntegerField(blank=True, null=True)
    provedid = models.BigIntegerField(db_column='provedId', blank=True, null=True)  # Field name made lowercase.
    provinceid = models.BigIntegerField(db_column='provinceId', blank=True, null=True)  # Field name made lowercase.
    sousprovedid = models.BigIntegerField(db_column='sousProvedId', blank=True, null=True)  # Field name made lowercase.
    date = models.CharField(max_length=255, blank=True, null=True)
    nometab = models.CharField(db_column='nomEtab', max_length=255, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'doublons_formulaires'


class EcoleDigeGombe(models.Model):
    id = models.AutoField(primary_key=True)
    sous_division = models.CharField(max_length=191)
    nom_etablissement = models.CharField(max_length=255)
    numero_dinacope = models.CharField(max_length=64, blank=True, null=True)
    niveau = models.CharField(max_length=64, blank=True, null=True)
    regime_gestion = models.CharField(max_length=64, blank=True, null=True)
    quartier = models.CharField(max_length=128, blank=True, null=True)
    source_file = models.CharField(max_length=255, blank=True, null=True)
    imported_at = models.DateTimeField(blank=True, null=True)
    sousprovedid = models.BigIntegerField(db_column='sousProvedId')  # Field name made lowercase.
    provedid = models.BigIntegerField(db_column='provedId', blank=True, null=True)  # Field name made lowercase.
    provinceid = models.BigIntegerField(db_column='provinceId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ecole_dige_gombe'


class EcoleDigeGombeAutre(models.Model):
    id = models.AutoField(primary_key=True)
    sous_division = models.CharField(max_length=191)
    nom_etablissement = models.CharField(max_length=255)
    numero_dinacope = models.CharField(max_length=64, blank=True, null=True)
    niveau = models.CharField(max_length=64, blank=True, null=True)
    regime_gestion = models.CharField(max_length=64, blank=True, null=True)
    quartier = models.CharField(max_length=128, blank=True, null=True)
    source_file = models.CharField(max_length=255, blank=True, null=True)
    imported_at = models.DateTimeField(blank=True, null=True)
    sousprovedid = models.BigIntegerField(db_column='sousProvedId')  # Field name made lowercase.
    provedid = models.BigIntegerField(db_column='provedId', blank=True, null=True)  # Field name made lowercase.
    provinceid = models.BigIntegerField(db_column='provinceId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ecole_dige_gombe_autre'


class EducationEnvironnementale(models.Model):
    education_environnementale_discipline = models.TextField(blank=True, null=True)  # This field type is a guess.
    education_environnementale_enseigne = models.TextField(blank=True, null=True)  # This field type is a guess.
    education_environnementale_parascolaire = models.TextField(blank=True, null=True)  # This field type is a guess.
    education_environnementale_programme = models.TextField(blank=True, null=True)  # This field type is a guess.
    form_st = models.ForeignKey('Formulaires', models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'education_environnementale'


class Enseigants(models.Model):
    formstid = models.BigIntegerField(db_column='FormStId', blank=True, null=True)  # Field name made lowercase.
    id = models.BigAutoField(primary_key=True)
    enseignants = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'enseigants'


class Etablisement(models.Model):
    id = models.BigAutoField(primary_key=True)
    anneeid = models.ForeignKey(AnneeScolaire, models.DO_NOTHING, db_column='anneeId')  # Field name made lowercase.
    provinceid = models.ForeignKey('Provinces', models.DO_NOTHING, db_column='provinceId')  # Field name made lowercase.
    provedid = models.ForeignKey('Proveds', models.DO_NOTHING, db_column='provedId')  # Field name made lowercase.
    sousprovedid = models.ForeignKey('SousProved', models.DO_NOTHING, db_column='sousProvedId')  # Field name made lowercase.
    territoireid = models.BigIntegerField(db_column='territoireId', blank=True, null=True)  # Field name made lowercase.
    type_enseignement = models.CharField(max_length=50, blank=True, null=True)
    nometablissement = models.CharField(db_column='nomEtablissement', max_length=255)  # Field name made lowercase.
    nomchefetablissement = models.CharField(db_column='nomChefEtablissement', max_length=255, blank=True, null=True)  # Field name made lowercase.
    telephoneetablissement = models.CharField(db_column='telephoneEtablissement', max_length=50, blank=True, null=True)  # Field name made lowercase.
    adresseetablissement = models.CharField(db_column='adresseEtablissement', max_length=500, blank=True, null=True)  # Field name made lowercase.
    informations_generale = models.ForeignKey('InformationsGenerale', models.DO_NOTHING, blank=True, null=True)
    localisation_administrative = models.ForeignKey('LocalisationAdministrative', models.DO_NOTHING, blank=True, null=True)
    localisation_scolaire = models.ForeignKey('LocalisationScolaire', models.DO_NOTHING, blank=True, null=True)
    reference_juridique = models.ForeignKey('ReferenceJuridique', models.DO_NOTHING, blank=True, null=True)
    identification_id = models.BigIntegerField(blank=True, null=True)
    isactive = models.IntegerField(db_column='isActive', blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.IntegerField(db_column='isDeleted', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'etablisement'


class Etablissement(models.Model):
    id = models.BigAutoField(primary_key=True)
    anneeid = models.ForeignKey(AnneeScolaire, models.DO_NOTHING, db_column='anneeId')  # Field name made lowercase.
    nometablissement = models.CharField(db_column='nomEtablissement', max_length=255)  # Field name made lowercase.
    type_enseignement = models.CharField(max_length=50, blank=True, null=True)
    nomchefetablissement = models.CharField(db_column='nomChefEtablissement', max_length=255, blank=True, null=True)  # Field name made lowercase.
    adresseetablissement = models.CharField(db_column='adresseEtablissement', max_length=500, blank=True, null=True)  # Field name made lowercase.
    telephoneetablissement = models.CharField(db_column='telephoneEtablissement', max_length=50, blank=True, null=True)  # Field name made lowercase.
    provinceid = models.ForeignKey('Provinces', models.DO_NOTHING, db_column='provinceId')  # Field name made lowercase.
    provedid = models.ForeignKey('Proveds', models.DO_NOTHING, db_column='provedId')  # Field name made lowercase.
    sousprovedid = models.ForeignKey('SousProved', models.DO_NOTHING, db_column='sousProvedId')  # Field name made lowercase.
    informations_generale = models.ForeignKey('InformationsGenerale', models.DO_NOTHING, blank=True, null=True)
    localisation_administrative = models.ForeignKey('LocalisationAdministrative', models.DO_NOTHING, blank=True, null=True)
    localisation_scolaire = models.ForeignKey('LocalisationScolaire', models.DO_NOTHING, blank=True, null=True)
    territoireid = models.BigIntegerField(db_column='territoireId', blank=True, null=True)  # Field name made lowercase.
    reference_juridique = models.ForeignKey('ReferenceJuridique', models.DO_NOTHING, blank=True, null=True)
    identification_id = models.BigIntegerField(blank=True, null=True)
    isactive = models.IntegerField(db_column='isActive', blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.IntegerField(db_column='isDeleted', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    nom_norm = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'etablissement'


class EtablissementNiveaux(models.Model):
    etablissement_id = models.BigIntegerField()
    niveau = models.ForeignKey('NiveauEnseignement', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'etablissement_niveaux'


class EtablissementTypeEnseignement(models.Model):
    etablissement = models.ForeignKey(Etablissement, models.DO_NOTHING)
    type_enseignement = models.ForeignKey('TypeEnseignement', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'etablissement_type_enseignement'
        unique_together = (('etablissement', 'type_enseignement'),)


class EtablissementsSd(models.Model):
    id = models.BigAutoField(primary_key=True)
    sous_division = models.CharField(max_length=191)
    nom_etablissement = models.CharField(max_length=255)
    numero_dinacope = models.CharField(max_length=64, blank=True, null=True)
    niveau = models.CharField(max_length=64, blank=True, null=True)
    regime_gestion = models.CharField(max_length=64, blank=True, null=True)
    quartier = models.CharField(max_length=128, blank=True, null=True)
    source_file = models.CharField(max_length=255, blank=True, null=True)
    imported_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'etablissements_sd'


class Filieres(models.Model):
    effectifelevesf1h = models.IntegerField(db_column='effectifElevesF1H')  # Field name made lowercase.
    effectifelevesf2h = models.IntegerField(db_column='effectifElevesF2H')  # Field name made lowercase.
    effectifelevesf3h = models.IntegerField(db_column='effectifElevesF3H')  # Field name made lowercase.
    effectifelevesf4h = models.IntegerField(db_column='effectifElevesF4H')  # Field name made lowercase.
    effectifelevesf7 = models.IntegerField(db_column='effectifElevesF7')  # Field name made lowercase.
    effectifelevesf8 = models.IntegerField(db_column='effectifElevesF8')  # Field name made lowercase.
    effectifelevesg1h = models.IntegerField(db_column='effectifElevesG1H')  # Field name made lowercase.
    effectifelevesg2h = models.IntegerField(db_column='effectifElevesG2H')  # Field name made lowercase.
    effectifelevesg3h = models.IntegerField(db_column='effectifElevesG3H')  # Field name made lowercase.
    effectifelevesg4h = models.IntegerField(db_column='effectifElevesG4H')  # Field name made lowercase.
    effectifelevesg7 = models.IntegerField(db_column='effectifElevesG7')  # Field name made lowercase.
    effectifelevesg8 = models.IntegerField(db_column='effectifElevesG8')  # Field name made lowercase.
    form_st = models.ForeignKey('Formulaires', models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    nom = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'filieres'


class Formulaire(models.Model):
    id = models.BigAutoField(primary_key=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    responded = models.IntegerField()
    nometab = models.CharField(db_column='nomEtab', max_length=255, blank=True, null=True)  # Field name made lowercase.
    etablissement = models.ForeignKey(Etablissement, models.DO_NOTHING, blank=True, null=True)
    idannee = models.BigIntegerField(blank=True, null=True)
    provinceid = models.BigIntegerField(db_column='provinceId', blank=True, null=True)  # Field name made lowercase.
    provedid = models.BigIntegerField(db_column='provedId', blank=True, null=True)  # Field name made lowercase.
    sousprovedid = models.BigIntegerField(db_column='sousProvedId', blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(max_length=255, blank=True, null=True)
    idutilisateur = models.BigIntegerField(db_column='idUtilisateur', blank=True, null=True)  # Field name made lowercase.
    validated = models.IntegerField()
    validatedby = models.BigIntegerField(db_column='validatedBy', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(blank=True, null=True)
    idetablissement = models.BigIntegerField(blank=True, null=True)
    date = models.CharField(max_length=255, blank=True, null=True)
    identification_id = models.BigIntegerField(blank=True, null=True)
    corrected = models.IntegerField(blank=True, null=True)
    nom_norm = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'formulaire'
        unique_together = (('etablissement', 'idannee', 'sousprovedid', 'type'),)


class Formulaires(models.Model):
    id = models.BigAutoField(primary_key=True)
    updated_at = models.DateTimeField()
    responded = models.IntegerField()
    nometab = models.CharField(db_column='nomEtab', max_length=255, blank=True, null=True)  # Field name made lowercase.
    etablissement = models.ForeignKey(Etablissement, models.DO_NOTHING, blank=True, null=True)
    idannee = models.BigIntegerField(blank=True, null=True)
    provinceid = models.BigIntegerField(db_column='provinceId', blank=True, null=True)  # Field name made lowercase.
    provedid = models.BigIntegerField(db_column='provedId', blank=True, null=True)  # Field name made lowercase.
    sousprovedid = models.BigIntegerField(db_column='sousProvedId', blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(max_length=255, blank=True, null=True)
    idutilisateur = models.BigIntegerField(db_column='idUtilisateur', blank=True, null=True)  # Field name made lowercase.
    validated = models.IntegerField()
    validatedby = models.BigIntegerField(db_column='validatedBy', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField()
    idetablissement = models.BigIntegerField(blank=True, null=True)
    date = models.CharField(max_length=255, blank=True, null=True)
    identification_id = models.BigIntegerField(blank=True, null=True)
    nom_norm = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'formulaires'
        unique_together = (('etablissement', 'idannee', 'sousprovedid', 'type'),)


class Identification(models.Model):
    id = models.AutoField(primary_key=True)
    fk_annee_id = models.BigIntegerField(blank=True, null=True)
    fk_etab_id = models.BigIntegerField(blank=True, null=True)
    fk_centre_reg_id = models.BigIntegerField(blank=True, null=True)
    fk_province_id = models.BigIntegerField(blank=True, null=True)
    fk_proved_id = models.BigIntegerField(blank=True, null=True)
    code_centre_reg = models.CharField(max_length=255, blank=True, null=True)
    fk_territoire_id = models.BigIntegerField(blank=True, null=True)
    fk_ville_id = models.BigIntegerField(blank=True, null=True)
    sous_proved_id = models.BigIntegerField(blank=True, null=True)
    denomination = models.CharField(max_length=255, blank=True, null=True)
    adresse = models.CharField(max_length=191, blank=True, null=True)
    nom_chef_etab = models.CharField(max_length=191, blank=True, null=True)
    latitude = models.CharField(max_length=255, blank=True, null=True)
    longitude = models.CharField(max_length=255, blank=True, null=True)
    milieu = models.CharField(max_length=191, blank=True, null=True)
    ref_juridique = models.CharField(max_length=191, blank=True, null=True)
    num_secope = models.CharField(max_length=191, blank=True, null=True)
    stat_occup_parcel = models.CharField(max_length=191, blank=True, null=True)
    etab_est = models.CharField(max_length=191, blank=True, null=True)
    tel_chef_etab = models.CharField(max_length=150, blank=True, null=True)
    secteur_enseignement = models.CharField(max_length=150, blank=True, null=True)
    regime_gestion = models.CharField(max_length=6, blank=True, null=True)
    type_enseignement = models.CharField(max_length=3, blank=True, null=True)
    download = models.IntegerField(blank=True, null=True)
    submit = models.IntegerField(blank=True, null=True)
    finished = models.IntegerField(blank=True, null=True)
    altitude = models.CharField(max_length=255, blank=True, null=True)
    released_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    center = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.BigIntegerField(blank=True, null=True)
    remplissage = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'identification'


class Identifications(models.Model):
    download = models.TextField(blank=True, null=True)  # This field type is a guess.
    finished = models.TextField(blank=True, null=True)  # This field type is a guess.
    remplissage = models.IntegerField(blank=True, null=True)
    submit = models.TextField(blank=True, null=True)  # This field type is a guess.
    fk_annee_id = models.BigIntegerField(blank=True, null=True)
    fk_centre_reg_id = models.BigIntegerField(blank=True, null=True)
    fk_etab_id = models.BigIntegerField(blank=True, null=True)
    fk_proved_id = models.BigIntegerField(blank=True, null=True)
    fk_province_id = models.BigIntegerField(blank=True, null=True)
    fk_territoire_id = models.BigIntegerField(blank=True, null=True)
    fk_ville_id = models.BigIntegerField(blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    released_at = models.DateTimeField(blank=True, null=True)
    sous_proved_id = models.BigIntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    user_id = models.BigIntegerField(blank=True, null=True)
    secteur_enseignement = models.CharField(max_length=150, blank=True, null=True)
    tel_chef_etab = models.CharField(max_length=150, blank=True, null=True)
    adresse = models.CharField(max_length=191, blank=True, null=True)
    etab_est = models.CharField(max_length=191, blank=True, null=True)
    milieu = models.CharField(max_length=191, blank=True, null=True)
    nom_chef_etab = models.CharField(max_length=191, blank=True, null=True)
    num_secope = models.CharField(max_length=191, blank=True, null=True)
    ref_juridique = models.CharField(max_length=191, blank=True, null=True)
    stat_occup_parcel = models.CharField(max_length=191, blank=True, null=True)
    center = models.CharField(max_length=255, blank=True, null=True)
    code_centre_reg = models.CharField(max_length=255, blank=True, null=True)
    denomination = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.CharField(max_length=255, blank=True, null=True)
    longitude = models.CharField(max_length=255, blank=True, null=True)
    regime_gestion = models.CharField(max_length=255, blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    type_enseignement = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'identifications'


class InformationRelativePersonnel(models.Model):
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    anneedenaissance = models.CharField(db_column='AnneeDeNaissance', max_length=255, blank=True, null=True)  # Field name made lowercase.
    anneeengagement = models.CharField(db_column='AnneeEngagement', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fonction = models.CharField(db_column='Fonction', max_length=255, blank=True, null=True)  # Field name made lowercase.
    matriculesecope = models.CharField(db_column='MatriculeSecope', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nom = models.CharField(db_column='Nom', max_length=255, blank=True, null=True)  # Field name made lowercase.
    qualification = models.CharField(db_column='Qualification', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sexe = models.CharField(db_column='Sexe', max_length=255, blank=True, null=True)  # Field name made lowercase.
    situationsalariale = models.CharField(db_column='SituationSalariale', max_length=255, blank=True, null=True)  # Field name made lowercase.
    anneeetudes = models.CharField(db_column='AnneeEtudes', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'information_relative_personnel'


class InformationsGenerale(models.Model):
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    identification_id = models.BigIntegerField(blank=True, null=True)
    cloture = models.CharField(max_length=255, blank=True, null=True)
    coges = models.CharField(max_length=255, blank=True, null=True)
    coges_operationnel = models.CharField(max_length=255, blank=True, null=True)
    compartiments_filles = models.CharField(max_length=255, blank=True, null=True)
    copa = models.CharField(max_length=255, blank=True, null=True)
    copa_operationnel = models.CharField(max_length=255, blank=True, null=True)
    cour_recreation = models.CharField(max_length=255, blank=True, null=True)
    etablissement_pris_en_charge_programme_refugies = models.CharField(max_length=255, blank=True, null=True)
    internat = models.CharField(max_length=255, blank=True, null=True)
    latrines = models.CharField(max_length=255, blank=True, null=True)
    locaux_utilises = models.CharField(max_length=255, blank=True, null=True)
    nature_cloture = models.CharField(max_length=255, blank=True, null=True)
    nbr_femmes_dans_copa = models.CharField(max_length=255, blank=True, null=True)
    nbr_femmes_dans_coge = models.CharField(max_length=255, blank=True, null=True)
    nom_second_etablissement = models.CharField(max_length=255, blank=True, null=True)
    nombre_compartiments = models.CharField(max_length=255, blank=True, null=True)
    organisme_projet = models.CharField(max_length=255, blank=True, null=True)
    par_quel_organisme = models.CharField(max_length=255, blank=True, null=True)
    plan_action = models.CharField(max_length=255, blank=True, null=True)
    point_eau = models.CharField(max_length=255, blank=True, null=True)
    prevision_budgetaire = models.CharField(max_length=255, blank=True, null=True)
    programmes_officiels = models.CharField(max_length=255, blank=True, null=True)
    projet_etablissement = models.CharField(max_length=255, blank=True, null=True)
    reunions_pv = models.CharField(max_length=255, blank=True, null=True)
    reunions_rapport = models.CharField(max_length=255, blank=True, null=True)
    revue_performance = models.CharField(max_length=255, blank=True, null=True)
    sources_energie = models.CharField(max_length=255, blank=True, null=True)
    tableau_bord = models.CharField(max_length=255, blank=True, null=True)
    terrain_jeux = models.CharField(max_length=255, blank=True, null=True)
    type_point_eau = models.CharField(max_length=255, blank=True, null=True)
    type_sources_energie = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'informations_generale'


class InfosGeneralesEtab(models.Model):
    id = models.AutoField(primary_key=True)
    fk_annee_id = models.IntegerField(blank=True, null=True)
    fk_etab_id = models.IntegerField(blank=True, null=True)
    libelle_etab = models.TextField()
    type_enseignement = models.CharField(max_length=3, db_comment="Type d'enseignement")
    nbre_femme_dans_copa = models.IntegerField(blank=True, null=True)
    nbre_reunion_avec_rapports_annee_passee = models.IntegerField(blank=True, null=True)
    nbre_femmes_dans_coges = models.IntegerField(blank=True, null=True)
    nom2_etab = models.CharField(max_length=255, blank=True, null=True)
    type_point_eau = models.CharField(max_length=255, blank=True, null=True)
    nom_type_source_energie = models.CharField(max_length=255, blank=True, null=True)
    nbre_compart_latrine = models.IntegerField(blank=True, null=True)
    nature_cloture = models.CharField(max_length=255, blank=True, null=True)
    organisme_pris_en_charge_internat = models.CharField(max_length=255, blank=True, null=True)
    plan_action_operationel_exist = models.IntegerField(blank=True, null=True)
    nbre_enseign_form12_mois = models.IntegerField(blank=True, null=True)
    nbre_enseign_cote_positiv = models.IntegerField(blank=True, null=True)
    nbre_enseign_insp_pedag = models.IntegerField(blank=True, null=True)
    pv_reunion_etab_unite_peda_opera = models.IntegerField(blank=True, null=True)
    nbre_arbres_plantes = models.IntegerField(blank=True, null=True)
    nbre_femmes_enseign_recrutees_cette_annee = models.IntegerField(blank=True, null=True)
    nbre_enseign_suivi_format_peda_sens_genre = models.IntegerField(blank=True, null=True)
    nbre_reunions_avec_pvannee_passee = models.IntegerField(blank=True, null=True)
    released_at = models.DateTimeField(blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    nbre_latrine_pour_filles = models.IntegerField(blank=True, null=True)
    nom_program_pris_en_charge_internat = models.CharField(max_length=255, blank=True, null=True)
    pv_reunion_verif_pvd_et_dd = models.CharField(max_length=255, blank=True, null=True)
    nbre_ens_formes_adm1er_soin = models.IntegerField(blank=True, null=True)
    active_step = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    active_step_end = models.IntegerField(blank=True, null=True)
    finished = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    program_officiel = models.IntegerField(blank=True, null=True)
    copa = models.IntegerField(blank=True, null=True)
    copa_operationel = models.IntegerField(blank=True, null=True)
    coges_exist = models.IntegerField(blank=True, null=True)
    coges_operationel = models.IntegerField(blank=True, null=True)
    locaux_util2_etab = models.IntegerField(blank=True, null=True)
    point_eau_exist = models.IntegerField(blank=True, null=True)
    source_energy_exist = models.IntegerField(blank=True, null=True)
    latrine_exist = models.IntegerField(blank=True, null=True)
    cour_recre_exist = models.IntegerField(blank=True, null=True)
    terrain_jeux_exist = models.IntegerField(blank=True, null=True)
    cloture_exist = models.IntegerField(blank=True, null=True)
    internat_exist = models.IntegerField(blank=True, null=True)
    internat_pris_en_charge = models.IntegerField(blank=True, null=True)
    develop_projet_etab_avec_partie_prenantes = models.IntegerField(blank=True, null=True)
    prev_budget_et_docum_compt = models.IntegerField(blank=True, null=True)
    tab_de_bord_exist = models.IntegerField(blank=True, null=True)
    revue_annuel_perf_rap = models.IntegerField(blank=True, null=True)
    chef_format12_mois = models.IntegerField(blank=True, null=True)
    chef_cote_positivement = models.IntegerField(blank=True, null=True)
    activite_parascolaire_cette_annee = models.IntegerField(blank=True, null=True)
    etab_unite_peda_opera = models.IntegerField(blank=True, null=True)
    etab_manuel_proced_gest_ress_fin_mat_et_autre = models.IntegerField(blank=True, null=True)
    comm_plan_exist = models.IntegerField(blank=True, null=True)
    etab_particip_forum_echange_reseau_prox_rep = models.IntegerField(blank=True, null=True)
    dir_reseau_locaux_ope_rldexist = models.IntegerField(blank=True, null=True)
    chef_assist_res_loc_direct_rld = models.IntegerField(blank=True, null=True)
    arbres_exist = models.IntegerField(blank=True, null=True)
    coins_gestion_dechets_exist = models.IntegerField(blank=True, null=True)
    gouv_ope_dans_etab = models.IntegerField(blank=True, null=True)
    nom_organism_pris_etab_encharge = models.CharField(max_length=255, blank=True, null=True)
    fk_identification_id = models.IntegerField(blank=True, null=True)
    fk_province_id = models.IntegerField(blank=True, null=True)
    fk_proved_id = models.IntegerField(blank=True, null=True)
    fk_territoire_id = models.IntegerField(blank=True, null=True)
    fk_sous_proved_id = models.IntegerField(blank=True, null=True)
    type_point_eau_forage = models.CharField(max_length=255, blank=True, null=True)
    type_point_eau_source = models.CharField(max_length=255, blank=True, null=True)
    nom_type_source_energie_solaire = models.CharField(max_length=255, blank=True, null=True)
    nom_type_source_energie_groupe_elec = models.CharField(max_length=255, blank=True, null=True)
    submit = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'infos_generales_etab'


class InvalidFormsTmp(models.Model):
    id = models.BigIntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'invalid_forms_tmp'


class InventaireBanc(models.Model):
    banc_1_place_bon_etat = models.IntegerField(blank=True, null=True)
    banc_1_place_mauvais_etat = models.IntegerField(blank=True, null=True)
    banc_2_places_bon_etat = models.IntegerField(blank=True, null=True)
    banc_2_places_mauvais_etat = models.IntegerField(blank=True, null=True)
    banc_3_places_bon_etat = models.IntegerField(blank=True, null=True)
    banc_3_places_mauvais_etat = models.IntegerField(blank=True, null=True)
    banc_4_places_bon_etat = models.IntegerField(blank=True, null=True)
    banc_4_places_mauvais_etat = models.IntegerField(blank=True, null=True)
    banc_plus_4_places_bon_etat = models.IntegerField(blank=True, null=True)
    banc_plus_4_places_mauvais_etat = models.IntegerField(blank=True, null=True)
    total_bon_etat = models.IntegerField(blank=True, null=True)
    total_general = models.IntegerField(blank=True, null=True)
    total_mauvais_etat = models.IntegerField(blank=True, null=True)
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'inventaire_banc'


class LocalisationAdministrative(models.Model):
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    identification_id = models.BigIntegerField(blank=True, null=True)
    annee = models.CharField(max_length=255, blank=True, null=True)
    code_adm_ets = models.CharField(max_length=255, blank=True, null=True)
    code_adm_ets_auto = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    province_educationnelle = models.CharField(max_length=255, blank=True, null=True)
    secteur = models.CharField(max_length=255, blank=True, null=True)
    sous_division = models.CharField(max_length=255, blank=True, null=True)
    territoire = models.CharField(max_length=255, blank=True, null=True)
    territoire_commune = models.CharField(max_length=255, blank=True, null=True)
    village = models.CharField(max_length=255, blank=True, null=True)
    ville = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'localisation_administrative'


class LocalisationScolaire(models.Model):
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    identification_id = models.BigIntegerField(blank=True, null=True)
    altitude = models.CharField(max_length=255, blank=True, null=True)
    centre_regroupement = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.CharField(max_length=255, blank=True, null=True)
    longitude = models.CharField(max_length=255, blank=True, null=True)
    milieu = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'localisation_scolaire'


class MapEtabType(models.Model):
    etab_id = models.BigIntegerField()
    nom_norm = models.CharField(max_length=255)
    type_norm = models.CharField(max_length=50, blank=True, null=True)
    anneeid = models.BigIntegerField(db_column='anneeId')  # Field name made lowercase.
    sousprovedid = models.BigIntegerField(db_column='sousProvedId')  # Field name made lowercase.
    provedid = models.BigIntegerField(db_column='provedId')  # Field name made lowercase.
    provinceid = models.BigIntegerField(db_column='provinceId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'map_etab_type'


class NiveauEnseignement(models.Model):
    age_minimum = models.IntegerField(blank=True, null=True)
    duree_annees = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    id = models.BigAutoField(primary_key=True)
    updated_at = models.DateTimeField()
    code = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'niveau_enseignement'


class OptionCycle(models.Model):
    created_at = models.DateTimeField()
    cycle = models.ForeignKey(Cycle, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    updated_at = models.DateTimeField()
    nom = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'option_cycle'


class PersonnelEnseignant(models.Model):
    form_st_id = models.BigIntegerField(unique=True, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    chef_cote_positif = models.CharField(max_length=255, blank=True, null=True)
    chef_formation = models.CharField(max_length=255, blank=True, null=True)
    educateurs_cotes_positifs = models.CharField(max_length=255, blank=True, null=True)
    educateurs_formes = models.CharField(max_length=255, blank=True, null=True)
    educateurs_inspectes = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    etablissement_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'personnel_enseignant'


class Proveds(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    fk_province = models.ForeignKey('Provinces', models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    libelle = models.CharField(max_length=255, blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proveds'


class Provinces(models.Model):
    is_deleted = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField(blank=True, null=True)
    chef_lieu = models.CharField(max_length=255, blank=True, null=True)
    libelle = models.CharField(max_length=255, blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'provinces'


class ReferenceJuridique(models.Model):
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    identification_id = models.BigIntegerField(blank=True, null=True)
    etat_etablissement = models.CharField(max_length=255, blank=True, null=True)
    matricule_secope = models.CharField(max_length=255, blank=True, null=True)
    reference_juridique = models.CharField(max_length=255, blank=True, null=True)
    regime_gestion = models.CharField(max_length=255, blank=True, null=True)
    statut_occupation = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reference_juridique'


class RegimeGestion(models.Model):
    created_at = models.DateTimeField()
    id = models.BigAutoField(primary_key=True)
    updated_at = models.DateTimeField()
    code = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'regime_gestion'


class ReglementVigueur(models.Model):
    reglement_discrimination = models.TextField(blank=True, null=True)  # This field type is a guess.
    reglement_harcelement = models.TextField(blank=True, null=True)  # This field type is a guess.
    reglement_securite_physique = models.TextField(blank=True, null=True)  # This field type is a guess.
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'reglement_vigueur'


class Roles(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'roles'


class SanteSexuelleReproductive(models.Model):
    sante_reproductive_discipline = models.TextField(blank=True, null=True)  # This field type is a guess.
    sante_reproductive_enseigne = models.TextField(blank=True, null=True)  # This field type is a guess.
    sante_reproductive_parascolaire = models.TextField(blank=True, null=True)  # This field type is a guess.
    sante_reproductive_programme = models.TextField(blank=True, null=True)  # This field type is a guess.
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'sante_sexuelle_reproductive'


class Secteur(models.Model):
    created_at = models.DateTimeField()
    id = models.BigAutoField(primary_key=True)
    updated_at = models.DateTimeField()
    denomination = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'secteur'


class SensibilisationContreAbus(models.Model):
    sensibilisation_abus_discipline = models.TextField(blank=True, null=True)  # This field type is a guess.
    sensibilisation_abus_enseigne = models.TextField(blank=True, null=True)  # This field type is a guess.
    sensibilisation_abus_parascolaire = models.TextField(blank=True, null=True)  # This field type is a guess.
    sensibilisation_abus_programme = models.TextField(blank=True, null=True)  # This field type is a guess.
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'sensibilisation_contre_abus'


class SousProved(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    fk_proved = models.ForeignKey(Proveds, models.DO_NOTHING, blank=True, null=True)
    fk_territoire = models.ForeignKey('Territoires', models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    libelle = models.CharField(max_length=255, blank=True, null=True)
    lieu_implantation = models.CharField(max_length=255, blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sous_proved'


class St1EffectifsParAge(models.Model):
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    effectif_filles_3ans_1ere = models.CharField(max_length=255, blank=True, null=True)
    effectif_filles_3ans_2eme = models.CharField(max_length=255, blank=True, null=True)
    effectif_filles_3ans_3eme = models.CharField(max_length=255, blank=True, null=True)
    effectif_filles_4ans_1ere = models.CharField(max_length=255, blank=True, null=True)
    effectif_filles_4ans_2eme = models.CharField(max_length=255, blank=True, null=True)
    effectif_filles_4ans_3eme = models.CharField(max_length=255, blank=True, null=True)
    effectif_filles_5ans_1ere = models.CharField(max_length=255, blank=True, null=True)
    effectif_filles_5ans_2eme = models.CharField(max_length=255, blank=True, null=True)
    effectif_filles_5ans_3eme = models.CharField(max_length=255, blank=True, null=True)
    effectif_filles_moins_3ans_1ere = models.CharField(max_length=255, blank=True, null=True)
    effectif_filles_moins_3ans_2eme = models.CharField(max_length=255, blank=True, null=True)
    effectif_filles_moins_3ans_3eme = models.CharField(max_length=255, blank=True, null=True)
    effectif_filles_plus_5ans_1ere = models.CharField(max_length=255, blank=True, null=True)
    effectif_filles_plus_5ans_2eme = models.CharField(max_length=255, blank=True, null=True)
    effectif_filles_plus_5ans_3eme = models.CharField(max_length=255, blank=True, null=True)
    effectif_garcons_3ans_1ere = models.CharField(max_length=255, blank=True, null=True)
    effectif_garcons_3ans_2eme = models.CharField(max_length=255, blank=True, null=True)
    effectif_garcons_3ans_3eme = models.CharField(max_length=255, blank=True, null=True)
    effectif_garcons_4ans_1ere = models.CharField(max_length=255, blank=True, null=True)
    effectif_garcons_4ans_2eme = models.CharField(max_length=255, blank=True, null=True)
    effectif_garcons_4ans_3eme = models.CharField(max_length=255, blank=True, null=True)
    effectif_garcons_5ans_1ere = models.CharField(max_length=255, blank=True, null=True)
    effectif_garcons_5ans_2eme = models.CharField(max_length=255, blank=True, null=True)
    effectif_garcons_5ans_3eme = models.CharField(max_length=255, blank=True, null=True)
    effectif_garcons_moins_3ans_1ere = models.CharField(max_length=255, blank=True, null=True)
    effectif_garcons_moins_3ans_2eme = models.CharField(max_length=255, blank=True, null=True)
    effectif_garcons_moins_3ans_3eme = models.CharField(max_length=255, blank=True, null=True)
    effectif_garcons_plus_5ans_1ere = models.CharField(max_length=255, blank=True, null=True)
    effectif_garcons_plus_5ans_2eme = models.CharField(max_length=255, blank=True, null=True)
    effectif_garcons_plus_5ans_3eme = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'st1_effectifs_par_age'


class St1Enseignant(models.Model):
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    enseignants_autres_femmes_1ere = models.CharField(max_length=255, blank=True, null=True)
    enseignants_autres_femmes_2eme = models.CharField(max_length=255, blank=True, null=True)
    enseignants_autres_femmes_3eme = models.CharField(max_length=255, blank=True, null=True)
    enseignants_autres_hommes_1ere = models.CharField(max_length=255, blank=True, null=True)
    enseignants_autres_hommes_2eme = models.CharField(max_length=255, blank=True, null=True)
    enseignants_autres_hommes_3eme = models.CharField(max_length=255, blank=True, null=True)
    enseignants_d4_femmes_1ere = models.CharField(max_length=255, blank=True, null=True)
    enseignants_d4_femmes_2eme = models.CharField(max_length=255, blank=True, null=True)
    enseignants_d4_femmes_3eme = models.CharField(max_length=255, blank=True, null=True)
    enseignants_d4_hommes_1ere = models.CharField(max_length=255, blank=True, null=True)
    enseignants_d4_hommes_2eme = models.CharField(max_length=255, blank=True, null=True)
    enseignants_d4_hommes_3eme = models.CharField(max_length=255, blank=True, null=True)
    enseignants_d4p_femmes_1ere = models.CharField(max_length=255, blank=True, null=True)
    enseignants_d4p_femmes_2eme = models.CharField(max_length=255, blank=True, null=True)
    enseignants_d4p_femmes_3eme = models.CharField(max_length=255, blank=True, null=True)
    enseignants_d4p_hommes_1ere = models.CharField(max_length=255, blank=True, null=True)
    enseignants_d4p_hommes_2eme = models.CharField(max_length=255, blank=True, null=True)
    enseignants_d4p_hommes_3eme = models.CharField(max_length=255, blank=True, null=True)
    enseignants_d6_femmes_1ere = models.CharField(max_length=255, blank=True, null=True)
    enseignants_d6_femmes_2eme = models.CharField(max_length=255, blank=True, null=True)
    enseignants_d6_femmes_3eme = models.CharField(max_length=255, blank=True, null=True)
    enseignants_d6_hommes_1ere = models.CharField(max_length=255, blank=True, null=True)
    enseignants_d6_hommes_2eme = models.CharField(max_length=255, blank=True, null=True)
    enseignants_d6_hommes_3eme = models.CharField(max_length=255, blank=True, null=True)
    enseignants_em_femmes_1ere = models.CharField(max_length=255, blank=True, null=True)
    enseignants_em_femmes_2eme = models.CharField(max_length=255, blank=True, null=True)
    enseignants_em_femmes_3eme = models.CharField(max_length=255, blank=True, null=True)
    enseignants_em_hommes_1ere = models.CharField(max_length=255, blank=True, null=True)
    enseignants_em_hommes_2eme = models.CharField(max_length=255, blank=True, null=True)
    enseignants_em_hommes_3eme = models.CharField(max_length=255, blank=True, null=True)
    enseignants_p6_femmes_1ere = models.CharField(max_length=255, blank=True, null=True)
    enseignants_p6_femmes_2eme = models.CharField(max_length=255, blank=True, null=True)
    enseignants_p6_femmes_3eme = models.CharField(max_length=255, blank=True, null=True)
    enseignants_p6_hommes_1ere = models.CharField(max_length=255, blank=True, null=True)
    enseignants_p6_hommes_2eme = models.CharField(max_length=255, blank=True, null=True)
    enseignants_p6_hommes_3eme = models.CharField(max_length=255, blank=True, null=True)
    personnel_eligible_retraite = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'st1_enseignant'


class St1GroupesSpecifiques(models.Model):
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    autochtones_filles_1ere = models.CharField(max_length=255, blank=True, null=True)
    autochtones_filles_2eme = models.CharField(max_length=255, blank=True, null=True)
    autochtones_filles_3eme = models.CharField(max_length=255, blank=True, null=True)
    autochtones_garcons_1ere = models.CharField(max_length=255, blank=True, null=True)
    autochtones_garcons_2eme = models.CharField(max_length=255, blank=True, null=True)
    autochtones_garcons_3eme = models.CharField(max_length=255, blank=True, null=True)
    deplaces_externes_filles_1ere = models.CharField(max_length=255, blank=True, null=True)
    deplaces_externes_filles_2eme = models.CharField(max_length=255, blank=True, null=True)
    deplaces_externes_filles_3eme = models.CharField(max_length=255, blank=True, null=True)
    deplaces_externes_garcons_1ere = models.CharField(max_length=255, blank=True, null=True)
    deplaces_externes_garcons_2eme = models.CharField(max_length=255, blank=True, null=True)
    deplaces_externes_garcons_3eme = models.CharField(max_length=255, blank=True, null=True)
    deplaces_internes_filles_1ere = models.CharField(max_length=255, blank=True, null=True)
    deplaces_internes_filles_2eme = models.CharField(max_length=255, blank=True, null=True)
    deplaces_internes_filles_3eme = models.CharField(max_length=255, blank=True, null=True)
    deplaces_internes_garcons_1ere = models.CharField(max_length=255, blank=True, null=True)
    deplaces_internes_garcons_2eme = models.CharField(max_length=255, blank=True, null=True)
    deplaces_internes_garcons_3eme = models.CharField(max_length=255, blank=True, null=True)
    etrangers_filles_1ere = models.CharField(max_length=255, blank=True, null=True)
    etrangers_filles_2eme = models.CharField(max_length=255, blank=True, null=True)
    etrangers_filles_3eme = models.CharField(max_length=255, blank=True, null=True)
    etrangers_garcons_1ere = models.CharField(max_length=255, blank=True, null=True)
    etrangers_garcons_2eme = models.CharField(max_length=255, blank=True, null=True)
    etrangers_garcons_3eme = models.CharField(max_length=255, blank=True, null=True)
    handicaps_filles_1ere = models.CharField(max_length=255, blank=True, null=True)
    handicaps_filles_2eme = models.CharField(max_length=255, blank=True, null=True)
    handicaps_filles_3eme = models.CharField(max_length=255, blank=True, null=True)
    handicaps_garcons_1ere = models.CharField(max_length=255, blank=True, null=True)
    handicaps_garcons_2eme = models.CharField(max_length=255, blank=True, null=True)
    handicaps_garcons_3eme = models.CharField(max_length=255, blank=True, null=True)
    orphelins_filles_1ere = models.CharField(max_length=255, blank=True, null=True)
    orphelins_filles_2eme = models.CharField(max_length=255, blank=True, null=True)
    orphelins_filles_3eme = models.CharField(max_length=255, blank=True, null=True)
    orphelins_garcons_1ere = models.CharField(max_length=255, blank=True, null=True)
    orphelins_garcons_2eme = models.CharField(max_length=255, blank=True, null=True)
    orphelins_garcons_3eme = models.CharField(max_length=255, blank=True, null=True)
    refugies_filles_1ere = models.CharField(max_length=255, blank=True, null=True)
    refugies_filles_2eme = models.CharField(max_length=255, blank=True, null=True)
    refugies_filles_3eme = models.CharField(max_length=255, blank=True, null=True)
    refugies_garcons_1ere = models.CharField(max_length=255, blank=True, null=True)
    refugies_garcons_2eme = models.CharField(max_length=255, blank=True, null=True)
    refugies_garcons_3eme = models.CharField(max_length=255, blank=True, null=True)
    reintegrants_filles_1ere = models.CharField(max_length=255, blank=True, null=True)
    reintegrants_filles_2eme = models.CharField(max_length=255, blank=True, null=True)
    reintegrants_filles_3eme = models.CharField(max_length=255, blank=True, null=True)
    reintegrants_garcons_1ere = models.CharField(max_length=255, blank=True, null=True)
    reintegrants_garcons_2eme = models.CharField(max_length=255, blank=True, null=True)
    reintegrants_garcons_3eme = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'st1_groupes_specifiques'


class St1GuidesEducateurs(models.Model):
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    guides_autres_1ere = models.CharField(max_length=255, blank=True, null=True)
    guides_autres_2eme = models.CharField(max_length=255, blank=True, null=True)
    guides_autres_3eme = models.CharField(max_length=255, blank=True, null=True)
    guides_comptage_1ere = models.CharField(max_length=255, blank=True, null=True)
    guides_comptage_2eme = models.CharField(max_length=255, blank=True, null=True)
    guides_comptage_3eme = models.CharField(max_length=255, blank=True, null=True)
    guides_etude_du_milieu_1ere = models.CharField(max_length=255, blank=True, null=True)
    guides_etude_du_milieu_2eme = models.CharField(max_length=255, blank=True, null=True)
    guides_etude_du_milieu_3eme = models.CharField(max_length=255, blank=True, null=True)
    guides_eveil_1ere = models.CharField(max_length=255, blank=True, null=True)
    guides_eveil_2eme = models.CharField(max_length=255, blank=True, null=True)
    guides_eveil_3eme = models.CharField(max_length=255, blank=True, null=True)
    guides_francais_1ere = models.CharField(max_length=255, blank=True, null=True)
    guides_francais_2eme = models.CharField(max_length=255, blank=True, null=True)
    guides_francais_3eme = models.CharField(max_length=255, blank=True, null=True)
    guides_themes_transversaux_1ere = models.CharField(max_length=255, blank=True, null=True)
    guides_themes_transversaux_2eme = models.CharField(max_length=255, blank=True, null=True)
    guides_themes_transversaux_3eme = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'st1_guides_educateurs'


class St1Infrastructure(models.Model):
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    nb_salles_autorisees_1ere = models.CharField(max_length=255, blank=True, null=True)
    nb_salles_autorisees_2eme = models.CharField(max_length=255, blank=True, null=True)
    nb_salles_autorisees_3eme = models.CharField(max_length=255, blank=True, null=True)
    nb_salles_organisees_1ere = models.CharField(max_length=255, blank=True, null=True)
    nb_salles_organisees_2eme = models.CharField(max_length=255, blank=True, null=True)
    nb_salles_organisees_3eme = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'st1_infrastructure'


class St1Locaux(models.Model):
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    bureau_dur_bon = models.CharField(max_length=255, blank=True, null=True)
    bureau_dur_mauvais = models.CharField(max_length=255, blank=True, null=True)
    bureau_paille_bon = models.CharField(max_length=255, blank=True, null=True)
    bureau_paille_mauvais = models.CharField(max_length=255, blank=True, null=True)
    bureau_semidur_bon = models.CharField(max_length=255, blank=True, null=True)
    bureau_semidur_mauvais = models.CharField(max_length=255, blank=True, null=True)
    bureau_terre_bon = models.CharField(max_length=255, blank=True, null=True)
    bureau_terre_mauvais = models.CharField(max_length=255, blank=True, null=True)
    magasin_dur_bon = models.CharField(max_length=255, blank=True, null=True)
    magasin_dur_mauvais = models.CharField(max_length=255, blank=True, null=True)
    magasin_paille_bon = models.CharField(max_length=255, blank=True, null=True)
    magasin_paille_mauvais = models.CharField(max_length=255, blank=True, null=True)
    magasin_semidur_bon = models.CharField(max_length=255, blank=True, null=True)
    magasin_semidur_mauvais = models.CharField(max_length=255, blank=True, null=True)
    magasin_terre_bon = models.CharField(max_length=255, blank=True, null=True)
    magasin_terre_mauvais = models.CharField(max_length=255, blank=True, null=True)
    salle_activites_detruits = models.CharField(max_length=255, blank=True, null=True)
    salle_activites_dur_bon = models.CharField(max_length=255, blank=True, null=True)
    salle_activites_dur_mauvais = models.CharField(max_length=255, blank=True, null=True)
    salle_activites_paille_bon = models.CharField(max_length=255, blank=True, null=True)
    salle_activites_paille_mauvais = models.CharField(max_length=255, blank=True, null=True)
    salle_activites_semidur_bon = models.CharField(max_length=255, blank=True, null=True)
    salle_activites_semidur_mauvais = models.CharField(max_length=255, blank=True, null=True)
    salle_activites_terre_bon = models.CharField(max_length=255, blank=True, null=True)
    salle_activites_terre_mauvais = models.CharField(max_length=255, blank=True, null=True)
    salle_attente_dur_bon = models.CharField(max_length=255, blank=True, null=True)
    salle_attente_dur_mauvais = models.CharField(max_length=255, blank=True, null=True)
    salle_attente_paille_bon = models.CharField(max_length=255, blank=True, null=True)
    salle_attente_paille_mauvais = models.CharField(max_length=255, blank=True, null=True)
    salle_attente_semidur_bon = models.CharField(max_length=255, blank=True, null=True)
    salle_attente_semidur_mauvais = models.CharField(max_length=255, blank=True, null=True)
    salle_attente_terre_bon = models.CharField(max_length=255, blank=True, null=True)
    salle_attente_terre_mauvais = models.CharField(max_length=255, blank=True, null=True)
    salle_jeux_dur_bon = models.CharField(max_length=255, blank=True, null=True)
    salle_jeux_dur_mauvais = models.CharField(max_length=255, blank=True, null=True)
    salle_jeux_paille_bon = models.CharField(max_length=255, blank=True, null=True)
    salle_jeux_paille_mauvais = models.CharField(max_length=255, blank=True, null=True)
    salle_jeux_semidur_bon = models.CharField(max_length=255, blank=True, null=True)
    salle_jeux_semidur_mauvais = models.CharField(max_length=255, blank=True, null=True)
    salle_jeux_terre_bon = models.CharField(max_length=255, blank=True, null=True)
    salle_jeux_terre_mauvais = models.CharField(max_length=255, blank=True, null=True)
    salle_repos_dur_bon = models.CharField(max_length=255, blank=True, null=True)
    salle_repos_dur_mauvais = models.CharField(max_length=255, blank=True, null=True)
    salle_repos_paille_bon = models.CharField(max_length=255, blank=True, null=True)
    salle_repos_paille_mauvais = models.CharField(max_length=255, blank=True, null=True)
    salle_repos_semidur_bon = models.CharField(max_length=255, blank=True, null=True)
    salle_repos_semidur_mauvais = models.CharField(max_length=255, blank=True, null=True)
    salle_repos_terre_bon = models.CharField(max_length=255, blank=True, null=True)
    salle_repos_terre_mauvais = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'st1_locaux'


class St1ManuelsEnfants(models.Model):
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    manuels_autres_1ere = models.CharField(max_length=255, blank=True, null=True)
    manuels_autres_2eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_autres_3eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_comptage_1ere = models.CharField(max_length=255, blank=True, null=True)
    manuels_comptage_2eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_comptage_3eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_etude_du_milieu_1ere = models.CharField(max_length=255, blank=True, null=True)
    manuels_etude_du_milieu_2eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_etude_du_milieu_3eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_eveil_1ere = models.CharField(max_length=255, blank=True, null=True)
    manuels_eveil_2eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_eveil_3eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_francais_1ere = models.CharField(max_length=255, blank=True, null=True)
    manuels_francais_2eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_francais_3eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_themes_transversaux_1ere = models.CharField(max_length=255, blank=True, null=True)
    manuels_themes_transversaux_2eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_themes_transversaux_3eme = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'st1_manuels_enfants'


class St1PersonnelAdministratif(models.Model):
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    autres_directeur_adjoint_f = models.CharField(max_length=255, blank=True, null=True)
    autres_directeur_adjoint_h = models.CharField(max_length=255, blank=True, null=True)
    autres_directeur_f = models.CharField(max_length=255, blank=True, null=True)
    autres_directeur_h = models.CharField(max_length=255, blank=True, null=True)
    autres_ouvrier_f = models.CharField(max_length=255, blank=True, null=True)
    autres_ouvrier_h = models.CharField(max_length=255, blank=True, null=True)
    autres_surveillant_f = models.CharField(max_length=255, blank=True, null=True)
    autres_surveillant_h = models.CharField(max_length=255, blank=True, null=True)
    d4_directeur_adjoint_f = models.CharField(max_length=255, blank=True, null=True)
    d4_directeur_adjoint_h = models.CharField(max_length=255, blank=True, null=True)
    d4_directeur_f = models.CharField(max_length=255, blank=True, null=True)
    d4_directeur_h = models.CharField(max_length=255, blank=True, null=True)
    d4_ouvrier_f = models.CharField(max_length=255, blank=True, null=True)
    d4_ouvrier_h = models.CharField(max_length=255, blank=True, null=True)
    d4_surveillant_f = models.CharField(max_length=255, blank=True, null=True)
    d4_surveillant_h = models.CharField(max_length=255, blank=True, null=True)
    d6_directeur_adjoint_f = models.CharField(max_length=255, blank=True, null=True)
    d6_directeur_adjoint_h = models.CharField(max_length=255, blank=True, null=True)
    d6_directeur_f = models.CharField(max_length=255, blank=True, null=True)
    d6_directeur_h = models.CharField(max_length=255, blank=True, null=True)
    d6_ouvrier_f = models.CharField(max_length=255, blank=True, null=True)
    d6_ouvrier_h = models.CharField(max_length=255, blank=True, null=True)
    d6_surveillant_f = models.CharField(max_length=255, blank=True, null=True)
    d6_surveillant_h = models.CharField(max_length=255, blank=True, null=True)
    em_directeur_adjoint_f = models.CharField(max_length=255, blank=True, null=True)
    em_directeur_adjoint_h = models.CharField(max_length=255, blank=True, null=True)
    em_directeur_f = models.CharField(max_length=255, blank=True, null=True)
    em_directeur_h = models.CharField(max_length=255, blank=True, null=True)
    em_ouvrier_f = models.CharField(max_length=255, blank=True, null=True)
    em_ouvrier_h = models.CharField(max_length=255, blank=True, null=True)
    em_surveillant_f = models.CharField(max_length=255, blank=True, null=True)
    em_surveillant_h = models.CharField(max_length=255, blank=True, null=True)
    p6_directeur_adjoint_f = models.CharField(max_length=255, blank=True, null=True)
    p6_directeur_adjoint_h = models.CharField(max_length=255, blank=True, null=True)
    p6_directeur_f = models.CharField(max_length=255, blank=True, null=True)
    p6_directeur_h = models.CharField(max_length=255, blank=True, null=True)
    p6_ouvrier_f = models.CharField(max_length=255, blank=True, null=True)
    p6_ouvrier_h = models.CharField(max_length=255, blank=True, null=True)
    p6_surveillant_f = models.CharField(max_length=255, blank=True, null=True)
    p6_surveillant_h = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'st1_personnel_administratif'


class St2ClassesAutoriseesEtOrganisees(models.Model):
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    st2_nombre_classes_autorise_0 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_classes_autorise_1 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_classes_autorise_2 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_classes_autorise_3 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_classes_autorise_4 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_classes_autorise_5 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_classes_autorise_6 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_classes_organise_0 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_classes_organise_1 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_classes_organise_2 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_classes_organise_3 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_classes_organise_4 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_classes_organise_5 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_classes_organise_6 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'st2_classes_autorisees_et_organisees'


class St2EffectifsElevesCinquieme(models.Model):
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    st2_nombre_cinquieme_f_10 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_cinquieme_f_11 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_cinquieme_f_8 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_cinquieme_f_9 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_cinquieme_f_dont_autochtone = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_cinquieme_f_dont_avec_handicap = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_cinquieme_f_dont_deplaces = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_cinquieme_f_dont_etrangers = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_cinquieme_f_dont_internants = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_cinquieme_f_dont_orphelins = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_cinquieme_f_dont_redoublons = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_cinquieme_f_dont_refugies = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_cinquieme_f_dont_reintegrants = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_cinquieme_f_plus11 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_cinquieme_g_10 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_cinquieme_g_11 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_cinquieme_g_8 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_cinquieme_g_9 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_cinquieme_g_dont_autochtone = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_cinquieme_g_dont_avec_handicap = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_cinquieme_g_dont_deplaces = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_cinquieme_g_dont_etrangers = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_cinquieme_g_dont_internants = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_cinquieme_g_dont_orphelins = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_cinquieme_g_dont_redoublons = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_cinquieme_g_dont_refugies = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_cinquieme_g_dont_reintegrants = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_cinquieme_g_plus11 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'st2_effectifs_eleves_cinquieme'


class St2EffectifsElevesDeuxieme(models.Model):
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    st2_nombre_deuxieme_f_10 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_f_11 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_f_6 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_f_7 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_f_8 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_f_9 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_f_dont_autochtone = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_f_dont_avec_handicap = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_f_dont_deplaces = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_f_dont_etrangers = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_f_dont_internants = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_f_dont_orphelins = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_f_dont_redoublons = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_f_dont_refugies = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_f_dont_reintegrants = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_f_moins6 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_f_plus11 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_g_10 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_g_11 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_g_6 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_g_7 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_g_8 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_g_9 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_g_dont_autochtone = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_g_dont_avec_handicap = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_g_dont_deplaces = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_g_dont_etrangers = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_g_dont_internants = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_g_dont_orphelins = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_g_dont_redoublons = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_g_dont_refugies = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_g_dont_reintegrants = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_g_moins6 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_deuxieme_g_plus11 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'st2_effectifs_eleves_deuxieme'


class St2EffectifsElevesPremiere(models.Model):
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    st2_nombre_premiere_f_10 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_f_11 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_f_6 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_f_7 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_f_8 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_f_9 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_f_dont_autochtone = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_f_dont_avec_handicap = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_f_dont_deplaces = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_f_dont_etrangers = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_f_dont_internants = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_f_dont_orphelins = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_f_dont_redoublons = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_f_dont_refugies = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_f_dont_reintegrants = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_f_moins6 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_f_plus11 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_g_10 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_g_11 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_g_6 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_g_7 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_g_8 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_g_9 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_g_dont_autochtone = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_g_dont_avec_handicap = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_g_dont_deplaces = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_g_dont_etrangers = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_g_dont_internants = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_g_dont_orphelins = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_g_dont_redoublons = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_g_dont_refugies = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_g_dont_reintegrants = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_g_moins6 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_premiere_g_plus11 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'st2_effectifs_eleves_premiere'


class St2EffectifsElevesPreprimaire(models.Model):
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    st2_nombre_preprimaire_f_10 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_f_11 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_f_6 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_f_7 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_f_8 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_f_9 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_f_dont_autochtone = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_f_dont_avec_handicap = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_f_dont_deplaces = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_f_dont_etrangers = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_f_dont_internants = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_f_dont_orphelins = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_f_dont_redoublons = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_f_dont_refugies = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_f_dont_reintegrants = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_f_moins6 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_f_plus11 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_g_10 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_g_11 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_g_6 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_g_7 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_g_8 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_g_9 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_g_dont_autochtone = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_g_dont_avec_handicap = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_g_dont_deplaces = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_g_dont_etrangers = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_g_dont_internants = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_g_dont_orphelins = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_g_dont_redoublons = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_g_dont_refugies = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_g_dont_reintegrants = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_g_moins6 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_preprimaire_g_plus11 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'st2_effectifs_eleves_preprimaire'


class St2EffectifsElevesQuatrieme(models.Model):
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    st2_nombre_quatrieme_f_10 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_quatrieme_f_11 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_quatrieme_f_7 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_quatrieme_f_8 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_quatrieme_f_9 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_quatrieme_f_dont_autochtone = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_quatrieme_f_dont_avec_handicap = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_quatrieme_f_dont_deplaces = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_quatrieme_f_dont_etrangers = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_quatrieme_f_dont_internants = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_quatrieme_f_dont_orphelins = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_quatrieme_f_dont_redoublons = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_quatrieme_f_dont_refugies = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_quatrieme_f_dont_reintegrants = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_quatrieme_f_plus11 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_quatrieme_g_10 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_quatrieme_g_11 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_quatrieme_g_7 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_quatrieme_g_8 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_quatrieme_g_9 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_quatrieme_g_dont_autochtone = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_quatrieme_g_dont_avec_handicap = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_quatrieme_g_dont_deplaces = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_quatrieme_g_dont_etrangers = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_quatrieme_g_dont_internants = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_quatrieme_g_dont_orphelins = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_quatrieme_g_dont_redoublons = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_quatrieme_g_dont_refugies = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_quatrieme_g_dont_reintegrants = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_quatrieme_g_plus11 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'st2_effectifs_eleves_quatrieme'


class St2EffectifsElevesSixieme(models.Model):
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    st2_nombre_sixieme_f_10 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_sixieme_f_11 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_sixieme_f_9 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_sixieme_f_dont_autochtone = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_sixieme_f_dont_avec_handicap = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_sixieme_f_dont_deplaces = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_sixieme_f_dont_etrangers = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_sixieme_f_dont_internants = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_sixieme_f_dont_orphelins = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_sixieme_f_dont_redoublons = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_sixieme_f_dont_refugies = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_sixieme_f_dont_reintegrants = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_sixieme_f_plus11 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_sixieme_g_10 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_sixieme_g_11 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_sixieme_g_9 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_sixieme_g_dont_autochtone = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_sixieme_g_dont_avec_handicap = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_sixieme_g_dont_deplaces = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_sixieme_g_dont_etrangers = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_sixieme_g_dont_internants = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_sixieme_g_dont_orphelins = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_sixieme_g_dont_redoublons = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_sixieme_g_dont_refugies = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_sixieme_g_dont_reintegrants = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_sixieme_g_plus11 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'st2_effectifs_eleves_sixieme'


class St2EffectifsElevesTroisieme(models.Model):
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    st2_nombre_troisieme_f_10 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_f_11 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_f_6 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_f_7 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_f_8 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_f_9 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_f_dont_autochtone = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_f_dont_avec_handicap = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_f_dont_deplaces = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_f_dont_etrangers = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_f_dont_internants = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_f_dont_orphelins = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_f_dont_redoublons = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_f_dont_refugies = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_f_dont_reintegrants = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_f_moins6 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_f_plus11 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_g_10 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_g_11 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_g_6 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_g_7 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_g_8 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_g_9 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_g_dont_autochtone = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_g_dont_avec_handicap = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_g_dont_deplaces = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_g_dont_etrangers = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_g_dont_internants = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_g_dont_orphelins = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_g_dont_redoublons = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_g_dont_refugies = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_g_dont_reintegrants = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_g_moins6 = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_troisieme_g_plus11 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'st2_effectifs_eleves_troisieme'


class St2EnvironnementEtDeveloppement(models.Model):
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    st2_activites_parascolaires = models.CharField(max_length=255, blank=True, null=True)
    st2_coins_dechets = models.CharField(max_length=255, blank=True, null=True)
    st2_dispose_arbres = models.CharField(max_length=255, blank=True, null=True)
    st2_enseignants_formes_genre = models.CharField(max_length=255, blank=True, null=True)
    st2_enseignants_formes_premiers_soins = models.CharField(max_length=255, blank=True, null=True)
    st2_etablissement_locaux_directeurs_rld = models.CharField(max_length=255, blank=True, null=True)
    st2_femmes_enseignantes_recrutees = models.CharField(max_length=255, blank=True, null=True)
    st2_gouvernement_eleves = models.CharField(max_length=255, blank=True, null=True)
    st2_manuel_procedure = models.CharField(max_length=255, blank=True, null=True)
    st2_nombre_arbres_plantes = models.CharField(max_length=255, blank=True, null=True)
    st2_participation_rep = models.CharField(max_length=255, blank=True, null=True)
    st2_plan_communication = models.CharField(max_length=255, blank=True, null=True)
    st2_pv_eleves = models.CharField(max_length=255, blank=True, null=True)
    st2_reseaux_locaux_directeurs = models.CharField(max_length=255, blank=True, null=True)
    st2_unite_pedagogique = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'st2_environnement_et_developpement'


class St2EquipementsAteliersOuLaboratoires(models.Model):
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    st2_nomequipement = models.CharField(db_column='st2_NomEquipement', max_length=255, blank=True, null=True)  # Field name made lowercase.
    st2_nombreequipemenstmauvais = models.CharField(db_column='st2_NombreEquipemenstMauvais', max_length=255, blank=True, null=True)  # Field name made lowercase.
    st2_nombreequipementsbon = models.CharField(db_column='st2_NombreEquipementsBon', max_length=255, blank=True, null=True)  # Field name made lowercase.
    st2_typeatelieroulabo = models.CharField(db_column='st2_TypeAtelierOuLabo', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'st2_equipements_ateliers_ou_laboratoires'


class St2EtatDesLocaux(models.Model):
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    locaux_latrine_dur_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_latrine_dur_mauvais = models.CharField(max_length=255, blank=True, null=True)
    locaux_latrine_paille_feuillage_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_latrine_paille_feuillage_mauvais = models.CharField(max_length=255, blank=True, null=True)
    locaux_latrine_semidur_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_latrine_semidur_mauvais = models.CharField(max_length=255, blank=True, null=True)
    locaux_latrine_terre_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_latrine_terre_mauvais = models.CharField(max_length=255, blank=True, null=True)
    locaux_magasin_dur_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_magasin_dur_mauvais = models.CharField(max_length=255, blank=True, null=True)
    locaux_magasin_paille_feuillage_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_magasin_paille_feuillage_mauvais = models.CharField(max_length=255, blank=True, null=True)
    locaux_magasin_semidur_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_magasin_semidur_mauvais = models.CharField(max_length=255, blank=True, null=True)
    locaux_magasin_terre_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_magasin_terre_mauvais = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_bureau_administratif_dur_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_bureau_administratif_dur_mauvais = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_bureau_administratif_paille_feuillage_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_bureau_administratif_paille_feuillage_mauvais = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_bureau_administratif_semidur_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_bureau_administratif_semidur_mauvais = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_bureau_administratif_terre_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_bureau_administratif_terre_mauvais = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_de_cours_dur_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_de_cours_dur_mauvais = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_de_cours_paille_feuillage_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_de_cours_paille_feuillage_mauvais = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_de_cours_semidur_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_de_cours_semidur_mauvais = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_de_cours_terre_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_de_cours_terre_mauvais = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_specialisee_dur_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_specialisee_dur_mauvais = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_specialisee_paille_feuillage_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_specialisee_paille_feuillage_mauvais = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_specialisee_semidur_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_specialisee_semidur_mauvais = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_specialisee_terre_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_specialisee_terre_mauvais = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'st2_etat_des_locaux'


class St2EtatDesLocauxSpecifiques(models.Model):
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    locaux_activite_entole_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_activite_entole_mauvais = models.CharField(max_length=255, blank=True, null=True)
    locaux_activite_paille_feuillage_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_activite_paille_feuillage_mauvais = models.CharField(max_length=255, blank=True, null=True)
    locaux_bureau_entole_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_bureau_entole_mauvais = models.CharField(max_length=255, blank=True, null=True)
    locaux_bureau_paille_feuillage_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_bureau_paille_feuillage_mauvais = models.CharField(max_length=255, blank=True, null=True)
    locaux_magasin_entole_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_magasin_entole_mauvais = models.CharField(max_length=255, blank=True, null=True)
    locaux_magasin_paille_feuillage_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_magasin_paille_feuillage_mauvais = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_attente_paille_feuillage_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_attente_paille_feuillage_mauvais = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_jeux_sport_entole_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_jeux_sport_entole_mauvais = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_jeux_sport_paille_feuillage_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_jeux_sport_paille_feuillage_mauvais = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_repos_entole_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_repos_entole_mauvais = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_repos_paille_feuillage_bon = models.CharField(max_length=255, blank=True, null=True)
    locaux_salle_repos_paille_feuillage_mauvais = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'st2_etat_des_locaux_specifiques'


class St2GuidesPedagogiquesDisponibles(models.Model):
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    guide_autres_manuel_1ere = models.CharField(max_length=255, blank=True, null=True)
    guide_autres_manuel_2eme = models.CharField(max_length=255, blank=True, null=True)
    guide_autres_manuel_3eme = models.CharField(max_length=255, blank=True, null=True)
    guide_autres_manuel_4eme = models.CharField(max_length=255, blank=True, null=True)
    guide_autres_manuel_5eme = models.CharField(max_length=255, blank=True, null=True)
    guide_autres_manuel_6eme = models.CharField(max_length=255, blank=True, null=True)
    guide_autres_manuel_pre_primaire = models.CharField(max_length=255, blank=True, null=True)
    guide_education_civique_morale_1ere = models.CharField(max_length=255, blank=True, null=True)
    guide_education_civique_morale_2eme = models.CharField(max_length=255, blank=True, null=True)
    guide_education_civique_morale_3eme = models.CharField(max_length=255, blank=True, null=True)
    guide_education_civique_morale_4eme = models.CharField(max_length=255, blank=True, null=True)
    guide_education_civique_morale_5eme = models.CharField(max_length=255, blank=True, null=True)
    guide_education_civique_morale_6eme = models.CharField(max_length=255, blank=True, null=True)
    guide_education_civique_morale_pre_primaire = models.CharField(max_length=255, blank=True, null=True)
    guide_education_pour_la_paix_1ere = models.CharField(max_length=255, blank=True, null=True)
    guide_education_pour_la_paix_2eme = models.CharField(max_length=255, blank=True, null=True)
    guide_education_pour_la_paix_3eme = models.CharField(max_length=255, blank=True, null=True)
    guide_education_pour_la_paix_4eme = models.CharField(max_length=255, blank=True, null=True)
    guide_education_pour_la_paix_5eme = models.CharField(max_length=255, blank=True, null=True)
    guide_education_pour_la_paix_6eme = models.CharField(max_length=255, blank=True, null=True)
    guide_education_pour_la_paix_pre_primaire = models.CharField(max_length=255, blank=True, null=True)
    guide_eveil_1ere = models.CharField(max_length=255, blank=True, null=True)
    guide_eveil_2eme = models.CharField(max_length=255, blank=True, null=True)
    guide_eveil_3eme = models.CharField(max_length=255, blank=True, null=True)
    guide_eveil_4eme = models.CharField(max_length=255, blank=True, null=True)
    guide_eveil_5eme = models.CharField(max_length=255, blank=True, null=True)
    guide_eveil_6eme = models.CharField(max_length=255, blank=True, null=True)
    guide_eveil_pre_primaire = models.CharField(max_length=255, blank=True, null=True)
    guide_francais_1ere = models.CharField(max_length=255, blank=True, null=True)
    guide_francais_2eme = models.CharField(max_length=255, blank=True, null=True)
    guide_francais_3eme = models.CharField(max_length=255, blank=True, null=True)
    guide_francais_4eme = models.CharField(max_length=255, blank=True, null=True)
    guide_francais_5eme = models.CharField(max_length=255, blank=True, null=True)
    guide_francais_6eme = models.CharField(max_length=255, blank=True, null=True)
    guide_francais_pre_primaire = models.CharField(max_length=255, blank=True, null=True)
    guide_mathematique_1ere = models.CharField(max_length=255, blank=True, null=True)
    guide_mathematique_2eme = models.CharField(max_length=255, blank=True, null=True)
    guide_mathematique_3eme = models.CharField(max_length=255, blank=True, null=True)
    guide_mathematique_4eme = models.CharField(max_length=255, blank=True, null=True)
    guide_mathematique_5eme = models.CharField(max_length=255, blank=True, null=True)
    guide_mathematique_6eme = models.CharField(max_length=255, blank=True, null=True)
    guide_mathematique_pre_primaire = models.CharField(max_length=255, blank=True, null=True)
    guide_themes_tranversaux_1ere = models.CharField(max_length=255, blank=True, null=True)
    guide_themes_tranversaux_2eme = models.CharField(max_length=255, blank=True, null=True)
    guide_themes_tranversaux_3eme = models.CharField(max_length=255, blank=True, null=True)
    guide_themes_tranversaux_4eme = models.CharField(max_length=255, blank=True, null=True)
    guide_themes_tranversaux_5eme = models.CharField(max_length=255, blank=True, null=True)
    guide_themes_tranversaux_6eme = models.CharField(max_length=255, blank=True, null=True)
    guide_themes_tranversaux_pre_primaire = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'st2_guides_pedagogiques_disponibles'


class St2ManuelsDisponibles(models.Model):
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    manuels_autres_manuel_1ere = models.CharField(max_length=255, blank=True, null=True)
    manuels_autres_manuel_2eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_autres_manuel_3eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_autres_manuel_4eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_autres_manuel_5eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_autres_manuel_6eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_autres_manuel_pre_primaire = models.CharField(max_length=255, blank=True, null=True)
    manuels_education_civique_morale_1ere = models.CharField(max_length=255, blank=True, null=True)
    manuels_education_civique_morale_2eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_education_civique_morale_3eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_education_civique_morale_4eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_education_civique_morale_5eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_education_civique_morale_6eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_education_civique_morale_pre_primaire = models.CharField(max_length=255, blank=True, null=True)
    manuels_education_pour_la_paix_1ere = models.CharField(max_length=255, blank=True, null=True)
    manuels_education_pour_la_paix_2eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_education_pour_la_paix_3eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_education_pour_la_paix_4eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_education_pour_la_paix_5eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_education_pour_la_paix_6eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_education_pour_la_paix_pre_primaire = models.CharField(max_length=255, blank=True, null=True)
    manuels_eveil_1ere = models.CharField(max_length=255, blank=True, null=True)
    manuels_eveil_2eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_eveil_3eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_eveil_4eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_eveil_5eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_eveil_6eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_eveil_pre_primaire = models.CharField(max_length=255, blank=True, null=True)
    manuels_francais_1ere = models.CharField(max_length=255, blank=True, null=True)
    manuels_francais_2eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_francais_3eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_francais_4eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_francais_5eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_francais_6eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_francais_pre_primaire = models.CharField(max_length=255, blank=True, null=True)
    manuels_mathematique_1ere = models.CharField(max_length=255, blank=True, null=True)
    manuels_mathematique_2eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_mathematique_3eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_mathematique_4eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_mathematique_5eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_mathematique_6eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_mathematique_pre_primaire = models.CharField(max_length=255, blank=True, null=True)
    manuels_themes_tranversaux_1ere = models.CharField(max_length=255, blank=True, null=True)
    manuels_themes_tranversaux_2eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_themes_tranversaux_3eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_themes_tranversaux_4eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_themes_tranversaux_5eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_themes_tranversaux_6eme = models.CharField(max_length=255, blank=True, null=True)
    manuels_themes_tranversaux_pre_primaire = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'st2_manuels_disponibles'


class St2PersonnelAdministratifEtOuvrier(models.Model):
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    admin_autres_directeur_adjoint_f = models.CharField(max_length=255, blank=True, null=True)
    admin_autres_directeur_adjoint_h = models.CharField(max_length=255, blank=True, null=True)
    admin_autres_directeur_f = models.CharField(max_length=255, blank=True, null=True)
    admin_autres_directeur_h = models.CharField(max_length=255, blank=True, null=True)
    admin_autres_ouvrier_autre_f = models.CharField(max_length=255, blank=True, null=True)
    admin_autres_ouvrier_autre_h = models.CharField(max_length=255, blank=True, null=True)
    admin_autres_surnumeraire_f = models.CharField(max_length=255, blank=True, null=True)
    admin_autres_surnumeraire_h = models.CharField(max_length=255, blank=True, null=True)
    admin_autres_surveillant_f = models.CharField(max_length=255, blank=True, null=True)
    admin_autres_surveillant_h = models.CharField(max_length=255, blank=True, null=True)
    admin_d4_directeur_adjoint_f = models.CharField(max_length=255, blank=True, null=True)
    admin_d4_directeur_adjoint_h = models.CharField(max_length=255, blank=True, null=True)
    admin_d4_directeur_f = models.CharField(max_length=255, blank=True, null=True)
    admin_d4_directeur_h = models.CharField(max_length=255, blank=True, null=True)
    admin_d4_ouvrier_autre_f = models.CharField(max_length=255, blank=True, null=True)
    admin_d4_ouvrier_autre_h = models.CharField(max_length=255, blank=True, null=True)
    admin_d4_surnumeraire_f = models.CharField(max_length=255, blank=True, null=True)
    admin_d4_surnumeraire_h = models.CharField(max_length=255, blank=True, null=True)
    admin_d4_surveillant_f = models.CharField(max_length=255, blank=True, null=True)
    admin_d4_surveillant_h = models.CharField(max_length=255, blank=True, null=True)
    admin_d6_directeur_adjoint_f = models.CharField(max_length=255, blank=True, null=True)
    admin_d6_directeur_adjoint_h = models.CharField(max_length=255, blank=True, null=True)
    admin_d6_directeur_f = models.CharField(max_length=255, blank=True, null=True)
    admin_d6_directeur_h = models.CharField(max_length=255, blank=True, null=True)
    admin_d6_ouvrier_autre_f = models.CharField(max_length=255, blank=True, null=True)
    admin_d6_ouvrier_autre_h = models.CharField(max_length=255, blank=True, null=True)
    admin_d6_surnumeraire_f = models.CharField(max_length=255, blank=True, null=True)
    admin_d6_surnumeraire_h = models.CharField(max_length=255, blank=True, null=True)
    admin_d6_surveillant_f = models.CharField(max_length=255, blank=True, null=True)
    admin_d6_surveillant_h = models.CharField(max_length=255, blank=True, null=True)
    admin_moin_d4_directeur_adjoint_f = models.CharField(max_length=255, blank=True, null=True)
    admin_moin_d4_directeur_adjoint_h = models.CharField(max_length=255, blank=True, null=True)
    admin_moin_d4_directeur_f = models.CharField(max_length=255, blank=True, null=True)
    admin_moin_d4_directeur_h = models.CharField(max_length=255, blank=True, null=True)
    admin_moin_d4_ouvrier_autre_f = models.CharField(max_length=255, blank=True, null=True)
    admin_moin_d4_ouvrier_autre_h = models.CharField(max_length=255, blank=True, null=True)
    admin_moin_d4_surnumeraire_f = models.CharField(max_length=255, blank=True, null=True)
    admin_moin_d4_surnumeraire_h = models.CharField(max_length=255, blank=True, null=True)
    admin_moin_d4_surveillant_f = models.CharField(max_length=255, blank=True, null=True)
    admin_moin_d4_surveillant_h = models.CharField(max_length=255, blank=True, null=True)
    admin_p6_directeur_adjoint_f = models.CharField(max_length=255, blank=True, null=True)
    admin_p6_directeur_adjoint_h = models.CharField(max_length=255, blank=True, null=True)
    admin_p6_directeur_f = models.CharField(max_length=255, blank=True, null=True)
    admin_p6_directeur_h = models.CharField(max_length=255, blank=True, null=True)
    admin_p6_ouvrier_autre_f = models.CharField(max_length=255, blank=True, null=True)
    admin_p6_ouvrier_autre_h = models.CharField(max_length=255, blank=True, null=True)
    admin_p6_surnumeraire_f = models.CharField(max_length=255, blank=True, null=True)
    admin_p6_surnumeraire_h = models.CharField(max_length=255, blank=True, null=True)
    admin_p6_surveillant_f = models.CharField(max_length=255, blank=True, null=True)
    admin_p6_surveillant_h = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'st2_personnel_administratif_et_ouvrier'


class St2RepartitionAffectation(models.Model):
    niveau = models.IntegerField(blank=True, null=True)
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    st2_class_affectation_1f_autres = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_1f_d4 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_1f_d6 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_1f_p6 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_1f_pred4 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_1h_autres = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_1h_d4 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_1h_d6 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_1h_p6 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_1h_pred4 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_2f_autres = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_2f_d4 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_2f_d6 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_2f_p6 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_2f_pred4 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_2h_autres = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_2h_d4 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_2h_d6 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_2h_p6 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_2h_pred4 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_3f_autres = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_3f_d4 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_3f_d6 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_3f_p6 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_3f_pred4 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_3h_autres = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_3h_d4 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_3h_d6 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_3h_p6 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_3h_pred4 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_4f_autres = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_4f_d4 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_4f_d6 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_4f_p6 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_4f_pred4 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_4h_autres = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_4h_d4 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_4h_d6 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_4h_p6 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_4h_pred4 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_5f_autres = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_5f_d4 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_5f_d6 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_5f_p6 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_5f_pred4 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_5h_autres = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_5h_d4 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_5h_d6 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_5h_p6 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_5h_pred4 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_6f_autres = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_6f_d4 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_6f_d6 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_6f_p6 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_6f_pred4 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_6h_autres = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_6h_d4 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_6h_d6 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_6h_p6 = models.CharField(max_length=255, blank=True, null=True)
    st2_class_affectation_6h_pred4 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'st2_repartition_affectation'


class St2RepartitionEnseignantsEligibles(models.Model):
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    nbenseignantseligiblesretraite = models.CharField(db_column='nbEnseignantsEligiblesRetraite', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'st2_repartition_enseignants_eligibles'


class St2RepartitionReleve(models.Model):
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    releveautresf = models.CharField(db_column='releveAutresF', max_length=255, blank=True, null=True)  # Field name made lowercase.
    releveautresh = models.CharField(db_column='releveAutresH', max_length=255, blank=True, null=True)  # Field name made lowercase.
    releved4f = models.CharField(db_column='releveD4F', max_length=255, blank=True, null=True)  # Field name made lowercase.
    releved4h = models.CharField(db_column='releveD4H', max_length=255, blank=True, null=True)  # Field name made lowercase.
    releved6f = models.CharField(db_column='releveD6F', max_length=255, blank=True, null=True)  # Field name made lowercase.
    releved6h = models.CharField(db_column='releveD6H', max_length=255, blank=True, null=True)  # Field name made lowercase.
    relevep6f = models.CharField(db_column='releveP6F', max_length=255, blank=True, null=True)  # Field name made lowercase.
    relevep6h = models.CharField(db_column='releveP6H', max_length=255, blank=True, null=True)  # Field name made lowercase.
    relevepred4f = models.CharField(db_column='relevePred4F', max_length=255, blank=True, null=True)  # Field name made lowercase.
    relevepred4h = models.CharField(db_column='relevePred4H', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'st2_repartition_releve'


class St2ResultatsEnafEpsante(models.Model):
    st2_effectif_eleves_admis_francais_f = models.IntegerField(blank=True, null=True)
    st2_effectif_eleves_admis_francais_g = models.IntegerField(blank=True, null=True)
    st2_effectif_eleves_admis_maths_f = models.IntegerField(blank=True, null=True)
    st2_effectif_eleves_admis_maths_g = models.IntegerField(blank=True, null=True)
    st2_effectif_eleves_inscrit_f = models.IntegerField(blank=True, null=True)
    st2_effectif_eleves_inscrit_g = models.IntegerField(blank=True, null=True)
    st2_effectif_eleves_present_f = models.IntegerField(blank=True, null=True)
    st2_effectif_eleves_present_g = models.IntegerField(blank=True, null=True)
    st2_nombre_absences_eleves_1 = models.IntegerField(blank=True, null=True)
    st2_nombre_absences_eleves_2 = models.IntegerField(blank=True, null=True)
    st2_nombre_absences_eleves_3 = models.IntegerField(blank=True, null=True)
    st2_nombre_absences_eleves_4 = models.IntegerField(blank=True, null=True)
    st2_nombre_absences_eleves_5 = models.IntegerField(blank=True, null=True)
    st2_nombre_absences_eleves_6 = models.IntegerField(blank=True, null=True)
    st2_nombre_eleves_beneficiants_deparasitage_1 = models.IntegerField(blank=True, null=True)
    st2_nombre_eleves_beneficiants_deparasitage_2 = models.IntegerField(blank=True, null=True)
    st2_nombre_eleves_beneficiants_deparasitage_3 = models.IntegerField(blank=True, null=True)
    st2_nombre_eleves_beneficiants_deparasitage_4 = models.IntegerField(blank=True, null=True)
    st2_nombre_eleves_beneficiants_deparasitage_5 = models.IntegerField(blank=True, null=True)
    st2_nombre_eleves_beneficiants_deparasitage_6 = models.IntegerField(blank=True, null=True)
    st2_nombre_eleves_beneficiants_visite_medicales_1 = models.IntegerField(blank=True, null=True)
    st2_nombre_eleves_beneficiants_visite_medicales_2 = models.IntegerField(blank=True, null=True)
    st2_nombre_eleves_beneficiants_visite_medicales_3 = models.IntegerField(blank=True, null=True)
    st2_nombre_eleves_beneficiants_visite_medicales_4 = models.IntegerField(blank=True, null=True)
    st2_nombre_eleves_beneficiants_visite_medicales_5 = models.IntegerField(blank=True, null=True)
    st2_nombre_eleves_beneficiants_visite_medicales_6 = models.IntegerField(blank=True, null=True)
    st2_nombre_jours_ouvrables_1 = models.IntegerField(blank=True, null=True)
    st2_nombre_jours_ouvrables_2 = models.IntegerField(blank=True, null=True)
    st2_nombre_jours_ouvrables_3 = models.IntegerField(blank=True, null=True)
    st2_nombre_jours_ouvrables_4 = models.IntegerField(blank=True, null=True)
    st2_nombre_jours_ouvrables_5 = models.IntegerField(blank=True, null=True)
    st2_nombre_jours_ouvrables_6 = models.IntegerField(blank=True, null=True)
    st2_nombre_total_eleves_1 = models.IntegerField(blank=True, null=True)
    st2_nombre_total_eleves_2 = models.IntegerField(blank=True, null=True)
    st2_nombre_total_eleves_3 = models.IntegerField(blank=True, null=True)
    st2_nombre_total_eleves_4 = models.IntegerField(blank=True, null=True)
    st2_nombre_total_eleves_5 = models.IntegerField(blank=True, null=True)
    st2_nombre_total_eleves_6 = models.IntegerField(blank=True, null=True)
    st2_taux_abandon = models.FloatField(blank=True, null=True)
    st2_taux_reussite_enafep = models.FloatField(blank=True, null=True)
    st2_total_admis_f_reussie_test = models.IntegerField(blank=True, null=True)
    st2_total_admis_g_reussie_test = models.IntegerField(blank=True, null=True)
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'st2_resultats_enaf_epsante'


class St3DisponibiliteProgrammeNational(models.Model):
    estdisponibilitedansleprogrammenational = models.TextField(db_column='EstDisponibiliteDansLeProgrammeNational', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    nomdufiliere = models.CharField(db_column='NomDuFiliere', max_length=255, blank=True, null=True)  # Field name made lowercase.
    typedeprogrammenational = models.CharField(db_column='TypeDeProgrammeNational', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'st3_disponibilite_programme_national'


class St3Documentation(models.Model):
    st3_manuel_procedure = models.TextField(blank=True, null=True)  # This field type is a guess.
    st3_plan_communication = models.TextField(blank=True, null=True)  # This field type is a guess.
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'st3_documentation'


class St3DualInputSection(models.Model):
    st3_enseignants_formes_genre = models.IntegerField(blank=True, null=True)
    st3_femmes_enseignantes_recrutees = models.IntegerField(blank=True, null=True)
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'st3_dual_input_section'


class St3EffectifEleveInscritSexeAnneeEtudeAgeRevolu(models.Model):
    effectifparageetsexe = models.OneToOneField('St3EffectifParAgeSexe', models.DO_NOTHING, db_column='effectifParAgeEtSexe_id', blank=True, null=True)  # Field name made lowercase.
    effectifparcategorieparticuliere = models.OneToOneField('St3EffectifParCategorieParticuliere', models.DO_NOTHING, db_column='effectifParCategorieParticuliere_id', blank=True, null=True)  # Field name made lowercase.
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'st3_effectif_eleve_inscrit_sexe_annee_etude_age_revolu'


class St3EffectifEleveTypeEnseignement(models.Model):
    st_3_enseignementartsetmetiers1hf = models.IntegerField(db_column='st_3_EnseignementArtsEtMetiers1HF', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementartsetmetiers1hf_redoublant = models.IntegerField(db_column='st_3_EnseignementArtsEtMetiers1HF_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementartsetmetiers1hg = models.IntegerField(db_column='st_3_EnseignementArtsEtMetiers1HG', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementartsetmetiers1hg_redoublant = models.IntegerField(db_column='st_3_EnseignementArtsEtMetiers1HG_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementartsetmetiers1hnombreclass = models.IntegerField(db_column='st_3_EnseignementArtsEtMetiers1HNombreClass', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementartsetmetiers2hf = models.IntegerField(db_column='st_3_EnseignementArtsEtMetiers2HF', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementartsetmetiers2hf_redoublant = models.IntegerField(db_column='st_3_EnseignementArtsEtMetiers2HF_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementartsetmetiers2hg = models.IntegerField(db_column='st_3_EnseignementArtsEtMetiers2HG', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementartsetmetiers2hg_redoublant = models.IntegerField(db_column='st_3_EnseignementArtsEtMetiers2HG_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementartsetmetiers2hnombreclass = models.IntegerField(db_column='st_3_EnseignementArtsEtMetiers2HNombreClass', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementartsetmetiers3hf = models.IntegerField(db_column='st_3_EnseignementArtsEtMetiers3HF', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementartsetmetiers3hf_redoublant = models.IntegerField(db_column='st_3_EnseignementArtsEtMetiers3HF_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementartsetmetiers3hg = models.IntegerField(db_column='st_3_EnseignementArtsEtMetiers3HG', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementartsetmetiers3hg_redoublant = models.IntegerField(db_column='st_3_EnseignementArtsEtMetiers3HG_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementartsetmetiers3hnombreclass = models.IntegerField(db_column='st_3_EnseignementArtsEtMetiers3HNombreClass', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementartsetmetiers4hf = models.IntegerField(db_column='st_3_EnseignementArtsEtMetiers4HF', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementartsetmetiers4hf_redoublant = models.IntegerField(db_column='st_3_EnseignementArtsEtMetiers4HF_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementartsetmetiers4hg = models.IntegerField(db_column='st_3_EnseignementArtsEtMetiers4HG', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementartsetmetiers4hg_redoublant = models.IntegerField(db_column='st_3_EnseignementArtsEtMetiers4HG_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementartsetmetiers4hnombreclass = models.IntegerField(db_column='st_3_EnseignementArtsEtMetiers4HNombreClass', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementartsetmetiers7f = models.IntegerField(db_column='st_3_EnseignementArtsEtMetiers7F', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementartsetmetiers7fredoublant = models.IntegerField(db_column='st_3_EnseignementArtsEtMetiers7FRedoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementartsetmetiers7g = models.IntegerField(db_column='st_3_EnseignementArtsEtMetiers7G', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementartsetmetiers7gredoublant = models.IntegerField(db_column='st_3_EnseignementArtsEtMetiers7GRedoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementartsetmetiers7nombreclass = models.IntegerField(db_column='st_3_EnseignementArtsEtMetiers7NombreClass', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementartsetmetiers8f = models.IntegerField(db_column='st_3_EnseignementArtsEtMetiers8F', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementartsetmetiers8fredoublant = models.IntegerField(db_column='st_3_EnseignementArtsEtMetiers8FRedoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementartsetmetiers8g = models.IntegerField(db_column='st_3_EnseignementArtsEtMetiers8G', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementartsetmetiers8gredoublant = models.IntegerField(db_column='st_3_EnseignementArtsEtMetiers8GRedoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementartsetmetiers8nombreclass = models.IntegerField(db_column='st_3_EnseignementArtsEtMetiers8NombreClass', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementgeneral1hf = models.IntegerField(db_column='st_3_EnseignementGeneral1HF', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementgeneral1hf_redoublant = models.IntegerField(db_column='st_3_EnseignementGeneral1HF_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementgeneral1hg = models.IntegerField(db_column='st_3_EnseignementGeneral1HG', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementgeneral1hg_redoublant = models.IntegerField(db_column='st_3_EnseignementGeneral1HG_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementgeneral1hnombreclass = models.IntegerField(db_column='st_3_EnseignementGeneral1HNombreClass', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementgeneral2hf = models.IntegerField(db_column='st_3_EnseignementGeneral2HF', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementgeneral2hf_redoublant = models.IntegerField(db_column='st_3_EnseignementGeneral2HF_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementgeneral2hg = models.IntegerField(db_column='st_3_EnseignementGeneral2HG', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementgeneral2hg_redoublant = models.IntegerField(db_column='st_3_EnseignementGeneral2HG_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementgeneral2hnombreclass = models.IntegerField(db_column='st_3_EnseignementGeneral2HNombreClass', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementgeneral3hf = models.IntegerField(db_column='st_3_EnseignementGeneral3HF', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementgeneral3hf_redoublant = models.IntegerField(db_column='st_3_EnseignementGeneral3HF_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementgeneral3hg = models.IntegerField(db_column='st_3_EnseignementGeneral3HG', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementgeneral3hg_redoublant = models.IntegerField(db_column='st_3_EnseignementGeneral3HG_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementgeneral3hnombreclass = models.IntegerField(db_column='st_3_EnseignementGeneral3HNombreClass', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementgeneral4hf = models.IntegerField(db_column='st_3_EnseignementGeneral4HF', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementgeneral4hf_redoublant = models.IntegerField(db_column='st_3_EnseignementGeneral4HF_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementgeneral4hg = models.IntegerField(db_column='st_3_EnseignementGeneral4HG', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementgeneral4hg_redoublant = models.IntegerField(db_column='st_3_EnseignementGeneral4HG_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementgeneral4hnombreclass = models.IntegerField(db_column='st_3_EnseignementGeneral4HNombreClass', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementgeneral7f = models.IntegerField(db_column='st_3_EnseignementGeneral7F', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementgeneral7fredoublant = models.IntegerField(db_column='st_3_EnseignementGeneral7FRedoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementgeneral7g = models.IntegerField(db_column='st_3_EnseignementGeneral7G', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementgeneral7gredoublant = models.IntegerField(db_column='st_3_EnseignementGeneral7GRedoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementgeneral7nombreclass = models.IntegerField(db_column='st_3_EnseignementGeneral7NombreClass', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementgeneral8f = models.IntegerField(db_column='st_3_EnseignementGeneral8F', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementgeneral8fredoublant = models.IntegerField(db_column='st_3_EnseignementGeneral8FRedoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementgeneral8g = models.IntegerField(db_column='st_3_EnseignementGeneral8G', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementgeneral8gredoublant = models.IntegerField(db_column='st_3_EnseignementGeneral8GRedoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementgeneral8nombreclass = models.IntegerField(db_column='st_3_EnseignementGeneral8NombreClass', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementnormal1hf = models.IntegerField(db_column='st_3_EnseignementNormal1HF', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementnormal1hf_redoublant = models.IntegerField(db_column='st_3_EnseignementNormal1HF_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementnormal1hg = models.IntegerField(db_column='st_3_EnseignementNormal1HG', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementnormal1hg_redoublant = models.IntegerField(db_column='st_3_EnseignementNormal1HG_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementnormal1hnombreclass = models.IntegerField(db_column='st_3_EnseignementNormal1HNombreClass', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementnormal2hf = models.IntegerField(db_column='st_3_EnseignementNormal2HF', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementnormal2hf_redoublant = models.IntegerField(db_column='st_3_EnseignementNormal2HF_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementnormal2hg = models.IntegerField(db_column='st_3_EnseignementNormal2HG', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementnormal2hg_redoublant = models.IntegerField(db_column='st_3_EnseignementNormal2HG_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementnormal2hnombreclass = models.IntegerField(db_column='st_3_EnseignementNormal2HNombreClass', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementnormal3hf = models.IntegerField(db_column='st_3_EnseignementNormal3HF', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementnormal3hf_redoublant = models.IntegerField(db_column='st_3_EnseignementNormal3HF_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementnormal3hg = models.IntegerField(db_column='st_3_EnseignementNormal3HG', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementnormal3hg_redoublant = models.IntegerField(db_column='st_3_EnseignementNormal3HG_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementnormal3hnombreclass = models.IntegerField(db_column='st_3_EnseignementNormal3HNombreClass', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementnormal4hf = models.IntegerField(db_column='st_3_EnseignementNormal4HF', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementnormal4hf_redoublant = models.IntegerField(db_column='st_3_EnseignementNormal4HF_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementnormal4hg = models.IntegerField(db_column='st_3_EnseignementNormal4HG', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementnormal4hg_redoublant = models.IntegerField(db_column='st_3_EnseignementNormal4HG_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementnormal4hnombreclass = models.IntegerField(db_column='st_3_EnseignementNormal4HNombreClass', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementnormal7f = models.IntegerField(db_column='st_3_EnseignementNormal7F', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementnormal7fredoublant = models.IntegerField(db_column='st_3_EnseignementNormal7FRedoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementnormal7g = models.IntegerField(db_column='st_3_EnseignementNormal7G', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementnormal7gredoublant = models.IntegerField(db_column='st_3_EnseignementNormal7GRedoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementnormal7nombreclass = models.IntegerField(db_column='st_3_EnseignementNormal7NombreClass', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementnormal8f = models.IntegerField(db_column='st_3_EnseignementNormal8F', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementnormal8fredoublant = models.IntegerField(db_column='st_3_EnseignementNormal8FRedoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementnormal8g = models.IntegerField(db_column='st_3_EnseignementNormal8G', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementnormal8gredoublant = models.IntegerField(db_column='st_3_EnseignementNormal8GRedoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementnormal8nombreclass = models.IntegerField(db_column='st_3_EnseignementNormal8NombreClass', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementtechnique1hf = models.IntegerField(db_column='st_3_EnseignementTechnique1HF', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementtechnique1hf_redoublant = models.IntegerField(db_column='st_3_EnseignementTechnique1HF_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementtechnique1hg = models.IntegerField(db_column='st_3_EnseignementTechnique1HG', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementtechnique1hg_redoublant = models.IntegerField(db_column='st_3_EnseignementTechnique1HG_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementtechnique1hnombreclass = models.IntegerField(db_column='st_3_EnseignementTechnique1HNombreClass', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementtechnique2hf = models.IntegerField(db_column='st_3_EnseignementTechnique2HF', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementtechnique2hf_redoublant = models.IntegerField(db_column='st_3_EnseignementTechnique2HF_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementtechnique2hg = models.IntegerField(db_column='st_3_EnseignementTechnique2HG', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementtechnique2hg_redoublant = models.IntegerField(db_column='st_3_EnseignementTechnique2HG_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementtechnique2hnombreclass = models.IntegerField(db_column='st_3_EnseignementTechnique2HNombreClass', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementtechnique3hf = models.IntegerField(db_column='st_3_EnseignementTechnique3HF', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementtechnique3hf_redoublant = models.IntegerField(db_column='st_3_EnseignementTechnique3HF_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementtechnique3hg = models.IntegerField(db_column='st_3_EnseignementTechnique3HG', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementtechnique3hg_redoublant = models.IntegerField(db_column='st_3_EnseignementTechnique3HG_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementtechnique3hnombreclass = models.IntegerField(db_column='st_3_EnseignementTechnique3HNombreClass', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementtechnique4hf = models.IntegerField(db_column='st_3_EnseignementTechnique4HF', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementtechnique4hf_redoublant = models.IntegerField(db_column='st_3_EnseignementTechnique4HF_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementtechnique4hg = models.IntegerField(db_column='st_3_EnseignementTechnique4HG', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementtechnique4hg_redoublant = models.IntegerField(db_column='st_3_EnseignementTechnique4HG_Redoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementtechnique4hnombreclass = models.IntegerField(db_column='st_3_EnseignementTechnique4HNombreClass', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementtechnique7f = models.IntegerField(db_column='st_3_EnseignementTechnique7F', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementtechnique7fredoublant = models.IntegerField(db_column='st_3_EnseignementTechnique7FRedoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementtechnique7g = models.IntegerField(db_column='st_3_EnseignementTechnique7G', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementtechnique7gredoublant = models.IntegerField(db_column='st_3_EnseignementTechnique7GRedoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementtechnique7nombreclass = models.IntegerField(db_column='st_3_EnseignementTechnique7NombreClass', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementtechnique8f = models.IntegerField(db_column='st_3_EnseignementTechnique8F', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementtechnique8fredoublant = models.IntegerField(db_column='st_3_EnseignementTechnique8FRedoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementtechnique8g = models.IntegerField(db_column='st_3_EnseignementTechnique8G', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementtechnique8gredoublant = models.IntegerField(db_column='st_3_EnseignementTechnique8GRedoublant', blank=True, null=True)  # Field name made lowercase.
    st_3_enseignementtechnique8nombreclass = models.IntegerField(db_column='st_3_EnseignementTechnique8NombreClass', blank=True, null=True)  # Field name made lowercase.
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'st3_effectif_eleve_type_enseignement'


class St3EffectifParAgeSexe(models.Model):
    effectifeleves1hf12 = models.IntegerField(db_column='effectifEleves1HF12', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hf13 = models.IntegerField(db_column='effectifEleves1HF13', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hf14 = models.IntegerField(db_column='effectifEleves1HF14', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hf15 = models.IntegerField(db_column='effectifEleves1HF15', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hf16 = models.IntegerField(db_column='effectifEleves1HF16', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hf17 = models.IntegerField(db_column='effectifEleves1HF17', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hfmoins12 = models.IntegerField(db_column='effectifEleves1HFMoins12', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hfplus17 = models.IntegerField(db_column='effectifEleves1HFPlus17', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hg12 = models.IntegerField(db_column='effectifEleves1HG12', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hg13 = models.IntegerField(db_column='effectifEleves1HG13', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hg14 = models.IntegerField(db_column='effectifEleves1HG14', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hg15 = models.IntegerField(db_column='effectifEleves1HG15', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hg16 = models.IntegerField(db_column='effectifEleves1HG16', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hg17 = models.IntegerField(db_column='effectifEleves1HG17', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hgmoins12 = models.IntegerField(db_column='effectifEleves1HGMoins12', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hgplus17 = models.IntegerField(db_column='effectifEleves1HGPlus17', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hf12 = models.IntegerField(db_column='effectifEleves2HF12', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hf13 = models.IntegerField(db_column='effectifEleves2HF13', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hf14 = models.IntegerField(db_column='effectifEleves2HF14', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hf15 = models.IntegerField(db_column='effectifEleves2HF15', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hf16 = models.IntegerField(db_column='effectifEleves2HF16', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hf17 = models.IntegerField(db_column='effectifEleves2HF17', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hfmoins12 = models.IntegerField(db_column='effectifEleves2HFMoins12', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hfplus17 = models.IntegerField(db_column='effectifEleves2HFPlus17', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hg12 = models.IntegerField(db_column='effectifEleves2HG12', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hg13 = models.IntegerField(db_column='effectifEleves2HG13', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hg14 = models.IntegerField(db_column='effectifEleves2HG14', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hg15 = models.IntegerField(db_column='effectifEleves2HG15', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hg16 = models.IntegerField(db_column='effectifEleves2HG16', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hg17 = models.IntegerField(db_column='effectifEleves2HG17', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hgmoins12 = models.IntegerField(db_column='effectifEleves2HGMoins12', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hgplus17 = models.IntegerField(db_column='effectifEleves2HGPlus17', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hf12 = models.IntegerField(db_column='effectifEleves3HF12', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hf13 = models.IntegerField(db_column='effectifEleves3HF13', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hf14 = models.IntegerField(db_column='effectifEleves3HF14', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hf15 = models.IntegerField(db_column='effectifEleves3HF15', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hf16 = models.IntegerField(db_column='effectifEleves3HF16', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hf17 = models.IntegerField(db_column='effectifEleves3HF17', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hfmoins12 = models.IntegerField(db_column='effectifEleves3HFMoins12', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hfplus17 = models.IntegerField(db_column='effectifEleves3HFPlus17', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hg12 = models.IntegerField(db_column='effectifEleves3HG12', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hg13 = models.IntegerField(db_column='effectifEleves3HG13', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hg14 = models.IntegerField(db_column='effectifEleves3HG14', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hg15 = models.IntegerField(db_column='effectifEleves3HG15', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hg16 = models.IntegerField(db_column='effectifEleves3HG16', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hg17 = models.IntegerField(db_column='effectifEleves3HG17', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hgmoins12 = models.IntegerField(db_column='effectifEleves3HGMoins12', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hgplus17 = models.IntegerField(db_column='effectifEleves3HGPlus17', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hf12 = models.IntegerField(db_column='effectifEleves4HF12', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hf13 = models.IntegerField(db_column='effectifEleves4HF13', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hf14 = models.IntegerField(db_column='effectifEleves4HF14', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hf15 = models.IntegerField(db_column='effectifEleves4HF15', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hf16 = models.IntegerField(db_column='effectifEleves4HF16', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hf17 = models.IntegerField(db_column='effectifEleves4HF17', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hfmoins12 = models.IntegerField(db_column='effectifEleves4HFMoins12', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hfplus17 = models.IntegerField(db_column='effectifEleves4HFPlus17', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hg12 = models.IntegerField(db_column='effectifEleves4HG12', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hg13 = models.IntegerField(db_column='effectifEleves4HG13', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hg14 = models.IntegerField(db_column='effectifEleves4HG14', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hg15 = models.IntegerField(db_column='effectifEleves4HG15', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hg16 = models.IntegerField(db_column='effectifEleves4HG16', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hg17 = models.IntegerField(db_column='effectifEleves4HG17', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hgmoins12 = models.IntegerField(db_column='effectifEleves4HGMoins12', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hgplus17 = models.IntegerField(db_column='effectifEleves4HGPlus17', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7f12 = models.IntegerField(db_column='effectifEleves7F12', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7f13 = models.IntegerField(db_column='effectifEleves7F13', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7f14 = models.IntegerField(db_column='effectifEleves7F14', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7f15 = models.IntegerField(db_column='effectifEleves7F15', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7f16 = models.IntegerField(db_column='effectifEleves7F16', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7f17 = models.IntegerField(db_column='effectifEleves7F17', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7fmoins12 = models.IntegerField(db_column='effectifEleves7FMoins12', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7fplus17 = models.IntegerField(db_column='effectifEleves7FPlus17', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7g12 = models.IntegerField(db_column='effectifEleves7G12', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7g13 = models.IntegerField(db_column='effectifEleves7G13', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7g14 = models.IntegerField(db_column='effectifEleves7G14', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7g15 = models.IntegerField(db_column='effectifEleves7G15', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7g16 = models.IntegerField(db_column='effectifEleves7G16', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7g17 = models.IntegerField(db_column='effectifEleves7G17', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7gmoins12 = models.IntegerField(db_column='effectifEleves7GMoins12', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7gplus17 = models.IntegerField(db_column='effectifEleves7GPlus17', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8f12 = models.IntegerField(db_column='effectifEleves8F12', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8f13 = models.IntegerField(db_column='effectifEleves8F13', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8f14 = models.IntegerField(db_column='effectifEleves8F14', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8f15 = models.IntegerField(db_column='effectifEleves8F15', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8f16 = models.IntegerField(db_column='effectifEleves8F16', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8f17 = models.IntegerField(db_column='effectifEleves8F17', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8fmoins12 = models.IntegerField(db_column='effectifEleves8FMoins12', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8fplus17 = models.IntegerField(db_column='effectifEleves8FPlus17', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8g12 = models.IntegerField(db_column='effectifEleves8G12', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8g13 = models.IntegerField(db_column='effectifEleves8G13', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8g14 = models.IntegerField(db_column='effectifEleves8G14', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8g15 = models.IntegerField(db_column='effectifEleves8G15', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8g16 = models.IntegerField(db_column='effectifEleves8G16', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8g17 = models.IntegerField(db_column='effectifEleves8G17', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8gmoins12 = models.IntegerField(db_column='effectifEleves8GMoins12', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8gplus17 = models.IntegerField(db_column='effectifEleves8GPlus17', blank=True, null=True)  # Field name made lowercase.
    id = models.BigAutoField(primary_key=True)
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'st3_effectif_par_age_sexe'


class St3EffectifParCategorieParticuliere(models.Model):
    effectifeleves1hfautochtone = models.IntegerField(db_column='effectifEleves1HFAutochtone', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hfavechandicap = models.IntegerField(db_column='effectifEleves1HFAvecHandicap', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hfdeplacesexternes = models.IntegerField(db_column='effectifEleves1HFDeplacesExternes', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hfdeplacesinternes = models.IntegerField(db_column='effectifEleves1HFDeplacesInternes', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hfetrangers = models.IntegerField(db_column='effectifEleves1HFEtrangers', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hfinternat = models.IntegerField(db_column='effectifEleves1HFInternat', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hforphelins = models.IntegerField(db_column='effectifEleves1HFOrphelins', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hfreintegrant = models.IntegerField(db_column='effectifEleves1HFReIntegrant', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hfredoublons = models.IntegerField(db_column='effectifEleves1HFRedoublons', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hfrefugies = models.IntegerField(db_column='effectifEleves1HFRefugies', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hgautochtone = models.IntegerField(db_column='effectifEleves1HGAutochtone', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hgavechandicap = models.IntegerField(db_column='effectifEleves1HGAvecHandicap', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hgdeplacesexternes = models.IntegerField(db_column='effectifEleves1HGDeplacesExternes', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hgdeplacesinternes = models.IntegerField(db_column='effectifEleves1HGDeplacesInternes', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hgetrangers = models.IntegerField(db_column='effectifEleves1HGEtrangers', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hginternat = models.IntegerField(db_column='effectifEleves1HGInternat', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hgorphelins = models.IntegerField(db_column='effectifEleves1HGOrphelins', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hgreintegrant = models.IntegerField(db_column='effectifEleves1HGReIntegrant', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hgredoublons = models.IntegerField(db_column='effectifEleves1HGRedoublons', blank=True, null=True)  # Field name made lowercase.
    effectifeleves1hgrefugies = models.IntegerField(db_column='effectifEleves1HGRefugies', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hfautochtone = models.IntegerField(db_column='effectifEleves2HFAutochtone', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hfavechandicap = models.IntegerField(db_column='effectifEleves2HFAvecHandicap', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hfdeplacesexternes = models.IntegerField(db_column='effectifEleves2HFDeplacesExternes', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hfdeplacesinternes = models.IntegerField(db_column='effectifEleves2HFDeplacesInternes', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hfetrangers = models.IntegerField(db_column='effectifEleves2HFEtrangers', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hfinternat = models.IntegerField(db_column='effectifEleves2HFInternat', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hforphelins = models.IntegerField(db_column='effectifEleves2HFOrphelins', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hfreintegrant = models.IntegerField(db_column='effectifEleves2HFReIntegrant', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hfredoublons = models.IntegerField(db_column='effectifEleves2HFRedoublons', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hfrefugies = models.IntegerField(db_column='effectifEleves2HFRefugies', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hgautochtone = models.IntegerField(db_column='effectifEleves2HGAutochtone', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hgavechandicap = models.IntegerField(db_column='effectifEleves2HGAvecHandicap', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hgdeplacesexternes = models.IntegerField(db_column='effectifEleves2HGDeplacesExternes', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hgdeplacesinternes = models.IntegerField(db_column='effectifEleves2HGDeplacesInternes', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hgetrangers = models.IntegerField(db_column='effectifEleves2HGEtrangers', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hginternat = models.IntegerField(db_column='effectifEleves2HGInternat', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hgorphelins = models.IntegerField(db_column='effectifEleves2HGOrphelins', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hgreintegrant = models.IntegerField(db_column='effectifEleves2HGReIntegrant', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hgredoublons = models.IntegerField(db_column='effectifEleves2HGRedoublons', blank=True, null=True)  # Field name made lowercase.
    effectifeleves2hgrefugies = models.IntegerField(db_column='effectifEleves2HGRefugies', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hfautochtone = models.IntegerField(db_column='effectifEleves3HFAutochtone', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hfavechandicap = models.IntegerField(db_column='effectifEleves3HFAvecHandicap', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hfdeplacesexternes = models.IntegerField(db_column='effectifEleves3HFDeplacesExternes', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hfdeplacesinternes = models.IntegerField(db_column='effectifEleves3HFDeplacesInternes', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hfetrangers = models.IntegerField(db_column='effectifEleves3HFEtrangers', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hfinternat = models.IntegerField(db_column='effectifEleves3HFInternat', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hforphelins = models.IntegerField(db_column='effectifEleves3HFOrphelins', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hfreintegrant = models.IntegerField(db_column='effectifEleves3HFReIntegrant', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hfredoublons = models.IntegerField(db_column='effectifEleves3HFRedoublons', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hfrefugies = models.IntegerField(db_column='effectifEleves3HFRefugies', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hgautochtone = models.IntegerField(db_column='effectifEleves3HGAutochtone', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hgavechandicap = models.IntegerField(db_column='effectifEleves3HGAvecHandicap', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hgdeplacesexternes = models.IntegerField(db_column='effectifEleves3HGDeplacesExternes', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hgdeplacesinternes = models.IntegerField(db_column='effectifEleves3HGDeplacesInternes', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hgetrangers = models.IntegerField(db_column='effectifEleves3HGEtrangers', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hginternat = models.IntegerField(db_column='effectifEleves3HGInternat', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hgorphelins = models.IntegerField(db_column='effectifEleves3HGOrphelins', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hgreintegrant = models.IntegerField(db_column='effectifEleves3HGReIntegrant', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hgredoublons = models.IntegerField(db_column='effectifEleves3HGRedoublons', blank=True, null=True)  # Field name made lowercase.
    effectifeleves3hgrefugies = models.IntegerField(db_column='effectifEleves3HGRefugies', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hfautochtone = models.IntegerField(db_column='effectifEleves4HFAutochtone', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hfavechandicap = models.IntegerField(db_column='effectifEleves4HFAvecHandicap', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hfdeplacesexternes = models.IntegerField(db_column='effectifEleves4HFDeplacesExternes', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hfdeplacesinternes = models.IntegerField(db_column='effectifEleves4HFDeplacesInternes', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hfetrangers = models.IntegerField(db_column='effectifEleves4HFEtrangers', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hfinternat = models.IntegerField(db_column='effectifEleves4HFInternat', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hforphelins = models.IntegerField(db_column='effectifEleves4HFOrphelins', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hfreintegrant = models.IntegerField(db_column='effectifEleves4HFReIntegrant', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hfredoublons = models.IntegerField(db_column='effectifEleves4HFRedoublons', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hfrefugies = models.IntegerField(db_column='effectifEleves4HFRefugies', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hgautochtone = models.IntegerField(db_column='effectifEleves4HGAutochtone', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hgavechandicap = models.IntegerField(db_column='effectifEleves4HGAvecHandicap', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hgdeplacesexternes = models.IntegerField(db_column='effectifEleves4HGDeplacesExternes', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hgdeplacesinternes = models.IntegerField(db_column='effectifEleves4HGDeplacesInternes', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hgetrangers = models.IntegerField(db_column='effectifEleves4HGEtrangers', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hginternat = models.IntegerField(db_column='effectifEleves4HGInternat', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hgorphelins = models.IntegerField(db_column='effectifEleves4HGOrphelins', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hgreintegrant = models.IntegerField(db_column='effectifEleves4HGReIntegrant', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hgredoublons = models.IntegerField(db_column='effectifEleves4HGRedoublons', blank=True, null=True)  # Field name made lowercase.
    effectifeleves4hgrefugies = models.IntegerField(db_column='effectifEleves4HGRefugies', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7fautochtone = models.IntegerField(db_column='effectifEleves7FAutochtone', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7favechandicap = models.IntegerField(db_column='effectifEleves7FAvecHandicap', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7fdeplacesexternes = models.IntegerField(db_column='effectifEleves7FDeplacesExternes', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7fdeplacesinternes = models.IntegerField(db_column='effectifEleves7FDeplacesInternes', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7fetrangers = models.IntegerField(db_column='effectifEleves7FEtrangers', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7finternat = models.IntegerField(db_column='effectifEleves7FInternat', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7forphelins = models.IntegerField(db_column='effectifEleves7FOrphelins', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7freintegrant = models.IntegerField(db_column='effectifEleves7FReIntegrant', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7fredoublons = models.IntegerField(db_column='effectifEleves7FRedoublons', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7frefugies = models.IntegerField(db_column='effectifEleves7FRefugies', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7gautochtone = models.IntegerField(db_column='effectifEleves7GAutochtone', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7gavechandicap = models.IntegerField(db_column='effectifEleves7GAvecHandicap', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7gdeplacesexternes = models.IntegerField(db_column='effectifEleves7GDeplacesExternes', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7gdeplacesinternes = models.IntegerField(db_column='effectifEleves7GDeplacesInternes', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7getrangers = models.IntegerField(db_column='effectifEleves7GEtrangers', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7ginternat = models.IntegerField(db_column='effectifEleves7GInternat', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7gorphelins = models.IntegerField(db_column='effectifEleves7GOrphelins', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7greintegrant = models.IntegerField(db_column='effectifEleves7GReIntegrant', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7gredoublons = models.IntegerField(db_column='effectifEleves7GRedoublons', blank=True, null=True)  # Field name made lowercase.
    effectifeleves7grefugies = models.IntegerField(db_column='effectifEleves7GRefugies', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8fautochtone = models.IntegerField(db_column='effectifEleves8FAutochtone', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8favechandicap = models.IntegerField(db_column='effectifEleves8FAvecHandicap', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8fdeplacesexternes = models.IntegerField(db_column='effectifEleves8FDeplacesExternes', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8fdeplacesinternes = models.IntegerField(db_column='effectifEleves8FDeplacesInternes', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8fetrangers = models.IntegerField(db_column='effectifEleves8FEtrangers', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8finternat = models.IntegerField(db_column='effectifEleves8FInternat', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8forphelins = models.IntegerField(db_column='effectifEleves8FOrphelins', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8freintegrant = models.IntegerField(db_column='effectifEleves8FReIntegrant', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8fredoublons = models.IntegerField(db_column='effectifEleves8FRedoublons', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8frefugies = models.IntegerField(db_column='effectifEleves8FRefugies', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8gautochtone = models.IntegerField(db_column='effectifEleves8GAutochtone', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8gavechandicap = models.IntegerField(db_column='effectifEleves8GAvecHandicap', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8gdeplacesexternes = models.IntegerField(db_column='effectifEleves8GDeplacesExternes', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8gdeplacesinternes = models.IntegerField(db_column='effectifEleves8GDeplacesInternes', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8getrangers = models.IntegerField(db_column='effectifEleves8GEtrangers', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8ginternat = models.IntegerField(db_column='effectifEleves8GInternat', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8gorphelins = models.IntegerField(db_column='effectifEleves8GOrphelins', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8greintegrant = models.IntegerField(db_column='effectifEleves8GReIntegrant', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8gredoublons = models.IntegerField(db_column='effectifEleves8GRedoublons', blank=True, null=True)  # Field name made lowercase.
    effectifeleves8grefugies = models.IntegerField(db_column='effectifEleves8GRefugies', blank=True, null=True)  # Field name made lowercase.
    id = models.BigAutoField(primary_key=True)
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'st3_effectif_par_categorie_particuliere'


class St3Eleve(models.Model):
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    adresse = models.CharField(db_column='Adresse', max_length=255, blank=True, null=True)  # Field name made lowercase.
    datenaissance = models.CharField(db_column='DateNaissance', max_length=255, blank=True, null=True)  # Field name made lowercase.
    edition = models.CharField(db_column='Edition', max_length=255, blank=True, null=True)  # Field name made lowercase.
    filiere = models.CharField(db_column='Filiere', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nom = models.CharField(db_column='Nom', max_length=255, blank=True, null=True)  # Field name made lowercase.
    observation = models.CharField(db_column='Observation', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sexe = models.CharField(db_column='Sexe', max_length=255, blank=True, null=True)  # Field name made lowercase.
    telephone = models.CharField(db_column='Telephone', max_length=255, blank=True, null=True)  # Field name made lowercase.
    telephoneparent = models.CharField(db_column='TelephoneParent', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'st3_eleve'


class St3EnregistrementEquipement(models.Model):
    nombreequipementsbon = models.IntegerField(db_column='NombreEquipementsBon', blank=True, null=True)  # Field name made lowercase.
    nombreequipementsmauvais = models.IntegerField(db_column='NombreEquipementsMauvais', blank=True, null=True)  # Field name made lowercase.
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    nomequipement = models.CharField(db_column='NomEquipement', max_length=255, blank=True, null=True)  # Field name made lowercase.
    typeatelieroulabo = models.CharField(db_column='TypeAtelierOuLabo', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'st3_enregistrement_equipement'


class St3EquipementExistant(models.Model):
    nombreequipementsbon = models.IntegerField(db_column='NombreEquipementsBon', blank=True, null=True)  # Field name made lowercase.
    nombreequipementsmauvais = models.IntegerField(db_column='NombreEquipementsMauvais', blank=True, null=True)  # Field name made lowercase.
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    nomequipement = models.CharField(db_column='NomEquipement', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'st3_equipement_existant'


class St3Formation(models.Model):
    st3_enseignants_formes_genre = models.IntegerField(blank=True, null=True)
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'st3_formation'


class St3InfrastructureActivites(models.Model):
    st3_activites_parascolaires = models.TextField(blank=True, null=True)  # This field type is a guess.
    st3_gouvernement_eleves = models.TextField(blank=True, null=True)  # This field type is a guess.
    st3_unite_pedagogique = models.TextField(blank=True, null=True)  # This field type is a guess.
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    st3_pv_reunions = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'st3_infrastructure_activites'


class St3ManuelDisponibleNiveau(models.Model):
    st_3_manuel_autre_1eme_h_annee = models.IntegerField(db_column='st_3_manuel_Autre_1eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_autre_2eme_h_annee = models.IntegerField(db_column='st_3_manuel_Autre_2eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_autre_3eme_h_annee = models.IntegerField(db_column='st_3_manuel_Autre_3eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_autre_4eme_h_annee = models.IntegerField(db_column='st_3_manuel_Autre_4eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_autre_7eme_annee = models.IntegerField(db_column='st_3_manuel_Autre_7eme_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_autre_8eme_annee = models.IntegerField(db_column='st_3_manuel_Autre_8eme_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_educationciviquemorale_1eme_h_annee = models.IntegerField(db_column='st_3_manuel_EducationCiviqueMorale_1eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_educationciviquemorale_2eme_h_annee = models.IntegerField(db_column='st_3_manuel_EducationCiviqueMorale_2eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_educationciviquemorale_3eme_h_annee = models.IntegerField(db_column='st_3_manuel_EducationCiviqueMorale_3eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_educationciviquemorale_4eme_h_annee = models.IntegerField(db_column='st_3_manuel_EducationCiviqueMorale_4eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_educationciviquemorale_7eme_annee = models.IntegerField(db_column='st_3_manuel_EducationCiviqueMorale_7eme_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_educationciviquemorale_8eme_annee = models.IntegerField(db_column='st_3_manuel_EducationCiviqueMorale_8eme_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_mathematique_1eme_h_annee = models.IntegerField(db_column='st_3_manuel_Mathematique_1eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_mathematique_2eme_h_annee = models.IntegerField(db_column='st_3_manuel_Mathematique_2eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_mathematique_3eme_h_annee = models.IntegerField(db_column='st_3_manuel_Mathematique_3eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_mathematique_4eme_h_annee = models.IntegerField(db_column='st_3_manuel_Mathematique_4eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_mathematique_7eme_annee = models.IntegerField(db_column='st_3_manuel_Mathematique_7eme_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_mathematique_8eme_annee = models.IntegerField(db_column='st_3_manuel_Mathematique_8eme_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_pourfiliere_1eme_h_annee = models.IntegerField(db_column='st_3_manuel_PourFiliere_1eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_pourfiliere_2eme_h_annee = models.IntegerField(db_column='st_3_manuel_PourFiliere_2eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_pourfiliere_3eme_h_annee = models.IntegerField(db_column='st_3_manuel_PourFiliere_3eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_pourfiliere_4eme_h_annee = models.IntegerField(db_column='st_3_manuel_PourFiliere_4eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_pourfiliere_7eme_annee = models.IntegerField(db_column='st_3_manuel_PourFiliere_7eme_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_pourfiliere_8eme_annee = models.IntegerField(db_column='st_3_manuel_PourFiliere_8eme_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_pourlapaix_1eme_h_annee = models.IntegerField(db_column='st_3_manuel_PourLapaix_1eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_pourlapaix_2eme_h_annee = models.IntegerField(db_column='st_3_manuel_PourLapaix_2eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_pourlapaix_3eme_h_annee = models.IntegerField(db_column='st_3_manuel_PourLapaix_3eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_pourlapaix_4eme_h_annee = models.IntegerField(db_column='st_3_manuel_PourLapaix_4eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_pourlapaix_7eme_annee = models.IntegerField(db_column='st_3_manuel_PourLapaix_7eme_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_pourlapaix_8eme_annee = models.IntegerField(db_column='st_3_manuel_PourLapaix_8eme_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_sciences_1eme_h_annee = models.IntegerField(db_column='st_3_manuel_Sciences_1eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_sciences_2eme_h_annee = models.IntegerField(db_column='st_3_manuel_Sciences_2eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_sciences_3eme_h_annee = models.IntegerField(db_column='st_3_manuel_Sciences_3eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_sciences_4eme_h_annee = models.IntegerField(db_column='st_3_manuel_Sciences_4eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_sciences_7eme_annee = models.IntegerField(db_column='st_3_manuel_Sciences_7eme_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_sciences_8eme_annee = models.IntegerField(db_column='st_3_manuel_Sciences_8eme_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_themestransversaux_1eme_h_annee = models.IntegerField(db_column='st_3_manuel_ThemesTransversaux_1eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_themestransversaux_2eme_h_annee = models.IntegerField(db_column='st_3_manuel_ThemesTransversaux_2eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_themestransversaux_3eme_h_annee = models.IntegerField(db_column='st_3_manuel_ThemesTransversaux_3eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_themestransversaux_4eme_h_annee = models.IntegerField(db_column='st_3_manuel_ThemesTransversaux_4eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_themestransversaux_7eme_annee = models.IntegerField(db_column='st_3_manuel_ThemesTransversaux_7eme_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_themestransversaux_8eme_annee = models.IntegerField(db_column='st_3_manuel_ThemesTransversaux_8eme_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_francais_1eme_h_annee = models.IntegerField(db_column='st_3_manuel_francais_1eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_francais_2eme_h_annee = models.IntegerField(db_column='st_3_manuel_francais_2eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_francais_3eme_h_annee = models.IntegerField(db_column='st_3_manuel_francais_3eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_francais_4eme_h_annee = models.IntegerField(db_column='st_3_manuel_francais_4eme_H_annee', blank=True, null=True)  # Field name made lowercase.
    st_3_manuel_francais_7eme_annee = models.IntegerField(blank=True, null=True)
    st_3_manuel_francais_8eme_annee = models.IntegerField(blank=True, null=True)
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'st3_manuel_disponible_niveau'


class St3NombreLocauxCaracteristiqueEtatMur(models.Model):
    st3_buradm_pf_be = models.IntegerField(db_column='st3_BurAdm_PF_BE', blank=True, null=True)  # Field name made lowercase.
    st3_buradm_pf_me = models.IntegerField(db_column='st3_BurAdm_PF_ME', blank=True, null=True)  # Field name made lowercase.
    st3_sc_pf_be = models.IntegerField(db_column='st3_SC_PF_BE', blank=True, null=True)  # Field name made lowercase.
    st3_sc_pf_me = models.IntegerField(db_column='st3_SC_PF_ME', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_autresendur_bon_etat = models.IntegerField(db_column='st_3_NombreLocaux_AutresEndur_Bon_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_autresendur_mauvais_etat = models.IntegerField(db_column='st_3_NombreLocaux_AutresEndur_Mauvais_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_autrespaille_feuillage_bon_etat = models.IntegerField(db_column='st_3_NombreLocaux_AutresPaille_Feuillage_Bon_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_autrespaille_feuillage_mauvais_etat = models.IntegerField(db_column='st_3_NombreLocaux_AutresPaille_Feuillage_Mauvais_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_autressemi_dur_bon_etat = models.IntegerField(db_column='st_3_NombreLocaux_AutresSemi_dur_Bon_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_autressemi_dur_mauvais_etat = models.IntegerField(db_column='st_3_NombreLocaux_AutresSemi_dur_Mauvais_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_autresterre_battu_bon_etat = models.IntegerField(db_column='st_3_NombreLocaux_AutresTerre_Battu_Bon_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_autresterre_mauvais_etat = models.IntegerField(db_column='st_3_NombreLocaux_AutresTerre_Mauvais_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_autres_dontdetruite_occupees = models.IntegerField(db_column='st_3_NombreLocaux_Autres_dontDetruite_occupees', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_bureauadministratifendur_bon_etat = models.IntegerField(db_column='st_3_NombreLocaux_BureauAdministratifEndur_Bon_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_bureauadministratifendur_mauvais_etat = models.IntegerField(db_column='st_3_NombreLocaux_BureauAdministratifEndur_Mauvais_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_bureauadministratifsemi_dur_bon_etat = models.IntegerField(db_column='st_3_NombreLocaux_BureauAdministratifSemi_dur_Bon_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_bureauadministratifsemi_dur_mauvais_etat = models.IntegerField(db_column='st_3_NombreLocaux_BureauAdministratifSemi_dur_Mauvais_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_bureauadministratifterre_battu_bon_etat = models.IntegerField(db_column='st_3_NombreLocaux_BureauAdministratifTerre_Battu_Bon_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_bureauadministratifterre_mauvais_etat = models.IntegerField(db_column='st_3_NombreLocaux_BureauAdministratifTerre_Mauvais_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_bureauadministratif_dontdetruite_occupees = models.IntegerField(db_column='st_3_NombreLocaux_BureauAdministratif_dontDetruite_occupees', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_laboratoireendur_bon_etat = models.IntegerField(db_column='st_3_NombreLocaux_LaboratoireEndur_Bon_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_laboratoireendur_mauvais_etat = models.IntegerField(db_column='st_3_NombreLocaux_LaboratoireEndur_Mauvais_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_laboratoirepaille_feuillage_bon_etat = models.IntegerField(db_column='st_3_NombreLocaux_LaboratoirePaille_Feuillage_Bon_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_laboratoirepaille_feuillage_mauvais_etat = models.IntegerField(db_column='st_3_NombreLocaux_LaboratoirePaille_Feuillage_Mauvais_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_laboratoiresemi_dur_bon_etat = models.IntegerField(db_column='st_3_NombreLocaux_LaboratoireSemi_dur_Bon_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_laboratoiresemi_dur_mauvais_etat = models.IntegerField(db_column='st_3_NombreLocaux_LaboratoireSemi_dur_Mauvais_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_laboratoireterre_battu_bon_etat = models.IntegerField(db_column='st_3_NombreLocaux_LaboratoireTerre_Battu_Bon_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_laboratoireterre_mauvais_etat = models.IntegerField(db_column='st_3_NombreLocaux_LaboratoireTerre_Mauvais_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_laboratoire_dontdetruite_occupees = models.IntegerField(db_column='st_3_NombreLocaux_Laboratoire_dontDetruite_occupees', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_latrinewcendur_bon_etat = models.IntegerField(db_column='st_3_NombreLocaux_LatrineWCEndur_Bon_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_latrinewcendur_mauvais_etat = models.IntegerField(db_column='st_3_NombreLocaux_LatrineWCEndur_Mauvais_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_latrinewcpaille_feuillage_bon_etat = models.IntegerField(db_column='st_3_NombreLocaux_LatrineWCPaille_Feuillage_Bon_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_latrinewcpaille_feuillage_mauvais_etat = models.IntegerField(db_column='st_3_NombreLocaux_LatrineWCPaille_Feuillage_Mauvais_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_latrinewcsemi_dur_bon_etat = models.IntegerField(db_column='st_3_NombreLocaux_LatrineWCSemi_dur_Bon_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_latrinewcsemi_dur_mauvais_etat = models.IntegerField(db_column='st_3_NombreLocaux_LatrineWCSemi_dur_Mauvais_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_latrinewcterre_battu_bon_etat = models.IntegerField(db_column='st_3_NombreLocaux_LatrineWCTerre_Battu_Bon_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_latrinewcterre_mauvais_etat = models.IntegerField(db_column='st_3_NombreLocaux_LatrineWCTerre_Mauvais_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_latrinewc_dontdetruite_occupees = models.IntegerField(db_column='st_3_NombreLocaux_LatrineWC_dontDetruite_occupees', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_magasinendur_bon_etat = models.IntegerField(db_column='st_3_NombreLocaux_MagasinEndur_Bon_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_magasinendur_mauvais_etat = models.IntegerField(db_column='st_3_NombreLocaux_MagasinEndur_Mauvais_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_magasinpaille_feuillage_bon_etat = models.IntegerField(db_column='st_3_NombreLocaux_MagasinPaille_Feuillage_Bon_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_magasinpaille_feuillage_mauvais_etat = models.IntegerField(db_column='st_3_NombreLocaux_MagasinPaille_Feuillage_Mauvais_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_magasinsemi_dur_bon_etat = models.IntegerField(db_column='st_3_NombreLocaux_MagasinSemi_dur_Bon_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_magasinsemi_dur_mauvais_etat = models.IntegerField(db_column='st_3_NombreLocaux_MagasinSemi_dur_Mauvais_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_magasinterre_battu_bon_etat = models.IntegerField(db_column='st_3_NombreLocaux_MagasinTerre_Battu_Bon_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_magasinterre_mauvais_etat = models.IntegerField(db_column='st_3_NombreLocaux_MagasinTerre_Mauvais_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_magasin_dontdetruite_occupees = models.IntegerField(db_column='st_3_NombreLocaux_Magasin_dontDetruite_occupees', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_sallecoursendur_bon_etat = models.IntegerField(db_column='st_3_NombreLocaux_salleCoursEndur_Bon_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_sallecoursendur_mauvais_etat = models.IntegerField(db_column='st_3_NombreLocaux_salleCoursEndur_Mauvais_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_sallecourssemi_dur_bon_etat = models.IntegerField(db_column='st_3_NombreLocaux_salleCoursSemi_dur_Bon_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_sallecourssemi_dur_mauvais_etat = models.IntegerField(db_column='st_3_NombreLocaux_salleCoursSemi_dur_Mauvais_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_sallecoursterre_battu_bon_etat = models.IntegerField(db_column='st_3_NombreLocaux_salleCoursTerre_Battu_Bon_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_sallecoursterre_mauvais_etat = models.IntegerField(db_column='st_3_NombreLocaux_salleCoursTerre_Mauvais_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_sallecours_dontdetruite_occupees = models.IntegerField(db_column='st_3_NombreLocaux_salleCours_dontDetruite_occupees', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_specialiseeendur_bon_etat = models.IntegerField(db_column='st_3_NombreLocaux_specialiseeEndur_Bon_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_specialiseeendur_mauvais_etat = models.IntegerField(db_column='st_3_NombreLocaux_specialiseeEndur_Mauvais_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_specialiseepaille_feuillage_bon_etat = models.IntegerField(db_column='st_3_NombreLocaux_specialiseePaille_Feuillage_Bon_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_specialiseepaille_feuillage_mauvais_etat = models.IntegerField(db_column='st_3_NombreLocaux_specialiseePaille_Feuillage_Mauvais_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_specialiseesemi_dur_bon_etat = models.IntegerField(db_column='st_3_NombreLocaux_specialiseeSemi_dur_Bon_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_specialiseesemi_dur_mauvais_etat = models.IntegerField(db_column='st_3_NombreLocaux_specialiseeSemi_dur_Mauvais_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_specialiseeterre_battu_bon_etat = models.IntegerField(db_column='st_3_NombreLocaux_specialiseeTerre_Battu_Bon_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_specialiseeterre_mauvais_etat = models.IntegerField(db_column='st_3_NombreLocaux_specialiseeTerre_Mauvais_Etat', blank=True, null=True)  # Field name made lowercase.
    st_3_nombrelocaux_specialisee_dontdetruite_occupees = models.IntegerField(db_column='st_3_NombreLocaux_specialisee_dontDetruite_occupees', blank=True, null=True)  # Field name made lowercase.
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'st3_nombre_locaux_caracteristique_etat_mur'


class St3NombreLocauxCaracteristiqueEtatNatureToillette(models.Model):
    st3_nloc_autres_detocc = models.IntegerField(db_column='st3_NLoc_Autres_DetOcc', blank=True, null=True)  # Field name made lowercase.
    st3_nloc_autres_pf_bon = models.IntegerField(db_column='st3_NLoc_Autres_PF_Bon', blank=True, null=True)  # Field name made lowercase.
    st3_nloc_autres_pf_mauv = models.IntegerField(db_column='st3_NLoc_Autres_PF_Mauv', blank=True, null=True)  # Field name made lowercase.
    st3_nloc_buradm_detocc = models.IntegerField(db_column='st3_NLoc_BurAdm_DetOcc', blank=True, null=True)  # Field name made lowercase.
    st3_nloc_buradm_pf_bon = models.IntegerField(db_column='st3_NLoc_BurAdm_PF_Bon', blank=True, null=True)  # Field name made lowercase.
    st3_nloc_buradm_pf_mauv = models.IntegerField(db_column='st3_NLoc_BurAdm_PF_Mauv', blank=True, null=True)  # Field name made lowercase.
    st3_nloc_cours_detocc = models.IntegerField(db_column='st3_NLoc_Cours_DetOcc', blank=True, null=True)  # Field name made lowercase.
    st3_nloc_cours_pf_bon = models.IntegerField(db_column='st3_NLoc_Cours_PF_Bon', blank=True, null=True)  # Field name made lowercase.
    st3_nloc_cours_pf_mauv = models.IntegerField(db_column='st3_NLoc_Cours_PF_Mauv', blank=True, null=True)  # Field name made lowercase.
    st3_nloc_labo_detocc = models.IntegerField(db_column='st3_NLoc_Labo_DetOcc', blank=True, null=True)  # Field name made lowercase.
    st3_nloc_labo_pf_bon = models.IntegerField(db_column='st3_NLoc_Labo_PF_Bon', blank=True, null=True)  # Field name made lowercase.
    st3_nloc_labo_pf_mauv = models.IntegerField(db_column='st3_NLoc_Labo_PF_Mauv', blank=True, null=True)  # Field name made lowercase.
    st3_nloc_latrine_detocc = models.IntegerField(db_column='st3_NLoc_Latrine_DetOcc', blank=True, null=True)  # Field name made lowercase.
    st3_nloc_latrine_pf_bon = models.IntegerField(db_column='st3_NLoc_Latrine_PF_Bon', blank=True, null=True)  # Field name made lowercase.
    st3_nloc_latrine_pf_mauv = models.IntegerField(db_column='st3_NLoc_Latrine_PF_Mauv', blank=True, null=True)  # Field name made lowercase.
    st3_nloc_mag_detocc = models.IntegerField(db_column='st3_NLoc_Mag_DetOcc', blank=True, null=True)  # Field name made lowercase.
    st3_nloc_mag_pf_bon = models.IntegerField(db_column='st3_NLoc_Mag_PF_Bon', blank=True, null=True)  # Field name made lowercase.
    st3_nloc_mag_pf_mauv = models.IntegerField(db_column='st3_NLoc_Mag_PF_Mauv', blank=True, null=True)  # Field name made lowercase.
    st3_nloc_spec_detocc = models.IntegerField(db_column='st3_NLoc_Spec_DetOcc', blank=True, null=True)  # Field name made lowercase.
    st3_nloc_spec_pf_bon = models.IntegerField(db_column='st3_NLoc_Spec_PF_Bon', blank=True, null=True)  # Field name made lowercase.
    st3_nloc_spec_pf_mauv = models.IntegerField(db_column='st3_NLoc_Spec_PF_Mauv', blank=True, null=True)  # Field name made lowercase.
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'st3_nombre_locaux_caracteristique_etat_nature_toillette'


class St3NoteSection(models.Model):
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    st3_note = models.CharField(max_length=255, blank=True, null=True)
    st3_pv_reunions = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'st3_note_section'


class St3PersonnelAdministratifFonctionSexe(models.Model):
    st_3_nombreconseillerpedagogiquef_a1 = models.IntegerField(db_column='st_3_NombreConseillerPedagogiqueF_A1', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreconseillerpedagogiquef_autres = models.IntegerField(db_column='st_3_NombreConseillerPedagogiqueF_Autres', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreconseillerpedagogiquef_d6 = models.IntegerField(db_column='st_3_NombreConseillerPedagogiqueF_D6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreconseillerpedagogiquef_dr = models.IntegerField(db_column='st_3_NombreConseillerPedagogiqueF_DR', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreconseillerpedagogiquef_g3 = models.IntegerField(db_column='st_3_NombreConseillerPedagogiqueF_G3', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreconseillerpedagogiquef_ir = models.IntegerField(db_column='st_3_NombreConseillerPedagogiqueF_IR', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreconseillerpedagogiquef_l2 = models.IntegerField(db_column='st_3_NombreConseillerPedagogiqueF_L2', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreconseillerpedagogiquef_l2a = models.IntegerField(db_column='st_3_NombreConseillerPedagogiqueF_L2A', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreconseillerpedagogiquef_la = models.IntegerField(db_column='st_3_NombreConseillerPedagogiqueF_LA', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreconseillerpedagogiquef_moinsd6 = models.IntegerField(db_column='st_3_NombreConseillerPedagogiqueF_MoinsD6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreconseillerpedagogiquef_p6 = models.IntegerField(db_column='st_3_NombreConseillerPedagogiqueF_P6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreconseillerpedagogiqueh_a1 = models.IntegerField(db_column='st_3_NombreConseillerPedagogiqueH_A1', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreconseillerpedagogiqueh_autres = models.IntegerField(db_column='st_3_NombreConseillerPedagogiqueH_Autres', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreconseillerpedagogiqueh_d6 = models.IntegerField(db_column='st_3_NombreConseillerPedagogiqueH_D6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreconseillerpedagogiqueh_dr = models.IntegerField(db_column='st_3_NombreConseillerPedagogiqueH_DR', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreconseillerpedagogiqueh_g3 = models.IntegerField(db_column='st_3_NombreConseillerPedagogiqueH_G3', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreconseillerpedagogiqueh_ir = models.IntegerField(db_column='st_3_NombreConseillerPedagogiqueH_IR', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreconseillerpedagogiqueh_l2 = models.IntegerField(db_column='st_3_NombreConseillerPedagogiqueH_L2', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreconseillerpedagogiqueh_l2a = models.IntegerField(db_column='st_3_NombreConseillerPedagogiqueH_L2A', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreconseillerpedagogiqueh_la = models.IntegerField(db_column='st_3_NombreConseillerPedagogiqueH_LA', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreconseillerpedagogiqueh_moinsd6 = models.IntegerField(db_column='st_3_NombreConseillerPedagogiqueH_MoinsD6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreconseillerpedagogiqueh_p6 = models.IntegerField(db_column='st_3_NombreConseillerPedagogiqueH_P6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteurdisciplinef_a1 = models.IntegerField(db_column='st_3_NombreDirecteurDisciplineF_A1', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteurdisciplinef_autres = models.IntegerField(db_column='st_3_NombreDirecteurDisciplineF_Autres', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteurdisciplinef_d6 = models.IntegerField(db_column='st_3_NombreDirecteurDisciplineF_D6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteurdisciplinef_dr = models.IntegerField(db_column='st_3_NombreDirecteurDisciplineF_DR', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteurdisciplinef_g3 = models.IntegerField(db_column='st_3_NombreDirecteurDisciplineF_G3', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteurdisciplinef_ir = models.IntegerField(db_column='st_3_NombreDirecteurDisciplineF_IR', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteurdisciplinef_l2 = models.IntegerField(db_column='st_3_NombreDirecteurDisciplineF_L2', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteurdisciplinef_l2a = models.IntegerField(db_column='st_3_NombreDirecteurDisciplineF_L2A', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteurdisciplinef_la = models.IntegerField(db_column='st_3_NombreDirecteurDisciplineF_LA', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteurdisciplinef_moinsd6 = models.IntegerField(db_column='st_3_NombreDirecteurDisciplineF_MoinsD6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteurdisciplinef_p6 = models.IntegerField(db_column='st_3_NombreDirecteurDisciplineF_P6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteurdisciplineh_a1 = models.IntegerField(db_column='st_3_NombreDirecteurDisciplineH_A1', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteurdisciplineh_autres = models.IntegerField(db_column='st_3_NombreDirecteurDisciplineH_Autres', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteurdisciplineh_d6 = models.IntegerField(db_column='st_3_NombreDirecteurDisciplineH_D6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteurdisciplineh_dr = models.IntegerField(db_column='st_3_NombreDirecteurDisciplineH_DR', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteurdisciplineh_g3 = models.IntegerField(db_column='st_3_NombreDirecteurDisciplineH_G3', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteurdisciplineh_ir = models.IntegerField(db_column='st_3_NombreDirecteurDisciplineH_IR', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteurdisciplineh_l2 = models.IntegerField(db_column='st_3_NombreDirecteurDisciplineH_L2', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteurdisciplineh_l2a = models.IntegerField(db_column='st_3_NombreDirecteurDisciplineH_L2A', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteurdisciplineh_la = models.IntegerField(db_column='st_3_NombreDirecteurDisciplineH_LA', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteurdisciplineh_moinsd6 = models.IntegerField(db_column='st_3_NombreDirecteurDisciplineH_MoinsD6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteurdisciplineh_p6 = models.IntegerField(db_column='st_3_NombreDirecteurDisciplineH_P6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteuretudesf_a1 = models.IntegerField(db_column='st_3_NombreDirecteurEtudesF_A1', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteuretudesf_autres = models.IntegerField(db_column='st_3_NombreDirecteurEtudesF_Autres', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteuretudesf_d6 = models.IntegerField(db_column='st_3_NombreDirecteurEtudesF_D6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteuretudesf_dr = models.IntegerField(db_column='st_3_NombreDirecteurEtudesF_DR', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteuretudesf_g3 = models.IntegerField(db_column='st_3_NombreDirecteurEtudesF_G3', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteuretudesf_ir = models.IntegerField(db_column='st_3_NombreDirecteurEtudesF_IR', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteuretudesf_l2 = models.IntegerField(db_column='st_3_NombreDirecteurEtudesF_L2', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteuretudesf_l2a = models.IntegerField(db_column='st_3_NombreDirecteurEtudesF_L2A', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteuretudesf_la = models.IntegerField(db_column='st_3_NombreDirecteurEtudesF_LA', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteuretudesf_moinsd6 = models.IntegerField(db_column='st_3_NombreDirecteurEtudesF_MoinsD6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteuretudesf_p6 = models.IntegerField(db_column='st_3_NombreDirecteurEtudesF_P6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteuretudesh_a1 = models.IntegerField(db_column='st_3_NombreDirecteurEtudesH_A1', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteuretudesh_autres = models.IntegerField(db_column='st_3_NombreDirecteurEtudesH_Autres', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteuretudesh_d6 = models.IntegerField(db_column='st_3_NombreDirecteurEtudesH_D6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteuretudesh_dr = models.IntegerField(db_column='st_3_NombreDirecteurEtudesH_DR', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteuretudesh_g3 = models.IntegerField(db_column='st_3_NombreDirecteurEtudesH_G3', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteuretudesh_ir = models.IntegerField(db_column='st_3_NombreDirecteurEtudesH_IR', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteuretudesh_l2 = models.IntegerField(db_column='st_3_NombreDirecteurEtudesH_L2', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteuretudesh_l2a = models.IntegerField(db_column='st_3_NombreDirecteurEtudesH_L2A', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteuretudesh_la = models.IntegerField(db_column='st_3_NombreDirecteurEtudesH_LA', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteuretudesh_moinsd6 = models.IntegerField(db_column='st_3_NombreDirecteurEtudesH_MoinsD6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombredirecteuretudesh_p6 = models.IntegerField(db_column='st_3_NombreDirecteurEtudesH_P6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreouvriersetautresf_a1 = models.IntegerField(db_column='st_3_NombreOuvriersEtAutresF_A1', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreouvriersetautresf_autres = models.IntegerField(db_column='st_3_NombreOuvriersEtAutresF_Autres', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreouvriersetautresf_d6 = models.IntegerField(db_column='st_3_NombreOuvriersEtAutresF_D6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreouvriersetautresf_dr = models.IntegerField(db_column='st_3_NombreOuvriersEtAutresF_DR', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreouvriersetautresf_g3 = models.IntegerField(db_column='st_3_NombreOuvriersEtAutresF_G3', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreouvriersetautresf_ir = models.IntegerField(db_column='st_3_NombreOuvriersEtAutresF_IR', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreouvriersetautresf_l2 = models.IntegerField(db_column='st_3_NombreOuvriersEtAutresF_L2', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreouvriersetautresf_l2a = models.IntegerField(db_column='st_3_NombreOuvriersEtAutresF_L2A', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreouvriersetautresf_la = models.IntegerField(db_column='st_3_NombreOuvriersEtAutresF_LA', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreouvriersetautresf_moinsd6 = models.IntegerField(db_column='st_3_NombreOuvriersEtAutresF_MoinsD6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreouvriersetautresf_p6 = models.IntegerField(db_column='st_3_NombreOuvriersEtAutresF_P6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreouvriersetautresh_a1 = models.IntegerField(db_column='st_3_NombreOuvriersEtAutresH_A1', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreouvriersetautresh_autres = models.IntegerField(db_column='st_3_NombreOuvriersEtAutresH_Autres', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreouvriersetautresh_d6 = models.IntegerField(db_column='st_3_NombreOuvriersEtAutresH_D6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreouvriersetautresh_dr = models.IntegerField(db_column='st_3_NombreOuvriersEtAutresH_DR', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreouvriersetautresh_g3 = models.IntegerField(db_column='st_3_NombreOuvriersEtAutresH_G3', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreouvriersetautresh_ir = models.IntegerField(db_column='st_3_NombreOuvriersEtAutresH_IR', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreouvriersetautresh_l2 = models.IntegerField(db_column='st_3_NombreOuvriersEtAutresH_L2', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreouvriersetautresh_l2a = models.IntegerField(db_column='st_3_NombreOuvriersEtAutresH_L2A', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreouvriersetautresh_la = models.IntegerField(db_column='st_3_NombreOuvriersEtAutresH_LA', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreouvriersetautresh_moinsd6 = models.IntegerField(db_column='st_3_NombreOuvriersEtAutresH_MoinsD6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreouvriersetautresh_p6 = models.IntegerField(db_column='st_3_NombreOuvriersEtAutresH_P6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreprefetetudesf_a1 = models.IntegerField(db_column='st_3_NombrePrefetEtudesF_A1', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreprefetetudesf_autres = models.IntegerField(db_column='st_3_NombrePrefetEtudesF_Autres', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreprefetetudesf_d6 = models.IntegerField(db_column='st_3_NombrePrefetEtudesF_D6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreprefetetudesf_dr = models.IntegerField(db_column='st_3_NombrePrefetEtudesF_DR', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreprefetetudesf_g3 = models.IntegerField(db_column='st_3_NombrePrefetEtudesF_G3', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreprefetetudesf_ir = models.IntegerField(db_column='st_3_NombrePrefetEtudesF_IR', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreprefetetudesf_l2 = models.IntegerField(db_column='st_3_NombrePrefetEtudesF_L2', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreprefetetudesf_l2a = models.IntegerField(db_column='st_3_NombrePrefetEtudesF_L2A', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreprefetetudesf_la = models.IntegerField(db_column='st_3_NombrePrefetEtudesF_LA', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreprefetetudesf_moinsd6 = models.IntegerField(db_column='st_3_NombrePrefetEtudesF_MoinsD6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreprefetetudesf_p6 = models.IntegerField(db_column='st_3_NombrePrefetEtudesF_P6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreprefetetudesh_a1 = models.IntegerField(db_column='st_3_NombrePrefetEtudesH_A1', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreprefetetudesh_autres = models.IntegerField(db_column='st_3_NombrePrefetEtudesH_Autres', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreprefetetudesh_d6 = models.IntegerField(db_column='st_3_NombrePrefetEtudesH_D6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreprefetetudesh_dr = models.IntegerField(db_column='st_3_NombrePrefetEtudesH_DR', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreprefetetudesh_g3 = models.IntegerField(db_column='st_3_NombrePrefetEtudesH_G3', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreprefetetudesh_ir = models.IntegerField(db_column='st_3_NombrePrefetEtudesH_IR', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreprefetetudesh_l2 = models.IntegerField(db_column='st_3_NombrePrefetEtudesH_L2', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreprefetetudesh_l2a = models.IntegerField(db_column='st_3_NombrePrefetEtudesH_L2A', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreprefetetudesh_la = models.IntegerField(db_column='st_3_NombrePrefetEtudesH_LA', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreprefetetudesh_moinsd6 = models.IntegerField(db_column='st_3_NombrePrefetEtudesH_MoinsD6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreprefetetudesh_p6 = models.IntegerField(db_column='st_3_NombrePrefetEtudesH_P6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombresurveillantf_a1 = models.IntegerField(db_column='st_3_NombreSurveillantF_A1', blank=True, null=True)  # Field name made lowercase.
    st_3_nombresurveillantf_autres = models.IntegerField(db_column='st_3_NombreSurveillantF_Autres', blank=True, null=True)  # Field name made lowercase.
    st_3_nombresurveillantf_d6 = models.IntegerField(db_column='st_3_NombreSurveillantF_D6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombresurveillantf_dr = models.IntegerField(db_column='st_3_NombreSurveillantF_DR', blank=True, null=True)  # Field name made lowercase.
    st_3_nombresurveillantf_g3 = models.IntegerField(db_column='st_3_NombreSurveillantF_G3', blank=True, null=True)  # Field name made lowercase.
    st_3_nombresurveillantf_ir = models.IntegerField(db_column='st_3_NombreSurveillantF_IR', blank=True, null=True)  # Field name made lowercase.
    st_3_nombresurveillantf_l2 = models.IntegerField(db_column='st_3_NombreSurveillantF_L2', blank=True, null=True)  # Field name made lowercase.
    st_3_nombresurveillantf_l2a = models.IntegerField(db_column='st_3_NombreSurveillantF_L2A', blank=True, null=True)  # Field name made lowercase.
    st_3_nombresurveillantf_la = models.IntegerField(db_column='st_3_NombreSurveillantF_LA', blank=True, null=True)  # Field name made lowercase.
    st_3_nombresurveillantf_moinsd6 = models.IntegerField(db_column='st_3_NombreSurveillantF_MoinsD6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombresurveillantf_p6 = models.IntegerField(db_column='st_3_NombreSurveillantF_P6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombresurveillanth_a1 = models.IntegerField(db_column='st_3_NombreSurveillantH_A1', blank=True, null=True)  # Field name made lowercase.
    st_3_nombresurveillanth_autres = models.IntegerField(db_column='st_3_NombreSurveillantH_Autres', blank=True, null=True)  # Field name made lowercase.
    st_3_nombresurveillanth_d6 = models.IntegerField(db_column='st_3_NombreSurveillantH_D6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombresurveillanth_dr = models.IntegerField(db_column='st_3_NombreSurveillantH_DR', blank=True, null=True)  # Field name made lowercase.
    st_3_nombresurveillanth_g3 = models.IntegerField(db_column='st_3_NombreSurveillantH_G3', blank=True, null=True)  # Field name made lowercase.
    st_3_nombresurveillanth_ir = models.IntegerField(db_column='st_3_NombreSurveillantH_IR', blank=True, null=True)  # Field name made lowercase.
    st_3_nombresurveillanth_l2 = models.IntegerField(db_column='st_3_NombreSurveillantH_L2', blank=True, null=True)  # Field name made lowercase.
    st_3_nombresurveillanth_l2a = models.IntegerField(db_column='st_3_NombreSurveillantH_L2A', blank=True, null=True)  # Field name made lowercase.
    st_3_nombresurveillanth_la = models.IntegerField(db_column='st_3_NombreSurveillantH_LA', blank=True, null=True)  # Field name made lowercase.
    st_3_nombresurveillanth_moinsd6 = models.IntegerField(db_column='st_3_NombreSurveillantH_MoinsD6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombresurveillanth_p6 = models.IntegerField(db_column='st_3_NombreSurveillantH_P6', blank=True, null=True)  # Field name made lowercase.
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'st3_personnel_administratif_fonction_sexe'


class St3PersonnelEnseignant(models.Model):
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    chef_cote_positif = models.CharField(max_length=255, blank=True, null=True)
    chef_formation = models.CharField(max_length=255, blank=True, null=True)
    educateurs_cotes_positifs = models.CharField(max_length=255, blank=True, null=True)
    educateurs_formes = models.CharField(max_length=255, blank=True, null=True)
    educateurs_inspectes = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'st3_personnel_enseignant'


class St3PersonnelEnseignantSexeQualification(models.Model):
    st_3_nombreenseigantsecondairef_a1 = models.IntegerField(db_column='st_3_NombreEnseigantSecondaireF_A1', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreenseigantsecondairef_autres = models.IntegerField(db_column='st_3_NombreEnseigantSecondaireF_Autres', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreenseigantsecondairef_dr = models.IntegerField(db_column='st_3_NombreEnseigantSecondaireF_DR', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreenseigantsecondairef_g3 = models.IntegerField(db_column='st_3_NombreEnseigantSecondaireF_G3', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreenseigantsecondairef_ir = models.IntegerField(db_column='st_3_NombreEnseigantSecondaireF_IR', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreenseigantsecondairef_l2 = models.IntegerField(db_column='st_3_NombreEnseigantSecondaireF_L2', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreenseigantsecondairef_l2a = models.IntegerField(db_column='st_3_NombreEnseigantSecondaireF_L2A', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreenseigantsecondairef_la = models.IntegerField(db_column='st_3_NombreEnseigantSecondaireF_LA', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreenseigantsecondairef_moinsd6 = models.IntegerField(db_column='st_3_NombreEnseigantSecondaireF_MoinsD6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreenseigantsecondairef_p6 = models.IntegerField(db_column='st_3_NombreEnseigantSecondaireF_P6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreenseigantsecondaireh_a1 = models.IntegerField(db_column='st_3_NombreEnseigantSecondaireH_A1', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreenseigantsecondaireh_autres = models.IntegerField(db_column='st_3_NombreEnseigantSecondaireH_Autres', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreenseigantsecondaireh_dr = models.IntegerField(db_column='st_3_NombreEnseigantSecondaireH_DR', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreenseigantsecondaireh_g3 = models.IntegerField(db_column='st_3_NombreEnseigantSecondaireH_G3', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreenseigantsecondaireh_ir = models.IntegerField(db_column='st_3_NombreEnseigantSecondaireH_IR', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreenseigantsecondaireh_l2 = models.IntegerField(db_column='st_3_NombreEnseigantSecondaireH_L2', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreenseigantsecondaireh_l2a = models.IntegerField(db_column='st_3_NombreEnseigantSecondaireH_L2A', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreenseigantsecondaireh_la = models.IntegerField(db_column='st_3_NombreEnseigantSecondaireH_LA', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreenseigantsecondaireh_moinsd6 = models.IntegerField(db_column='st_3_NombreEnseigantSecondaireH_MoinsD6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreenseigantsecondaireh_p6 = models.IntegerField(db_column='st_3_NombreEnseigantSecondaireH_P6', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreenseignantaretraite = models.IntegerField(db_column='st_3_NombreEnseignantARetraite', blank=True, null=True)  # Field name made lowercase.
    st_3_nombreenseignantnonpaye = models.IntegerField(db_column='st_3_NombreEnseignantNonPaye', blank=True, null=True)  # Field name made lowercase.
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'st3_personnel_enseignant_sexe_qualification'


class St3RepartitionTempsFormation(models.Model):
    nombreheureformationpratique = models.IntegerField(db_column='NombreHeureFormationPratique', blank=True, null=True)  # Field name made lowercase.
    nombreheureformationstage = models.IntegerField(db_column='NombreHeureFormationStage', blank=True, null=True)  # Field name made lowercase.
    nombreheureformationtheorique = models.IntegerField(db_column='NombreHeureFormationTheorique', blank=True, null=True)  # Field name made lowercase.
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    nomfiliere = models.CharField(db_column='NomFiliere', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'st3_repartition_temps_formation'


class St3ReseauxEnvironnement(models.Model):
    st3_chef_participe_rld = models.TextField(blank=True, null=True)  # This field type is a guess.
    st3_coins_dechets = models.TextField(blank=True, null=True)  # This field type is a guess.
    st3_dispose_arbres = models.TextField(blank=True, null=True)  # This field type is a guess.
    st3_nombre_arbres_plantes = models.IntegerField(blank=True, null=True)
    st3_nombre_enseignant_formes_sur_administration_1_soin = models.IntegerField(blank=True, null=True)
    st3_participation_rep = models.TextField(blank=True, null=True)  # This field type is a guess.
    st3_reseaux_locaux_directeurs = models.TextField(blank=True, null=True)  # This field type is a guess.
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'st3_reseaux_environnement'


class St3ResultatExamenEtat(models.Model):
    elevesinscritsf = models.IntegerField(db_column='ElevesInscritsF', blank=True, null=True)  # Field name made lowercase.
    elevesinscritsg = models.IntegerField(db_column='ElevesInscritsG', blank=True, null=True)  # Field name made lowercase.
    elevespresentesf = models.IntegerField(db_column='ElevesPresentesF', blank=True, null=True)  # Field name made lowercase.
    elevespresentesg = models.IntegerField(db_column='ElevesPresentesG', blank=True, null=True)  # Field name made lowercase.
    equipement = models.IntegerField(blank=True, null=True)
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    nomdufiliere = models.CharField(db_column='NomDuFiliere', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'st3_resultat_examen_etat'


class St3ResultatJuryNational(models.Model):
    nombreparticipantsf = models.IntegerField(db_column='NombreParticipantsF', blank=True, null=True)  # Field name made lowercase.
    nombreparticipantsg = models.IntegerField(db_column='NombreParticipantsG', blank=True, null=True)  # Field name made lowercase.
    nombrereussitesf = models.IntegerField(db_column='NombreReussitesF', blank=True, null=True)  # Field name made lowercase.
    nombrereussitesg = models.IntegerField(db_column='NombreReussitesG', blank=True, null=True)  # Field name made lowercase.
    form_st = models.OneToOneField(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    nomfiliere = models.CharField(db_column='NomFiliere', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'st3_resultat_jury_national'


class StatistiqueEnseignantsForme(models.Model):
    nb_enseignants_evf = models.IntegerField(blank=True, null=True)
    nb_enseignants_forme_f = models.IntegerField(blank=True, null=True)
    nb_enseignants_forme_h = models.IntegerField(blank=True, null=True)
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    nb_enseignants_dispense_h = models.CharField(max_length=255, blank=True, null=True)
    nb_enseignants_dispense_f = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'statistique_enseignants_forme'


class Territoires(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    fk_proved = models.ForeignKey(Proveds, models.DO_NOTHING, blank=True, null=True)
    fk_province = models.ForeignKey(Provinces, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    libelle = models.CharField(max_length=255, blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'territoires'


class TypeEnseignement(models.Model):
    libelle = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'type_enseignement'


class User(models.Model):
    fk_province_id = models.BigIntegerField(blank=True, null=True)
    fk_proved_id = models.BigIntegerField(blank=True, null=True)
    fk_sous_proved_id = models.BigIntegerField(blank=True, null=True)
    picture_id = models.BigIntegerField(blank=True, null=True)
    fk_territoire_id = models.BigIntegerField(blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    roles = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    about = models.CharField(max_length=255, blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField(blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='firstName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fkprovedid = models.BigIntegerField(db_column='fkProvedId', blank=True, null=True)  # Field name made lowercase.
    fkprovinceid = models.BigIntegerField(db_column='fkProvinceId', blank=True, null=True)  # Field name made lowercase.
    fksousprovedid = models.BigIntegerField(db_column='fkSousProvedId', blank=True, null=True)  # Field name made lowercase.
    fkterritoireid = models.BigIntegerField(db_column='fkTerritoireId', blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.TextField(db_column='isDeleted', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    pictureid = models.BigIntegerField(db_column='pictureId', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    mdp = models.CharField(max_length=255, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'user'


class Users(models.Model):
    active = models.TextField(blank=True, null=True)  # This field type is a guess.
    is_deleted = models.TextField(blank=True, null=True)  # This field type is a guess.
    created_at = models.DateTimeField(blank=True, null=True)
    fk_proved_id = models.BigIntegerField(blank=True, null=True)
    fk_province_id = models.BigIntegerField(blank=True, null=True)
    fk_sous_proved_id = models.BigIntegerField(blank=True, null=True)
    fk_territoire_id = models.BigIntegerField(blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    picture_id = models.BigIntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    mdp = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    roles = models.CharField(max_length=255, blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class VEffectifsSt1ProvinceSexe(models.Model):
    idannee = models.BigIntegerField(blank=True, null=True)
    province = models.CharField(max_length=1, blank=True, null=True)
    sexe = models.CharField(max_length=1)
    premiere_maternelle = models.DecimalField(db_column='Premiere_Maternelle', max_digits=48, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    deuxieme_maternelle = models.DecimalField(db_column='Deuxieme_Maternelle', max_digits=48, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    troisieme_maternelle = models.DecimalField(db_column='Troisieme_Maternelle', max_digits=48, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    total_general = models.DecimalField(db_column='Total_General', max_digits=52, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'v_effectifs_st1_province_sexe'


class VEffectifsSt1RegimeSexe(models.Model):
    idannee = models.BigIntegerField(blank=True, null=True)
    type = models.CharField(max_length=1, blank=True, null=True)
    regime = models.CharField(max_length=1)
    secteur = models.CharField(max_length=1)
    sexe = models.CharField(max_length=1)
    premiere_maternelle = models.DecimalField(db_column='Premiere_Maternelle', max_digits=48, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    deuxieme_maternelle = models.DecimalField(db_column='Deuxieme_Maternelle', max_digits=48, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    troisieme_maternelle = models.DecimalField(db_column='Troisieme_Maternelle', max_digits=48, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    total_general = models.DecimalField(db_column='Total_General', max_digits=52, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'v_effectifs_st1_regime_sexe'


class VEffectifsSt1RegimeSexeProvince(models.Model):
    idannee = models.BigIntegerField(blank=True, null=True)
    type = models.CharField(max_length=1, blank=True, null=True)
    province = models.CharField(max_length=1, blank=True, null=True)
    regime = models.CharField(max_length=1)
    secteur = models.CharField(max_length=1)
    sexe = models.CharField(max_length=1)
    premiere_maternelle = models.DecimalField(db_column='Premiere_Maternelle', max_digits=48, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    deuxieme_maternelle = models.DecimalField(db_column='Deuxieme_Maternelle', max_digits=48, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    troisieme_maternelle = models.DecimalField(db_column='Troisieme_Maternelle', max_digits=48, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    total_general = models.DecimalField(db_column='Total_General', max_digits=52, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'v_effectifs_st1_regime_sexe_province'


class VEffectifsSt2ParAge(models.Model):
    idannee = models.BigIntegerField(blank=True, null=True)
    niveau = models.CharField(max_length=1)
    moins_6 = models.DecimalField(max_digits=44, decimal_places=0, blank=True, null=True)
    age_6 = models.DecimalField(max_digits=44, decimal_places=0, blank=True, null=True)
    age_7 = models.DecimalField(max_digits=44, decimal_places=0, blank=True, null=True)
    age_8 = models.DecimalField(max_digits=44, decimal_places=0, blank=True, null=True)
    age_9 = models.DecimalField(max_digits=44, decimal_places=0, blank=True, null=True)
    age_10 = models.DecimalField(max_digits=44, decimal_places=0, blank=True, null=True)
    age_11 = models.DecimalField(max_digits=44, decimal_places=0, blank=True, null=True)
    plus_11 = models.DecimalField(max_digits=44, decimal_places=0, blank=True, null=True)
    total_general = models.DecimalField(max_digits=51, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'v_effectifs_st2_par_age'


class VEffectifsSt2ParAgeProvinceSexe(models.Model):
    idannee = models.BigIntegerField(blank=True, null=True)
    province = models.CharField(max_length=1, blank=True, null=True)
    niveau = models.CharField(max_length=1)
    sexe = models.CharField(max_length=1)
    moins_6 = models.DecimalField(max_digits=44, decimal_places=0, blank=True, null=True)
    age_6 = models.DecimalField(max_digits=44, decimal_places=0, blank=True, null=True)
    age_7 = models.DecimalField(max_digits=44, decimal_places=0, blank=True, null=True)
    age_8 = models.DecimalField(max_digits=44, decimal_places=0, blank=True, null=True)
    age_9 = models.DecimalField(max_digits=44, decimal_places=0, blank=True, null=True)
    age_10 = models.DecimalField(max_digits=44, decimal_places=0, blank=True, null=True)
    age_11 = models.DecimalField(max_digits=44, decimal_places=0, blank=True, null=True)
    plus_11 = models.DecimalField(max_digits=44, decimal_places=0, blank=True, null=True)
    total_general = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'v_effectifs_st2_par_age_province_sexe'


class VEffectifsSt2ParAgeSexe(models.Model):
    idannee = models.BigIntegerField(blank=True, null=True)
    niveau = models.CharField(max_length=1)
    sexe = models.CharField(max_length=1)
    moins_6 = models.DecimalField(max_digits=44, decimal_places=0, blank=True, null=True)
    age_6 = models.DecimalField(max_digits=44, decimal_places=0, blank=True, null=True)
    age_7 = models.DecimalField(max_digits=44, decimal_places=0, blank=True, null=True)
    age_8 = models.DecimalField(max_digits=44, decimal_places=0, blank=True, null=True)
    age_9 = models.DecimalField(max_digits=44, decimal_places=0, blank=True, null=True)
    age_10 = models.DecimalField(max_digits=44, decimal_places=0, blank=True, null=True)
    age_11 = models.DecimalField(max_digits=44, decimal_places=0, blank=True, null=True)
    plus_11 = models.DecimalField(max_digits=44, decimal_places=0, blank=True, null=True)
    total_general = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'v_effectifs_st2_par_age_sexe'


class VEtablissementDetail(models.Model):
    etab_id = models.BigIntegerField()
    nometablissement = models.CharField(db_column='nomEtablissement', max_length=1)  # Field name made lowercase.
    adresseetablissement = models.CharField(db_column='adresseEtablissement', max_length=1, blank=True, null=True)  # Field name made lowercase.
    telephoneetablissement = models.CharField(db_column='telephoneEtablissement', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nomchefetablissement = models.CharField(db_column='nomChefEtablissement', max_length=1, blank=True, null=True)  # Field name made lowercase.
    annee_id = models.BigIntegerField()
    anneescolaire = models.CharField(db_column='anneeScolaire', max_length=1, blank=True, null=True)  # Field name made lowercase.
    province_id = models.BigIntegerField()
    province = models.CharField(max_length=1, blank=True, null=True)
    proved_id = models.BigIntegerField()
    proved = models.CharField(max_length=1, blank=True, null=True)
    sousproved_id = models.BigIntegerField(db_column='sousProved_id')  # Field name made lowercase.
    sousproved = models.CharField(db_column='sousProved', max_length=1, blank=True, null=True)  # Field name made lowercase.
    territoire_id = models.BigIntegerField()
    territoire = models.CharField(max_length=1, blank=True, null=True)
    typeenseignement = models.CharField(db_column='typeEnseignement', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ville = models.CharField(max_length=1, blank=True, null=True)
    secteur = models.CharField(max_length=1, blank=True, null=True)
    code_adm_ets = models.CharField(max_length=1, blank=True, null=True)
    territoire_txt = models.CharField(max_length=1, blank=True, null=True)
    centre_regroupement = models.CharField(max_length=1, blank=True, null=True)
    milieu = models.CharField(max_length=1, blank=True, null=True)
    latitude = models.CharField(max_length=1, blank=True, null=True)
    longitude = models.CharField(max_length=1, blank=True, null=True)
    regime_gestion = models.CharField(max_length=1, blank=True, null=True)
    matricule_secope = models.CharField(max_length=1, blank=True, null=True)
    reference_juridique = models.CharField(max_length=1, blank=True, null=True)
    statut_occupation = models.CharField(max_length=1, blank=True, null=True)
    isactive = models.IntegerField(db_column='isActive', blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.IntegerField(db_column='isDeleted', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'v_etablissement_detail'


class VEtablissementList(models.Model):
    etab_id = models.BigIntegerField()
    nometablissement = models.CharField(db_column='nomEtablissement', max_length=1)  # Field name made lowercase.
    adresseetablissement = models.CharField(db_column='adresseEtablissement', max_length=1, blank=True, null=True)  # Field name made lowercase.
    telephoneetablissement = models.CharField(db_column='telephoneEtablissement', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nomchefetablissement = models.CharField(db_column='nomChefEtablissement', max_length=1, blank=True, null=True)  # Field name made lowercase.
    anneescolaire = models.CharField(db_column='anneeScolaire', max_length=1, blank=True, null=True)  # Field name made lowercase.
    province = models.CharField(max_length=1, blank=True, null=True)
    proved = models.CharField(max_length=1, blank=True, null=True)
    sousproved = models.CharField(db_column='sousProved', max_length=1, blank=True, null=True)  # Field name made lowercase.
    territoire = models.CharField(max_length=1, blank=True, null=True)
    isactive = models.IntegerField(db_column='isActive', blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.IntegerField(db_column='isDeleted', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'v_etablissement_list'


class VGombeAutre(models.Model):
    id = models.AutoField(primary_key=True)
    sous_division = models.CharField(max_length=1)
    nom_etablissement = models.CharField(max_length=1)
    numero_dinacope = models.CharField(max_length=1, blank=True, null=True)
    niveau = models.CharField(max_length=1, blank=True, null=True)
    regime_gestion = models.CharField(max_length=1, blank=True, null=True)
    quartier = models.CharField(max_length=1, blank=True, null=True)
    source_file = models.CharField(max_length=1, blank=True, null=True)
    imported_at = models.DateTimeField(blank=True, null=True)
    sousprovedid = models.BigIntegerField(db_column='sousProvedId')  # Field name made lowercase.
    provedid = models.BigIntegerField(db_column='provedId', blank=True, null=True)  # Field name made lowercase.
    provinceid = models.BigIntegerField(db_column='provinceId', blank=True, null=True)  # Field name made lowercase.
    nom_norm = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'v_gombe_autre'


class VGombeNorm(models.Model):
    id = models.AutoField(primary_key=True)
    sous_division = models.CharField(max_length=1)
    nom_etablissement = models.CharField(max_length=1)
    numero_dinacope = models.CharField(max_length=1, blank=True, null=True)
    niveau = models.CharField(max_length=1, blank=True, null=True)
    regime_gestion = models.CharField(max_length=1, blank=True, null=True)
    quartier = models.CharField(max_length=1, blank=True, null=True)
    source_file = models.CharField(max_length=1, blank=True, null=True)
    imported_at = models.DateTimeField(blank=True, null=True)
    sousprovedid = models.BigIntegerField(db_column='sousProvedId')  # Field name made lowercase.
    provedid = models.BigIntegerField(db_column='provedId', blank=True, null=True)  # Field name made lowercase.
    provinceid = models.BigIntegerField(db_column='provinceId', blank=True, null=True)  # Field name made lowercase.
    nom_norm = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'v_gombe_norm'


class VReportingEtablissements(models.Model):
    formulaire_id = models.BigIntegerField()
    etablissement_id = models.BigIntegerField(blank=True, null=True)
    nom_etablissement = models.CharField(max_length=1, blank=True, null=True)
    chef_etablissement = models.CharField(max_length=1, blank=True, null=True)
    telephone = models.CharField(max_length=1, blank=True, null=True)
    adresse = models.CharField(max_length=1, blank=True, null=True)
    annee_id = models.BigIntegerField(blank=True, null=True)
    annee_scolaire = models.CharField(max_length=1, blank=True, null=True)
    province = models.CharField(max_length=1, blank=True, null=True)
    proved = models.CharField(max_length=1, blank=True, null=True)
    sous_proved = models.CharField(max_length=1, blank=True, null=True)
    territoire = models.CharField(max_length=1, blank=True, null=True)
    milieu = models.CharField(max_length=1, blank=True, null=True)
    latitude = models.CharField(max_length=1, blank=True, null=True)
    longitude = models.CharField(max_length=1, blank=True, null=True)
    altitude = models.CharField(max_length=1, blank=True, null=True)
    regime_gestion = models.CharField(max_length=1, blank=True, null=True)
    reference_juridique = models.CharField(max_length=1, blank=True, null=True)
    matricule_secope = models.CharField(max_length=1, blank=True, null=True)
    etat_etablissement = models.CharField(max_length=1, blank=True, null=True)
    statut_occupation = models.CharField(max_length=1, blank=True, null=True)
    internat = models.CharField(max_length=1, blank=True, null=True)
    cloture = models.CharField(max_length=1, blank=True, null=True)
    coges = models.CharField(max_length=1, blank=True, null=True)
    coges_operationnel = models.CharField(max_length=1, blank=True, null=True)
    copa = models.CharField(max_length=1, blank=True, null=True)
    copa_operationnel = models.CharField(max_length=1, blank=True, null=True)
    pris_en_charge_refugies = models.CharField(max_length=1, blank=True, null=True)
    point_eau = models.CharField(max_length=1, blank=True, null=True)
    type_point_eau = models.CharField(max_length=1, blank=True, null=True)
    sources_energie = models.CharField(max_length=1, blank=True, null=True)
    type_sources_energie = models.CharField(max_length=1, blank=True, null=True)
    cellule_orientation_evf = models.TextField(blank=True, null=True)  # This field type is a guess.
    enseignants_evf_formes = models.TextField(blank=True, null=True)  # This field type is a guess.
    env_discipline = models.TextField(blank=True, null=True)  # This field type is a guess.
    env_enseigne = models.TextField(blank=True, null=True)  # This field type is a guess.
    env_programme = models.TextField(blank=True, null=True)  # This field type is a guess.
    env_parascolaire = models.TextField(blank=True, null=True)  # This field type is a guess.
    vih_discipline = models.TextField(blank=True, null=True)  # This field type is a guess.
    vih_enseigne = models.TextField(blank=True, null=True)  # This field type is a guess.
    vih_programme = models.TextField(blank=True, null=True)  # This field type is a guess.
    vih_parascolaire = models.TextField(blank=True, null=True)  # This field type is a guess.
    reglement_discrimination = models.TextField(blank=True, null=True)  # This field type is a guess.
    reglement_harcelement = models.TextField(blank=True, null=True)  # This field type is a guess.
    reglement_securite_physique = models.TextField(blank=True, null=True)  # This field type is a guess.
    type_formulaire = models.CharField(max_length=1, blank=True, null=True)
    formulaire_repondu = models.IntegerField()
    formulaire_valide = models.IntegerField()
    derniere_mise_a_jour = models.DateTimeField()
    date_creation = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'v_reporting_etablissements'


class VStatistiquesClassesSt1(models.Model):
    idannee = models.BigIntegerField(blank=True, null=True)
    type = models.CharField(max_length=1, blank=True, null=True)
    regime_gestion = models.CharField(max_length=1)
    nb_salles_organisees_1ere = models.DecimalField(max_digits=43, decimal_places=0, blank=True, null=True)
    nb_salles_organisees_2eme = models.DecimalField(max_digits=43, decimal_places=0, blank=True, null=True)
    nb_salles_organisees_3eme = models.DecimalField(max_digits=43, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'v_statistiques_classes_st1'


class VStatistiquesClassesSt1Province(models.Model):
    idannee = models.BigIntegerField(blank=True, null=True)
    type = models.CharField(max_length=1, blank=True, null=True)
    province = models.CharField(max_length=1, blank=True, null=True)
    nb_salles_organisees_1ere = models.DecimalField(max_digits=43, decimal_places=0, blank=True, null=True)
    nb_salles_organisees_2eme = models.DecimalField(max_digits=43, decimal_places=0, blank=True, null=True)
    nb_salles_organisees_3eme = models.DecimalField(max_digits=43, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'v_statistiques_classes_st1_province'


class VStatistiquesClassesSt2(models.Model):
    idannee = models.BigIntegerField(blank=True, null=True)
    type = models.CharField(max_length=1, blank=True, null=True)
    regime_gestion = models.CharField(max_length=1)
    nb_classes_1ere = models.DecimalField(max_digits=43, decimal_places=0, blank=True, null=True)
    nb_classes_2eme = models.DecimalField(max_digits=43, decimal_places=0, blank=True, null=True)
    nb_classes_3eme = models.DecimalField(max_digits=43, decimal_places=0, blank=True, null=True)
    nb_classes_4eme = models.DecimalField(max_digits=43, decimal_places=0, blank=True, null=True)
    nb_classes_5eme = models.DecimalField(max_digits=43, decimal_places=0, blank=True, null=True)
    nb_classes_6eme = models.DecimalField(max_digits=43, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'v_statistiques_classes_st2'


class VStatistiquesClassesSt2Province(models.Model):
    idannee = models.BigIntegerField(blank=True, null=True)
    type = models.CharField(max_length=1, blank=True, null=True)
    province = models.CharField(max_length=1, blank=True, null=True)
    nb_classes_1ere = models.DecimalField(max_digits=43, decimal_places=0, blank=True, null=True)
    nb_classes_2eme = models.DecimalField(max_digits=43, decimal_places=0, blank=True, null=True)
    nb_classes_3eme = models.DecimalField(max_digits=43, decimal_places=0, blank=True, null=True)
    nb_classes_4eme = models.DecimalField(max_digits=43, decimal_places=0, blank=True, null=True)
    nb_classes_5eme = models.DecimalField(max_digits=43, decimal_places=0, blank=True, null=True)
    nb_classes_6eme = models.DecimalField(max_digits=43, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'v_statistiques_classes_st2_province'


class VStatistiquesNombreEcoleParMilieuEtProvince(models.Model):
    formulaire_id = models.BigIntegerField()
    idannee = models.BigIntegerField(blank=True, null=True)
    type = models.CharField(max_length=1, blank=True, null=True)
    province = models.CharField(max_length=1, blank=True, null=True)
    milieu = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'v_statistiques_nombre_ecole_par_milieu_et_province'


class VStatistiquesNombreEcoleParRegimeEtProvince(models.Model):
    formulaire_id = models.BigIntegerField()
    idannee = models.BigIntegerField(blank=True, null=True)
    type = models.CharField(max_length=1, blank=True, null=True)
    province = models.CharField(max_length=1, blank=True, null=True)
    regime_code = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'v_statistiques_nombre_ecole_par_regime_et_province'


class VTauxCouverture(models.Model):
    idannee = models.BigIntegerField(blank=True, null=True)
    province_id = models.BigIntegerField()
    province = models.CharField(max_length=1, blank=True, null=True)
    type = models.CharField(max_length=1, blank=True, null=True)
    nb_ecoles_existantes = models.BigIntegerField()
    nb_ecoles_repondues = models.BigIntegerField()
    taux_couverture = models.DecimalField(max_digits=26, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'v_taux_couverture'


class VTauxCouvertureRegime(models.Model):
    idannee = models.BigIntegerField(blank=True, null=True)
    province = models.CharField(max_length=1, blank=True, null=True)
    niveau = models.CharField(max_length=1, blank=True, null=True)
    regime = models.CharField(max_length=1, blank=True, null=True)
    nb_ecoles_existantes = models.BigIntegerField()
    nb_ecoles_repondues = models.BigIntegerField()
    taux_couverture = models.DecimalField(max_digits=26, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'v_taux_couverture_regime'


class VihSida(models.Model):
    vih_sida_active_parascolaire = models.TextField(blank=True, null=True)  # This field type is a guess.
    vih_sida_discipline = models.TextField(blank=True, null=True)  # This field type is a guess.
    vih_sida_enseigne = models.TextField(blank=True, null=True)  # This field type is a guess.
    vih_sida_programme = models.TextField(blank=True, null=True)  # This field type is a guess.
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'vih_sida'


class Villes(models.Model):
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    fkprovinceid = models.BigIntegerField(db_column='fkProvinceId', blank=True, null=True)  # Field name made lowercase.
    id = models.BigAutoField(primary_key=True)
    libelle = models.CharField(max_length=255, blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'villes'


class Violences(models.Model):
    abus_sexuels_f = models.IntegerField(blank=True, null=True)
    abus_sexuels_g = models.IntegerField(blank=True, null=True)
    autres_violences_f = models.IntegerField(blank=True, null=True)
    autres_violences_g = models.IntegerField(blank=True, null=True)
    chatiment_f = models.IntegerField(blank=True, null=True)
    chatiment_g = models.IntegerField(blank=True, null=True)
    discrimination_f = models.IntegerField(blank=True, null=True)
    discrimination_g = models.IntegerField(blank=True, null=True)
    harcelement_f = models.IntegerField(blank=True, null=True)
    harcelement_g = models.IntegerField(blank=True, null=True)
    intimidation_f = models.IntegerField(blank=True, null=True)
    intimidation_g = models.IntegerField(blank=True, null=True)
    form_st = models.ForeignKey(Formulaires, models.DO_NOTHING, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    reunions_pv_violence = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'violences'
