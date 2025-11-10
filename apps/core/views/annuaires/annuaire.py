from django.shortcuts import render

def annuaire_table_classe(request):
    """
    View simple pour afficher la page d'accueil avec base.html
    """
    context = {
        'titre': 'Mon Projet Django',
        'message': 'Bienvenue sur mon site !',
        'utilisateur': request.user.username if request.user.is_authenticated else 'Invité'
    }
    return render(request, 'annuaires/annuaire_table_classe.html', context)

def annuaire_table_ecole(request):
    """
    View simple pour afficher la page d'accueil avec base.html
    """
    context = {
        'titre': 'Mon Projet Django',
        'message': 'Bienvenue sur mon site !',
        'utilisateur': request.user.username if request.user.is_authenticated else 'Invité'
    }
    return render(request, 'annuaires/annuaire_table_ecole.html', context)






# views.py
from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

def annuaire_ecoles(request):
    """Vue principale pour l'annuaire des écoles"""
    context = {
        'annees_scolaires': get_annees_scolaires(),
        'provinces': get_provinces(),
        'types_enseignement': get_types_enseignement(),
    }
    return render(request, 'annuaires/annuaire_table_ecole.html', context)

@csrf_exempt
def get_table_data(request):
    """Endpoint AJAX pour récupérer les données des tableaux"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            regime_type = data.get('regime_type')
            filters = data.get('filters', {})
            
            # Appliquer les filtres
            where_conditions = ["f.responded = 1"]
            params = []
            
            annee = filters.get('annee')
            if annee:
                where_conditions.append("f.idannee = %s")
                params.append(annee)
                
            type_enseignement = filters.get('type_enseignement')
            if type_enseignement:
                where_conditions.append("UPPER(f.type) = UPPER(%s)")
                params.append(type_enseignement)
                
            province = filters.get('province')
            if province:
                where_conditions.append("p.id = %s")
                params.append(province)
            
            where_clause = " AND ".join(where_conditions)
            
            # Sélectionner la requête en fonction du type de régime
            if regime_type == 'regime_national':
                query = get_regime_national_query(where_clause)
            elif regime_type == 'regimes_proved':
                query = get_regimes_proved_query(where_clause)
            elif regime_type == 'milieu_proved':
                query = get_milieu_proved_query(where_clause)
            elif regime_type == 'public_proved':
                query = get_public_proved_query(where_clause)
            elif regime_type == 'milieu_public':
                query = get_milieu_public_query(where_clause)
            else:
                query = get_normal_query(where_clause)
            
            # Exécuter la requête
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                columns = [col[0] for col in cursor.description]
                results = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
            
            return JsonResponse({'success': True, 'data': results})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})

# Fonctions pour les différentes requêtes
def get_regime_national_query(where_clause):
    return f"""
    SELECT 
        i.secteur_enseignement AS secteur,
        COALESCE(i.regime_gestion, 'NR') AS regime_gestion,
        COUNT(*) AS total_etablissements,
        SUM(CASE WHEN COALESCE(i.regime_gestion, '') <> 'EPR' THEN 1 ELSE 0 END) AS total_public,
        SUM(CASE WHEN i.regime_gestion = 'EPR' THEN 1 ELSE 0 END) AS total_prive
    FROM identifications i
    INNER JOIN formulaires f 
        ON f.identification_id = i.id 
        AND {where_clause}
    GROUP BY i.secteur_enseignement, i.regime_gestion
    ORDER BY 
        CASE i.secteur_enseignement
            WHEN 'ECC' THEN 1
            WHEN 'ECF' THEN 2
            WHEN 'ECI' THEN 3
            WHEN 'ECK' THEN 4
            WHEN 'ECP' THEN 5
            WHEN 'ECS' THEN 6
            WHEN 'AUTRES' THEN 7
            WHEN 'ENC' THEN 8
            ELSE 9
        END,
        i.regime_gestion;
    """

def get_regimes_proved_query(where_clause):
    return f"""
    SELECT 
        p.id AS idProvince,
        p.libelle AS province,
        f.idannee,
        UPPER(f.type) AS type,
        
        -- Régimes de gestion en colonnes
        SUM(CASE WHEN i.regime_gestion = 'ECC' THEN 1 ELSE 0 END) AS ECC,
        SUM(CASE WHEN i.regime_gestion = 'ECF' THEN 1 ELSE 0 END) AS ECF,
        SUM(CASE WHEN i.regime_gestion = 'ECI' THEN 1 ELSE 0 END) AS ECI,
        SUM(CASE WHEN i.regime_gestion = 'ECK' THEN 1 ELSE 0 END) AS ECK,
        SUM(CASE WHEN i.regime_gestion = 'ECP' THEN 1 ELSE 0 END) AS ECP,
        SUM(CASE WHEN i.regime_gestion = 'ECS' THEN 1 ELSE 0 END) AS ECS,
        SUM(CASE WHEN i.regime_gestion = 'ENC' THEN 1 ELSE 0 END) AS ENC,
        SUM(CASE WHEN i.regime_gestion = 'EPR' THEN 1 ELSE 0 END) AS EPR,
        SUM(CASE WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN 1 ELSE 0 END) AS NR,

        -- Totaux
        SUM(CASE WHEN i.regime_gestion <> 'EPR' THEN 1 ELSE 0 END) AS Total_Public,
        SUM(CASE WHEN i.regime_gestion = 'EPR' THEN 1 ELSE 0 END) AS Total_Prive,
        COUNT(f.id) AS Total_General

    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE {where_clause}
    GROUP BY p.id, p.libelle, f.idannee, UPPER(f.type)
    ORDER BY p.id, f.idannee, UPPER(f.type);
    """

def get_milieu_proved_query(where_clause):
    return f"""
    SELECT 
        p.id AS idProvince,
        p.libelle AS province,
        f.idannee,
        UPPER(f.type) AS type,
        SUM(CASE WHEN UPPER(i.milieu) = 'URBAIN' THEN 1 ELSE 0 END) AS Urbain,
        SUM(CASE WHEN UPPER(i.milieu) = 'RURAL' THEN 1 ELSE 0 END) AS Rural,
        SUM(CASE WHEN i.milieu IS NULL OR i.milieu = '' THEN 1 ELSE 0 END) AS NR,
        COUNT(f.id) AS Total_General
    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE {where_clause}
    GROUP BY p.id, p.libelle, f.idannee, UPPER(f.type)
    ORDER BY p.id, f.idannee, UPPER(f.type);
    """

def get_public_proved_query(where_clause):
    return f"""
    SELECT 
        f.idannee,
        UPPER(f.type) AS type,
        p.id AS idProvince,
        p.libelle AS province,
        COUNT(f.id) AS nombre_ecoles_public
    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE {where_clause}
      AND (i.regime_gestion IS NOT NULL AND UPPER(i.regime_gestion) <> 'EPR')
    GROUP BY f.idannee, UPPER(f.type), p.id, p.libelle
    ORDER BY p.id, f.idannee, UPPER(f.type);
    """

def get_milieu_public_query(where_clause):
    return f"""
    SELECT 
        f.idannee,
        UPPER(f.type) AS type,
        p.id AS idProvince,
        p.libelle AS province,
        SUM(CASE WHEN UPPER(i.milieu) = 'URBAIN' THEN 1 ELSE 0 END) AS Urbain,
        SUM(CASE WHEN UPPER(i.milieu) = 'RURAL' THEN 1 ELSE 0 END) AS Rural,
        SUM(CASE WHEN i.milieu IS NULL OR i.milieu = '' THEN 1 ELSE 0 END) AS NR,
        COUNT(f.id) AS Total_Public
    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE {where_clause}
      AND (i.regime_gestion IS NOT NULL AND UPPER(i.regime_gestion) <> 'EPR')
    GROUP BY f.idannee, UPPER(f.type), p.id, p.libelle
    ORDER BY p.id, f.idannee, UPPER(f.type);
    """

def get_normal_query(where_clause):
    return f"""
    SELECT 
        f.id,
        f.idannee AS annee_scolaire,
        f.type AS type_enseignement,
        p.libelle AS province,
        CONCAT('Établissement ', f.id) AS nom_etablissement,  # Nom générique
        'Adresse non disponible' AS adresse,
        'Téléphone non disponible' AS telephone,
        'Chef non spécifié' AS chef_etablissement,
        'Actif' AS statut,
        f.created_at
    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE {where_clause}
    ORDER BY p.libelle, f.idannee
    LIMIT 100;
    """

# Fonctions utilitaires pour les filtres
def get_annees_scolaires():
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT idannee FROM formulaires WHERE responded = 1 ORDER BY idannee DESC")
        return [row[0] for row in cursor.fetchall()]

def get_provinces():
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, libelle FROM provinces ORDER BY libelle")
        return [{'id': row[0], 'libelle': row[1]} for row in cursor.fetchall()]

def get_types_enseignement():
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT UPPER(type) FROM formulaires WHERE responded = 1 ORDER BY type")
        return [row[0] for row in cursor.fetchall()]



def annuaire_table_eleve(request):
    """
    View simple pour afficher la page d'accueil avec base.html
    """
    context = {
        'titre': 'Mon Projet Django',
        'message': 'Bienvenue sur mon site !',
        'utilisateur': request.user.username if request.user.is_authenticated else 'Invité'
    }
    return render(request, 'annuaires/annuaire_table_eleve.html', context)

def annuaire_table_enseignant(request):
    """
    View simple pour afficher la page d'accueil avec base.html
    """
    context = {
        'titre': 'Mon Projet Django',
        'message': 'Bienvenue sur mon site !',
        'utilisateur': request.user.username if request.user.is_authenticated else 'Invité'
    }
    return render(request, 'annuaires/annuaire_table_enseignant.html', context)

def annuaire_form(request):
    """
    Une autre view simple pour tester
    """
    context = {
        'titre': 'À Propos',
        'message': 'Cette page utilise le template base.html'
    }
    return render(request, 'annuaires/annuaire_forms.html', context)