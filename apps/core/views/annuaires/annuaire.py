from django.shortcuts import render

# views.py
from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
import xlwt
import csv
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import datetime

def annuaire_ecoles(request):
    """Vue principale pour l'annuaire des écoles"""
    context = {
        'annees_scolaires': get_annees_scolaires(),
        'provinces': get_provinces(),
        'types_enseignement': get_types_enseignement(),
        'milieux': get_milieux(),
    }
    return render(request, 'annuaires/annuaire_table_ecole.html', context)

@csrf_exempt
def get_table_data(request):
    """Endpoint AJAX pour récupérer les données des tableaux avec pagination"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            regime_type = data.get('regime_type')
            filters = data.get('filters', {})
            page = int(data.get('page', 1))
            page_size = int(data.get('page_size', 10))
            
            # Calculer l'offset pour la pagination
            offset = (page - 1) * page_size
            
            # Appliquer TOUS les filtres
            where_conditions = ["f.responded = 1"]
            params = []
            
            # Filtre année scolaire
            annee = filters.get('annee')
            if annee:
                where_conditions.append("f.idannee = %s")
                params.append(annee)
                
            # Filtre type d'enseignement (ST1, ST2, ST3)
            type_enseignement = filters.get('type_enseignement')
            if type_enseignement:
                where_conditions.append("UPPER(f.type) = UPPER(%s)")
                params.append(type_enseignement)
                
            # Filtre province (proved)
            province = filters.get('province')
            if province:
                where_conditions.append("p.id = %s")
                params.append(province)
            
            # Filtre milieu (urbain, rural)
            milieu = filters.get('milieu')
            if milieu:
                where_conditions.append("UPPER(i.milieu) = UPPER(%s)")
                params.append(milieu)
            
            # Filtre secteur (public, privé)
            secteur = filters.get('secteur')
            if secteur:
                if secteur.upper() == 'PUBLIC':
                    where_conditions.append("(i.regime_gestion IS NOT NULL AND UPPER(i.regime_gestion) <> 'EPR')")
                elif secteur.upper() == 'PRIVE':
                    where_conditions.append("UPPER(i.regime_gestion) = 'EPR'")
            
            where_clause = " AND ".join(where_conditions)
            
            # Sélectionner la requête en fonction du type de régime
            if regime_type == 'regime_national':
                query = get_regime_national_query(where_clause)
                count_query = get_regime_national_count_query(where_clause)
            elif regime_type == 'regimes_proved':
                query = get_regimes_proved_query(where_clause)
                count_query = get_regimes_proved_count_query(where_clause)
            elif regime_type == 'milieu_proved':
                query = get_milieu_proved_query(where_clause)
                count_query = get_milieu_proved_count_query(where_clause)
            elif regime_type == 'public_proved':
                query = get_public_proved_query(where_clause)
                count_query = get_public_proved_count_query(where_clause)
            elif regime_type == 'milieu_public':
                query = get_milieu_public_query(where_clause)
                count_query = get_milieu_public_count_query(where_clause)
            else:
                query = get_normal_query(where_clause, page_size, offset)
                count_query = get_normal_count_query(where_clause)
            
            # Exécuter la requête de comptage pour le total
            with connection.cursor() as cursor:
                cursor.execute(count_query, params)
                total_count = cursor.fetchone()[0]
            
            # Exécuter la requête principale avec pagination
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                columns = [col[0] for col in cursor.description]
                results = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
            
            # Calculer les informations de pagination
            total_pages = (total_count + page_size - 1) // page_size if total_count > 0 else 1
            
            return JsonResponse({
                'success': True, 
                'data': results,
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total_count': total_count,
                    'total_pages': total_pages,
                    'has_previous': page > 1,
                    'has_next': page < total_pages,
                    'start_index': offset + 1,
                    'end_index': min(offset + page_size, total_count)
                }
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})

def export_excel(request):
    """Export Excel du tableau actuel"""
    try:
        regime_type = request.GET.get('regime_type', 'normal')
        filters = {
            'annee': request.GET.get('annee', ''),
            'type_enseignement': request.GET.get('type_enseignement', ''),
            'province': request.GET.get('province', ''),
            'milieu': request.GET.get('milieu', ''),
            'secteur': request.GET.get('secteur', '')
        }
        
        # Récupérer les données
        where_conditions = ["f.responded = 1"]
        params = []
        
        # Appliquer les mêmes filtres que dans get_table_data
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
        
        milieu = filters.get('milieu')
        if milieu:
            where_conditions.append("UPPER(i.milieu) = UPPER(%s)")
            params.append(milieu)
        
        secteur = filters.get('secteur')
        if secteur:
            if secteur.upper() == 'PUBLIC':
                where_conditions.append("(i.regime_gestion IS NOT NULL AND UPPER(i.regime_gestion) <> 'EPR')")
            elif secteur.upper() == 'PRIVE':
                where_conditions.append("UPPER(i.regime_gestion) = 'EPR'")
        
        where_clause = " AND ".join(where_conditions)
        
        # Sélectionner la requête
        if regime_type == 'regime_national':
            query = get_regime_national_query(where_clause)
            title = "Régime National"
        elif regime_type == 'regimes_proved':
            query = get_regimes_proved_query(where_clause)
            title = "Régimes par Province"
        elif regime_type == 'milieu_proved':
            query = get_milieu_proved_query(where_clause)
            title = "Milieu par Province"
        elif regime_type == 'public_proved':
            query = get_public_proved_query(where_clause)
            title = "Public par Province"
        elif regime_type == 'milieu_public':
            query = get_milieu_public_query(where_clause)
            title = "Milieu Public"
        else:
            query = get_normal_query(where_clause)
            title = "Liste des Établissements"
        
        # Exécuter la requête
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Créer le fichier Excel
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="annuaire_ecoles_{regime_type}_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.xls"'
        
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Annuaire')
        
        # Styles
        header_style = xlwt.easyxf('font: bold on; align: horiz center; pattern: pattern solid, fore_color light_green;')
        normal_style = xlwt.easyxf('align: horiz left;')
        number_style = xlwt.easyxf('align: horiz right;')
        
        # En-tête du document
        row_num = 0
        ws.write(row_num, 0, f"ANNUAIRE DES ÉCOLES - {title}", header_style)
        row_num += 1
        ws.write(row_num, 0, f"Généré le: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
        row_num += 2
        
        # En-têtes des colonnes
        for col_num, column_title in enumerate(columns):
            ws.write(row_num, col_num, column_title.replace('_', ' ').title(), header_style)
            ws.col(col_num).width = 4000  # Largeur des colonnes
        
        row_num += 1
        
        # Données
        for row in results:
            for col_num, column_title in enumerate(columns):
                value = row.get(column_title, '')
                if isinstance(value, (int, float)):
                    ws.write(row_num, col_num, value, number_style)
                else:
                    ws.write(row_num, col_num, str(value), normal_style)
            row_num += 1
        
        # Pied de page
        row_num += 1
        ws.write(row_num, 0, f"Total: {len(results)} enregistrements")
        
        wb.save(response)
        return response
        
    except Exception as e:
        return HttpResponse(f"Erreur lors de l'export Excel: {str(e)}")

def export_pdf(request):
    """Export PDF du tableau actuel"""
    try:
        regime_type = request.GET.get('regime_type', 'normal')
        filters = {
            'annee': request.GET.get('annee', ''),
            'type_enseignement': request.GET.get('type_enseignement', ''),
            'province': request.GET.get('province', ''),
            'milieu': request.GET.get('milieu', ''),
            'secteur': request.GET.get('secteur', '')
        }
        
        # Récupérer les données (même logique que export_excel)
        where_conditions = ["f.responded = 1"]
        params = []
        
        # Appliquer les filtres
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
        
        milieu = filters.get('milieu')
        if milieu:
            where_conditions.append("UPPER(i.milieu) = UPPER(%s)")
            params.append(milieu)
        
        secteur = filters.get('secteur')
        if secteur:
            if secteur.upper() == 'PUBLIC':
                where_conditions.append("(i.regime_gestion IS NOT NULL AND UPPER(i.regime_gestion) <> 'EPR')")
            elif secteur.upper() == 'PRIVE':
                where_conditions.append("UPPER(i.regime_gestion) = 'EPR'")
        
        where_clause = " AND ".join(where_conditions)
        
        # Sélectionner la requête
        if regime_type == 'regime_national':
            query = get_regime_national_query(where_clause)
            title = "Régime National"
        elif regime_type == 'regimes_proved':
            query = get_regimes_proved_query(where_clause)
            title = "Régimes par Province"
        elif regime_type == 'milieu_proved':
            query = get_milieu_proved_query(where_clause)
            title = "Milieu par Province"
        elif regime_type == 'public_proved':
            query = get_public_proved_query(where_clause)
            title = "Public par Province"
        elif regime_type == 'milieu_public':
            query = get_milieu_public_query(where_clause)
            title = "Milieu Public"
        else:
            query = get_normal_query(where_clause)
            title = "Liste des Établissements"
        
        # Exécuter la requête
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Créer le PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="annuaire_ecoles_{regime_type}_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.pdf"'
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        elements = []
        
        styles = getSampleStyleSheet()
        
        # Titre
        title_text = f"ANNUAIRE DES ÉCOLES - {title}"
        elements.append(Paragraph(title_text, styles['Title']))
        
        # Date de génération
        date_text = f"Généré le: {datetime.datetime.now().strftime('%d/%m/%Y à %H:%M')}"
        elements.append(Paragraph(date_text, styles['Normal']))
        
        # Filtres appliqués
        filters_text = "Filtres appliqués: "
        filters_list = []
        if filters['annee']:
            filters_list.append(f"Année: {filters['annee']}")
        if filters['type_enseignement']:
            filters_list.append(f"Type: {filters['type_enseignement']}")
        if filters['province']:
            filters_list.append(f"Province: {filters['province']}")
        if filters['milieu']:
            filters_list.append(f"Milieu: {filters['milieu']}")
        if filters['secteur']:
            filters_list.append(f"Secteur: {filters['secteur']}")
        
        if filters_list:
            filters_text += " | ".join(filters_list)
            elements.append(Paragraph(filters_text, styles['Normal']))
        
        elements.append(Paragraph(" ", styles['Normal']))  # Espace
        
        # Préparer les données pour le tableau
        if results:
            # En-têtes
            table_data = [[col.replace('_', ' ').title() for col in columns]]
            
            # Données
            for row in results:
                table_row = []
                for col in columns:
                    value = row.get(col, '')
                    table_row.append(str(value))
                table_data.append(table_row)
            
            # Créer le tableau
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(table)
            
            # Total
            elements.append(Paragraph(f"<br/>Total: {len(results)} enregistrements", styles['Normal']))
        else:
            elements.append(Paragraph("Aucune donnée à exporter", styles['Normal']))
        
        # Générer le PDF
        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
        
    except Exception as e:
        return HttpResponse(f"Erreur lors de l'export PDF: {str(e)}")

def export_csv(request):
    """Export CSV du tableau actuel"""
    try:
        regime_type = request.GET.get('regime_type', 'normal')
        filters = {
            'annee': request.GET.get('annee', ''),
            'type_enseignement': request.GET.get('type_enseignement', ''),
            'province': request.GET.get('province', ''),
            'milieu': request.GET.get('milieu', ''),
            'secteur': request.GET.get('secteur', '')
        }
        
        # Récupérer les données (même logique que export_excel)
        where_conditions = ["f.responded = 1"]
        params = []
        
        # Appliquer les filtres
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
        
        milieu = filters.get('milieu')
        if milieu:
            where_conditions.append("UPPER(i.milieu) = UPPER(%s)")
            params.append(milieu)
        
        secteur = filters.get('secteur')
        if secteur:
            if secteur.upper() == 'PUBLIC':
                where_conditions.append("(i.regime_gestion IS NOT NULL AND UPPER(i.regime_gestion) <> 'EPR')")
            elif secteur.upper() == 'PRIVE':
                where_conditions.append("UPPER(i.regime_gestion) = 'EPR'")
        
        where_clause = " AND ".join(where_conditions)
        
        # Sélectionner la requête
        if regime_type == 'regime_national':
            query = get_regime_national_query(where_clause)
            title = "Régime National"
        elif regime_type == 'regimes_proved':
            query = get_regimes_proved_query(where_clause)
            title = "Régimes par Province"
        elif regime_type == 'milieu_proved':
            query = get_milieu_proved_query(where_clause)
            title = "Milieu par Province"
        elif regime_type == 'public_proved':
            query = get_public_proved_query(where_clause)
            title = "Public par Province"
        elif regime_type == 'milieu_public':
            query = get_milieu_public_query(where_clause)
            title = "Milieu Public"
        else:
            query = get_normal_query(where_clause)
            title = "Liste des Établissements"
        
        # Exécuter la requête
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Créer le CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="annuaire_ecoles_{regime_type}_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.csv"'
        
        response.write(u'\ufeff'.encode('utf8'))  # BOM pour Excel
        writer = csv.writer(response)
        
        # En-tête
        writer.writerow([f"ANNUAIRE DES ÉCOLES - {title}"])
        writer.writerow([f"Généré le: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}"])
        writer.writerow([])
        
        # En-têtes des colonnes
        writer.writerow([col.replace('_', ' ').title() for col in columns])
        
        # Données
        for row in results:
            writer.writerow([str(row.get(col, '')) for col in columns])
        
        writer.writerow([])
        writer.writerow([f"Total: {len(results)} enregistrements"])
        
        return response
        
    except Exception as e:
        return HttpResponse(f"Erreur lors de l'export CSV: {str(e)}")

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

def get_normal_query(where_clause, page_size=10, offset=0):
    return f"""
    SELECT 
        f.id,
        f.idannee AS annee_scolaire,
        f.type AS type_enseignement,
        p.libelle AS province,
        CONCAT('Établissement ', f.id) AS nom_etablissement,
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
    LIMIT {page_size} OFFSET {offset};
    """

# Fonctions de comptage pour la pagination
def get_regime_national_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM identifications i
        INNER JOIN formulaires f ON f.identification_id = i.id AND {where_clause}
        GROUP BY i.secteur_enseignement, i.regime_gestion
    ) as subquery
    """

def get_regimes_proved_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        JOIN provinces p ON i.fk_province_id = p.id
        WHERE {where_clause}
        GROUP BY p.id, p.libelle, f.idannee, UPPER(f.type)
    ) as subquery
    """

def get_milieu_proved_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        JOIN provinces p ON i.fk_province_id = p.id
        WHERE {where_clause}
        GROUP BY p.id, p.libelle, f.idannee, UPPER(f.type)
    ) as subquery
    """

def get_public_proved_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        JOIN provinces p ON i.fk_province_id = p.id
        WHERE {where_clause}
          AND (i.regime_gestion IS NOT NULL AND UPPER(i.regime_gestion) <> 'EPR')
        GROUP BY f.idannee, UPPER(f.type), p.id, p.libelle
    ) as subquery
    """

def get_milieu_public_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        JOIN provinces p ON i.fk_province_id = p.id
        WHERE {where_clause}
          AND (i.regime_gestion IS NOT NULL AND UPPER(i.regime_gestion) <> 'EPR')
        GROUP BY f.idannee, UPPER(f.type), p.id, p.libelle
    ) as subquery
    """

def get_normal_count_query(where_clause):
    return f"""
    SELECT COUNT(*)
    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE {where_clause}
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

def get_milieux():
    """Récupère tous les milieux disponibles"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT UPPER(milieu) 
            FROM identifications 
            WHERE milieu IS NOT NULL AND milieu != '' 
            ORDER BY milieu
        """)
        return [row[0] for row in cursor.fetchall()]

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