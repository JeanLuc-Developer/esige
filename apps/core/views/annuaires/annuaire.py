from django.shortcuts import render


# ECOLES
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
            regime_type = data.get('regime_type', 'normal')
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
                data_formatter = format_regime_national_data
            elif regime_type == 'regimes_proved':
                query = get_regimes_proved_query(where_clause)
                count_query = get_regimes_proved_count_query(where_clause)
                data_formatter = format_regimes_proved_data
            elif regime_type == 'milieu_proved':
                query = get_milieu_proved_query(where_clause)
                count_query = get_milieu_proved_count_query(where_clause)
                data_formatter = format_milieu_proved_data
            elif regime_type == 'public_proved':
                query = get_public_proved_query(where_clause)
                count_query = get_public_proved_count_query(where_clause)
                data_formatter = format_public_proved_data
            elif regime_type == 'milieu_public':
                query = get_milieu_public_query(where_clause)
                count_query = get_milieu_public_count_query(where_clause)
                data_formatter = format_milieu_public_data
            else:
                query = get_normal_query(where_clause, page_size, offset)
                count_query = get_normal_count_query(where_clause)
                data_formatter = format_normal_data
            
            # Exécuter la requête de comptage pour le total
            with connection.cursor() as cursor:
                cursor.execute(count_query, params)
                total_count = cursor.fetchone()[0]
            
            # Exécuter la requête principale
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                columns = [col[0] for col in cursor.description]
                raw_results = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
            
            # Formater les données selon le type de tableau
            results = data_formatter(raw_results)
            
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

# Fonctions de formatage des données pour chaque type de tableau
def format_regime_national_data(raw_data):
    """Formater les données pour le tableau Régime National"""
    formatted_data = []
    
    # Regrouper par secteur et régime
    secteur_data = {}
    total_public = 0
    total_prive = 0
    
    for row in raw_data:
        secteur = row.get('secteur', 'Public')
        regime = row.get('regime_gestion', '')
        total_etablissements = row.get('total_etablissements', 0)
        
        if secteur not in secteur_data:
            secteur_data[secteur] = {}
        
        if regime not in secteur_data[secteur]:
            secteur_data[secteur][regime] = 0
        
        secteur_data[secteur][regime] += total_etablissements
        
        if regime != 'EPR':  # Public
            total_public += total_etablissements
        else:  # Privé
            total_prive += total_etablissements
    
    total_general = total_public + total_prive
    
    # Ajouter les données formatées selon la structure Excel
    for secteur, regimes in secteur_data.items():
        # Ajouter une ligne pour le secteur
        formatted_data.append({
            'type_ligne': 'secteur',
            'secteur': secteur,
            'regime': '',
            'total': ''
        })
        
        # Ajouter les régimes pour ce secteur
        for regime, total in regimes.items():
            formatted_data.append({
                'type_ligne': 'regime_detail',
                'secteur': '',
                'regime': regime,
                'total': total
            })
    
    # Ajouter les totaux
    formatted_data.append({
        'type_ligne': 'total_public',
        'secteur': 'Total Public',
        'regime': '',
        'total': total_public
    })
    
    formatted_data.append({
        'type_ligne': 'total_prive',
        'secteur': 'Prive',
        'regime': '',
        'total': total_prive
    })
    
    formatted_data.append({
        'type_ligne': 'total_general',
        'secteur': 'Total general',
        'regime': '',
        'total': total_general
    })
    
    return formatted_data

def format_regimes_proved_data(raw_data):
    """Formater les données pour le tableau Régimes par Province"""
    formatted_data = []
    
    # Regrouper par province pour éviter les doublons
    province_data = {}
    
    for row in raw_data:
        province_id = row.get('idProvince')
        province_name = row.get('province', '')
        
        if province_id not in province_data:
            province_data[province_id] = {
                'province': province_name,
                'ecc': 0, 'ecf': 0, 'eci': 0, 'eck': 0, 'ecp': 0, 
                'ecs': 0, 'enc': 0, 'epr': 0, 'nr': 0, 'autre': 0,
                'total_public': 0, 'prive': 0, 'total_general': 0
            }
        
        # Accumuler les données
        province_data[province_id]['ecc'] += row.get('ECC', 0)
        province_data[province_id]['ecf'] += row.get('ECF', 0)
        province_data[province_id]['eci'] += row.get('ECI', 0)
        province_data[province_id]['eck'] += row.get('ECK', 0)
        province_data[province_id]['ecp'] += row.get('ECP', 0)
        province_data[province_id]['ecs'] += row.get('ECS', 0)
        province_data[province_id]['enc'] += row.get('ENC', 0)
        province_data[province_id]['epr'] += row.get('EPR', 0)
        province_data[province_id]['nr'] += row.get('NR', 0)
        province_data[province_id]['autre'] += row.get('Autre', 0)
        province_data[province_id]['total_public'] += row.get('Total_Public', 0)
        province_data[province_id]['prive'] += row.get('Total_Prive', 0)
        province_data[province_id]['total_general'] += row.get('Total_General', 0)
    
    # Convertir en liste formatée
    for i, (province_id, data) in enumerate(province_data.items(), 1):
        formatted_data.append({
            'numero': i,
            'province': data['province'],
            'ecc': data['ecc'],
            'ecf': data['ecf'],
            'eci': data['eci'],
            'eck': data['eck'],
            'ecp': data['ecp'],
            'ecs': data['ecs'],
            'enc': data['enc'],
            'epr': data['epr'],
            'nr': data['nr'],
            'autre': data['autre'],
            'total_public': data['total_public'],
            'prive': data['prive'],
            'total_general': data['total_general']
        })
    
    # Ajouter la ligne de total général
    if formatted_data:
        totals = {
            'ecc': sum(row['ecc'] for row in formatted_data),
            'ecf': sum(row['ecf'] for row in formatted_data),
            'eci': sum(row['eci'] for row in formatted_data),
            'eck': sum(row['eck'] for row in formatted_data),
            'ecp': sum(row['ecp'] for row in formatted_data),
            'ecs': sum(row['ecs'] for row in formatted_data),
            'enc': sum(row['enc'] for row in formatted_data),
            'epr': sum(row['epr'] for row in formatted_data),
            'nr': sum(row['nr'] for row in formatted_data),
            'autre': sum(row['autre'] for row in formatted_data),
            'total_public': sum(row['total_public'] for row in formatted_data),
            'prive': sum(row['prive'] for row in formatted_data),
            'total_general': sum(row['total_general'] for row in formatted_data)
        }
        
        formatted_data.append({
            'type_ligne': 'total_general',
            'numero': '',
            'province': 'Total general',
            'ecc': totals['ecc'],
            'ecf': totals['ecf'],
            'eci': totals['eci'],
            'eck': totals['eck'],
            'ecp': totals['ecp'],
            'ecs': totals['ecs'],
            'enc': totals['enc'],
            'epr': totals['epr'],
            'nr': totals['nr'],
            'autre': totals['autre'],
            'total_public': totals['total_public'],
            'prive': totals['prive'],
            'total_general': totals['total_general']
        })
    
    return formatted_data

def format_milieu_proved_data(raw_data):
    """Formater les données pour le tableau Milieu par Province"""
    formatted_data = []
    
    # Regrouper par province pour éviter les doublons
    province_data = {}
    
    for row in raw_data:
        province_id = row.get('idProvince')
        province_name = row.get('province', '')
        
        if province_id not in province_data:
            province_data[province_id] = {
                'province': province_name,
                'urbain': 0, 'rural': 0, 'total_general': 0
            }
        
        # Accumuler les données
        province_data[province_id]['urbain'] += row.get('Urbain', 0)
        province_data[province_id]['rural'] += row.get('Rural', 0)
        province_data[province_id]['total_general'] += row.get('Total_General', 0)
    
    # Convertir en liste formatée
    for i, (province_id, data) in enumerate(province_data.items(), 1):
        formatted_data.append({
            'numero': i,
            'province': data['province'],
            'urbain': data['urbain'],
            'rural': data['rural'],
            'total_general': data['total_general']
        })
    
    # Ajouter la ligne de total général
    if formatted_data:
        totals = {
            'urbain': sum(row['urbain'] for row in formatted_data),
            'rural': sum(row['rural'] for row in formatted_data),
            'total_general': sum(row['total_general'] for row in formatted_data)
        }
        
        formatted_data.append({
            'type_ligne': 'total_general',
            'numero': '',
            'province': 'Total general',
            'urbain': totals['urbain'],
            'rural': totals['rural'],
            'total_general': totals['total_general']
        })
    
    return formatted_data

def format_public_proved_data(raw_data):
    """Formater les données pour le tableau Public par Province"""
    formatted_data = []
    
    # Regrouper par province pour éviter les doublons
    province_data = {}
    
    for row in raw_data:
        province_id = row.get('idProvince')
        province_name = row.get('province', '')
        
        if province_id not in province_data:
            province_data[province_id] = {
                'province': province_name,
                'total': 0
            }
        
        # Accumuler les données
        province_data[province_id]['total'] += row.get('nombre_ecoles_public', 0)
    
    # Convertir en liste formatée
    for i, (province_id, data) in enumerate(province_data.items(), 1):
        formatted_data.append({
            'numero': i,
            'province': data['province'],
            'total': data['total']
        })
    
    # Ajouter la ligne de total général
    if formatted_data:
        total_general = sum(row['total'] for row in formatted_data)
        formatted_data.append({
            'type_ligne': 'total_general',
            'numero': '',
            'province': 'Total general',
            'total': total_general
        })
    
    return formatted_data

def format_milieu_public_data(raw_data):
    """Formater les données pour le tableau Milieu Public"""
    formatted_data = []
    
    # Regrouper par province pour éviter les doublons
    province_data = {}
    
    for row in raw_data:
        province_id = row.get('idProvince')
        province_name = row.get('province', '')
        
        if province_id not in province_data:
            province_data[province_id] = {
                'province': province_name,
                'urbain': 0, 'rural': 0, 'total_general': 0
            }
        
        # Accumuler les données
        province_data[province_id]['urbain'] += row.get('Urbain', 0)
        province_data[province_id]['rural'] += row.get('Rural', 0)
        province_data[province_id]['total_general'] += row.get('Total_Public', 0)
    
    # Convertir en liste formatée
    for i, (province_id, data) in enumerate(province_data.items(), 1):
        formatted_data.append({
            'numero': i,
            'province': data['province'],
            'urbain': data['urbain'],
            'rural': data['rural'],
            'total_general': data['total_general']
        })
    
    # Ajouter la ligne de total général
    if formatted_data:
        totals = {
            'urbain': sum(row['urbain'] for row in formatted_data),
            'rural': sum(row['rural'] for row in formatted_data),
            'total_general': sum(row['total_general'] for row in formatted_data)
        }
        
        formatted_data.append({
            'type_ligne': 'total_general',
            'numero': '',
            'province': 'Total general',
            'urbain': totals['urbain'],
            'rural': totals['rural'],
            'total_general': totals['total_general']
        })
    
    return formatted_data

def format_normal_data(raw_data):
    """Formater les données pour le tableau normal"""
    formatted_data = []
    
    for i, row in enumerate(raw_data, 1):
        formatted_data.append({
            'numero': i,
            'nom': row.get('nom_etablissement', ''),
            'annee_scolaire': row.get('annee_scolaire', ''),
            'province': row.get('province', ''),
            'adresse': row.get('adresse', ''),
            'chef_etablissement': row.get('chef_etablissement', ''),
            'telephone': row.get('telephone', ''),
            'statut': row.get('statut', ''),
            'created_at': row.get('created_at', '')
        })
    
    return formatted_data

# FONCTIONS D'EXPORT CORRIGÉES
def export_excel(request):
    """Export Excel du tableau actuel - VERSION CORRIGÉE"""
    try:
        regime_type = request.GET.get('regime_type', 'normal')
        filters = {
            'annee': request.GET.get('annee', ''),
            'type_enseignement': request.GET.get('type_enseignement', ''),
            'province': request.GET.get('province', ''),
            'milieu': request.GET.get('milieu', ''),
            'secteur': request.GET.get('secteur', '')
        }
        
        print(f"Export Excel - Régime: {regime_type}, Filtres: {filters}")
        
        # Récupérer les données AVEC LA MÊME MÉTHODE QUE get_table_data
        data = get_export_data_direct(regime_type, filters)
        
        # Définir les colonnes selon le type de régime
        columns_config = {
            'regime_national': ['Secteur', 'Regime de gestion', 'Total'],
            'regimes_proved': ['N°', 'Province', 'ECC', 'ECF', 'ECI', 'ECK', 'ECP', 'ECS', 'ENC', 'EPR', 'NR', 'Autre', 'Total Public', 'Prive', 'Total general'],
            'milieu_proved': ['N°', 'Province', 'Urbain', 'Rural', 'Total general'],
            'public_proved': ['N°', 'Province', 'Total'],
            'milieu_public': ['N°', 'Province', 'Urbain', 'Rural', 'Total general'],
            'normal': ['N°', 'Nom', 'Année Scolaire', 'Province', 'Adresse', 'Chef établissement', 'Téléphone', 'Statut', 'Créé le']
        }
        
        columns = columns_config.get(regime_type, columns_config['normal'])
        
        # Créer le fichier Excel
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="annuaire_ecoles_{regime_type}_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.xls"'
        
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Annuaire')
        
        # Styles
        header_style = xlwt.easyxf('font: bold on; align: horiz center; pattern: pattern solid, fore_color light_green;')
        total_style = xlwt.easyxf('font: bold on; pattern: pattern solid, fore_color gray25;')
        normal_style = xlwt.easyxf('align: horiz left;')
        number_style = xlwt.easyxf('align: horiz right;')
        secteur_style = xlwt.easyxf('font: bold on; align: horiz left; pattern: pattern solid, fore_color light_blue;')
        
        # En-tête du document
        row_num = 0
        ws.write(row_num, 0, f"ANNUAIRE DES ÉCOLES - {get_regime_title(regime_type)}", header_style)
        row_num += 2
        
        # Date de génération
        ws.write(row_num, 0, f"Généré le: {datetime.datetime.now().strftime('%d/%m/%Y à %H:%M')}")
        row_num += 1
        
        # Filtres appliqués
        filters_text = "Filtres appliqués: "
        filters_list = []
        if filters['annee']:
            filters_list.append(f"Année: {filters['annee']}")
        if filters['type_enseignement']:
            filters_list.append(f"Type: {filters['type_enseignement']}")
        if filters['province']:
            province_name = get_province_name(filters['province'])
            filters_list.append(f"Province: {province_name}")
        if filters['milieu']:
            filters_list.append(f"Milieu: {filters['milieu']}")
        if filters['secteur']:
            filters_list.append(f"Secteur: {filters['secteur']}")
        
        if filters_list:
            ws.write(row_num, 0, filters_text + " | ".join(filters_list))
            row_num += 1
        
        row_num += 1
        
        # En-têtes des colonnes
        for col_num, column_title in enumerate(columns):
            ws.write(row_num, col_num, column_title, header_style)
            ws.col(col_num).width = 4000
        
        row_num += 1
        
        # Données
        print(f"Nombre de données à exporter: {len(data)}")
        
        for row in data:
            for col_num, column_title in enumerate(columns):
                value = row.get(column_title, '') if isinstance(row, dict) else ''
                
                style = normal_style
                
                # Vérifier si c'est un nombre
                if isinstance(value, (int, float)) or (isinstance(value, str) and value.replace('.', '').isdigit()):
                    style = number_style
                
                # Appliquer les styles selon le type de ligne
                if isinstance(row, dict) and row.get('type_ligne') == 'secteur':
                    style = secteur_style
                elif isinstance(row, dict) and row.get('type_ligne') in ['total_public', 'total_prive', 'total_general']:
                    style = total_style
                
                ws.write(row_num, col_num, str(value), style)
            row_num += 1
        
        # Total des enregistrements
        row_num += 1
        ws.write(row_num, 0, f"Total: {len(data)} enregistrements", total_style)
        
        wb.save(response)
        return response
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Erreur export Excel: {str(e)}")
        print(f"Détails: {error_details}")
        return HttpResponse(f"Erreur lors de l'export Excel: {str(e)}")


def export_pdf(request):
    """Export PDF du tableau actuel - VERSION CORRIGÉE"""
    try:
        regime_type = request.GET.get('regime_type', 'normal')
        filters = {
            'annee': request.GET.get('annee', ''),
            'type_enseignement': request.GET.get('type_enseignement', ''),
            'province': request.GET.get('province', ''),
            'milieu': request.GET.get('milieu', ''),
            'secteur': request.GET.get('secteur', '')
        }
        
        print(f"Export PDF - Régime: {regime_type}, Filtres: {filters}")
        
        # Récupérer les données
        data = get_export_data_direct(regime_type, filters)
        
        # Définir les colonnes
        columns_config = {
            'regime_national': ['Secteur', 'Regime de gestion', 'Total'],
            'regimes_proved': ['N°', 'Province', 'ECC', 'ECF', 'ECI', 'ECK', 'ECP', 'ECS', 'ENC', 'EPR', 'NR', 'Autre', 'Total Public', 'Prive', 'Total general'],
            'milieu_proved': ['N°', 'Province', 'Urbain', 'Rural', 'Total general'],
            'public_proved': ['N°', 'Province', 'Total'],
            'milieu_public': ['N°', 'Province', 'Urbain', 'Rural', 'Total general'],
            'normal': ['N°', 'Nom', 'Année Scolaire', 'Province', 'Adresse', 'Chef établissement', 'Téléphone', 'Statut', 'Créé le']
        }
        
        columns = columns_config.get(regime_type, columns_config['normal'])
        
        # Créer le PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="annuaire_ecoles_{regime_type}_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.pdf"'
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        elements = []
        
        styles = getSampleStyleSheet()
        
        # Titre
        title_text = f"ANNUAIRE DES ÉCOLES - {get_regime_title(regime_type)}"
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
            province_name = get_province_name(filters['province'])
            filters_list.append(f"Province: {province_name}")
        if filters['milieu']:
            filters_list.append(f"Milieu: {filters['milieu']}")
        if filters['secteur']:
            filters_list.append(f"Secteur: {filters['secteur']}")
        
        if filters_list:
            filters_text += " | ".join(filters_list)
            elements.append(Paragraph(filters_text, styles['Normal']))
        
        elements.append(Paragraph(" ", styles['Normal']))
        
        # Préparer les données pour le tableau
        print(f"Nombre de données PDF: {len(data)}")
        
        if data:
            # En-têtes
            table_data = [columns]
            
            # Données
            for row in data:
                table_row = []
                for col in columns:
                    if isinstance(row, dict):
                        value = row.get(col, '')
                    else:
                        value = ''
                    table_row.append(str(value))
                table_data.append(table_row)
            
            # Créer le tableau
            table = Table(table_data, repeatRows=1)
            
            # Appliquer les styles
            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4b6cb7')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ])
            
            table.setStyle(table_style)
            elements.append(table)
            
            # Ajouter le nombre total d'enregistrements
            elements.append(Paragraph(f"<br/><b>Total: {len(data)} enregistrements</b>", styles['Normal']))
        else:
            elements.append(Paragraph("Aucune donnée à exporter", styles['Normal']))
        
        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Erreur export PDF: {str(e)}")
        print(f"Détails: {error_details}")
        return HttpResponse(f"Erreur lors de l'export PDF: {str(e)}")


def export_csv(request):
    """Export CSV du tableau actuel - VERSION CORRIGÉE"""
    try:
        regime_type = request.GET.get('regime_type', 'normal')
        filters = {
            'annee': request.GET.get('annee', ''),
            'type_enseignement': request.GET.get('type_enseignement', ''),
            'province': request.GET.get('province', ''),
            'milieu': request.GET.get('milieu', ''),
            'secteur': request.GET.get('secteur', '')
        }
        
        print(f"Export CSV - Régime: {regime_type}, Filtres: {filters}")
        
        # Récupérer les données
        data = get_export_data_direct(regime_type, filters)
        
        # Définir les colonnes
        columns_config = {
            'regime_national': ['Secteur', 'Regime de gestion', 'Total'],
            'regimes_proved': ['N°', 'Province', 'ECC', 'ECF', 'ECI', 'ECK', 'ECP', 'ECS', 'ENC', 'EPR', 'NR', 'Autre', 'Total Public', 'Prive', 'Total general'],
            'milieu_proved': ['N°', 'Province', 'Urbain', 'Rural', 'Total general'],
            'public_proved': ['N°', 'Province', 'Total'],
            'milieu_public': ['N°', 'Province', 'Urbain', 'Rural', 'Total general'],
            'normal': ['N°', 'Nom', 'Année Scolaire', 'Province', 'Adresse', 'Chef établissement', 'Téléphone', 'Statut', 'Créé le']
        }
        
        columns = columns_config.get(regime_type, columns_config['normal'])
        
        # Créer le CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="annuaire_ecoles_{regime_type}_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.csv"'
        
        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response, delimiter=';')
        
        # En-tête
        writer.writerow([f"ANNUAIRE DES ÉCOLES - {get_regime_title(regime_type)}"])
        writer.writerow([f"Généré le: {datetime.datetime.now().strftime('%d/%m/%Y à %H:%M')}"])
        
        # Filtres appliqués
        filters_list = []
        if filters['annee']:
            filters_list.append(f"Année: {filters['annee']}")
        if filters['type_enseignement']:
            filters_list.append(f"Type: {filters['type_enseignement']}")
        if filters['province']:
            province_name = get_province_name(filters['province'])
            filters_list.append(f"Province: {province_name}")
        if filters['milieu']:
            filters_list.append(f"Milieu: {filters['milieu']}")
        if filters['secteur']:
            filters_list.append(f"Secteur: {filters['secteur']}")
        
        if filters_list:
            writer.writerow(["Filtres appliqués: " + " | ".join(filters_list)])
        
        writer.writerow([])
        
        # En-têtes des colonnes
        writer.writerow(columns)
        
        # Données
        print(f"Nombre de données CSV: {len(data)}")
        
        for row in data:
            row_data = []
            for col in columns:
                if isinstance(row, dict):
                    value = row.get(col, '')
                else:
                    value = ''
                row_data.append(str(value))
            writer.writerow(row_data)
        
        writer.writerow([])
        writer.writerow([f"Total: {len(data)} enregistrements"])
        
        return response
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Erreur export CSV: {str(e)}")
        print(f"Détails: {error_details}")
        return HttpResponse(f"Erreur lors de l'export CSV: {str(e)}")

def get_export_data_direct(regime_type, filters):
    """Récupère directement les données pour l'export - SIMPLIFIÉE"""
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
    query_functions = {
        'regime_national': get_regime_national_query,
        'regimes_proved': get_regimes_proved_query,
        'milieu_proved': get_milieu_proved_query,
        'public_proved': get_public_proved_query,
        'milieu_public': get_milieu_public_query,
    }
    
    query_func = query_functions.get(regime_type, get_normal_query_export)
    query = query_func(where_clause)
    
    print(f"Query: {query}")
    print(f"Params: {params}")
    
    # Exécuter la requête
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    print(f"Résultats bruts: {len(results)}")
    
    # Formater les données
    formatter_functions = {
        'regime_national': format_regime_national_data,
        'regimes_proved': format_regimes_proved_data,
        'milieu_proved': format_milieu_proved_data,
        'public_proved': format_public_proved_data,
        'milieu_public': format_milieu_public_data,
    }
    
    formatter_func = formatter_functions.get(regime_type, format_normal_data)
    formatted_data = formatter_func(results)
    
    print(f"Données formatées: {len(formatted_data)}")
    
    return formatted_data

def get_normal_query_export(where_clause):
    """Requête pour l'export du tableau normal"""
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
    LIMIT 10000;
    """

def get_province_name(province_id):
    """Récupère le nom d'une province par son ID"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT libelle FROM provinces WHERE id = %s", [province_id])
            result = cursor.fetchone()
            return result[0] if result else "Toutes provinces"
    except:
        return "Toutes provinces"

def get_regime_title(regime_type):
    """Retourne le titre selon le type de régime"""
    titles = {
        'regime_national': 'Régime National',
        'regimes_proved': 'Régime par Province',
        'milieu_proved': 'Milieu par Province',
        'public_proved': 'Public par Province',
        'milieu_public': 'Milieu Public',
        'normal': 'Liste des Établissements'
    }
    return titles.get(regime_type, 'Annuaires')

# FONCTIONS DE REQUÊTES SQL
def get_regime_national_query(where_clause):
    return f"""
    SELECT 
        CASE 
            WHEN i.regime_gestion = 'EPR' THEN 'Prive'
            ELSE 'Public'
        END AS secteur,
        COALESCE(i.regime_gestion, 'NR') AS regime_gestion,
        COUNT(*) AS total_etablissements
    FROM identifications i
    INNER JOIN formulaires f 
        ON f.identification_id = i.id 
        AND {where_clause}
    GROUP BY 
        CASE 
            WHEN i.regime_gestion = 'EPR' THEN 'Prive'
            ELSE 'Public'
        END,
        COALESCE(i.regime_gestion, 'NR')
    ORDER BY secteur, regime_gestion;
    """

def get_regimes_proved_query(where_clause):
    return f"""
    SELECT 
        p.id AS idProvince,
        p.libelle AS province,
        
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
        SUM(CASE WHEN i.regime_gestion NOT IN ('ECC', 'ECF', 'ECI', 'ECK', 'ECP', 'ECS', 'ENC', 'EPR') AND i.regime_gestion IS NOT NULL THEN 1 ELSE 0 END) AS Autre,

        -- Totaux
        SUM(CASE WHEN i.regime_gestion <> 'EPR' THEN 1 ELSE 0 END) AS Total_Public,
        SUM(CASE WHEN i.regime_gestion = 'EPR' THEN 1 ELSE 0 END) AS Total_Prive,
        COUNT(f.id) AS Total_General

    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE {where_clause}
    GROUP BY p.id, p.libelle
    ORDER BY p.libelle;
    """

def get_milieu_proved_query(where_clause):
    return f"""
    SELECT 
        p.id AS idProvince,
        p.libelle AS province,
        SUM(CASE WHEN UPPER(i.milieu) = 'URBAIN' THEN 1 ELSE 0 END) AS Urbain,
        SUM(CASE WHEN UPPER(i.milieu) = 'RURAL' THEN 1 ELSE 0 END) AS Rural,
        SUM(CASE WHEN i.milieu IS NULL OR i.milieu = '' THEN 1 ELSE 0 END) AS NR,
        COUNT(f.id) AS Total_General
    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE {where_clause}
    GROUP BY p.id, p.libelle
    ORDER BY p.libelle;
    """

def get_public_proved_query(where_clause):
    return f"""
    SELECT 
        p.id AS idProvince,
        p.libelle AS province,
        COUNT(f.id) AS nombre_ecoles_public
    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE {where_clause}
      AND (i.regime_gestion IS NOT NULL AND UPPER(i.regime_gestion) <> 'EPR')
    GROUP BY p.id, p.libelle
    ORDER BY p.libelle;
    """

def get_milieu_public_query(where_clause):
    return f"""
    SELECT 
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
    GROUP BY p.id, p.libelle
    ORDER BY p.libelle;
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

# FONCTIONS DE COMPTAGE
def get_regime_national_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM identifications i
        INNER JOIN formulaires f ON f.identification_id = i.id AND {where_clause}
        GROUP BY 
            CASE 
                WHEN i.regime_gestion = 'EPR' THEN 'Prive'
                ELSE 'Public'
            END,
            COALESCE(i.regime_gestion, 'NR')
    ) as subquery
    """

def get_regimes_proved_count_query(where_clause):
    return f"""
    SELECT COUNT(DISTINCT p.id)
    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE {where_clause}
    """

def get_milieu_proved_count_query(where_clause):
    return f"""
    SELECT COUNT(DISTINCT p.id)
    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE {where_clause}
    """

def get_public_proved_count_query(where_clause):
    return f"""
    SELECT COUNT(DISTINCT p.id)
    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE {where_clause}
      AND (i.regime_gestion IS NOT NULL AND UPPER(i.regime_gestion) <> 'EPR')
    """

def get_milieu_public_count_query(where_clause):
    return f"""
    SELECT COUNT(DISTINCT p.id)
    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE {where_clause}
      AND (i.regime_gestion IS NOT NULL AND UPPER(i.regime_gestion) <> 'EPR')
    """

def get_normal_count_query(where_clause):
    return f"""
    SELECT COUNT(*)
    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE {where_clause}
    """

# FONCTIONS UTILITAIRES POUR LES FILTRES
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
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT UPPER(milieu) 
            FROM identifications 
            WHERE milieu IS NOT NULL AND milieu != '' 
            ORDER BY milieu
        """)
        return [row[0] for row in cursor.fetchall()]











#CLASSES
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

def salles_organisees(request):
    """Vue principale pour les salles organisées"""
    context = {
        'annees_scolaires': get_annees_scolaires(),
        'provinces': get_provinces(),
        'types_enseignement': get_types_enseignement(),
        'milieux': get_milieux(),
    }
    return render(request, 'annuaires/salles_organisees.html', context)

@csrf_exempt
def get_salles_data(request):
    """Endpoint AJAX pour récupérer les données des salles organisées avec pagination"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rapport_type = data.get('rapport_type', 'secteur_regime')
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
                
            # Filtre type d'enseignement
            type_enseignement = filters.get('type_enseignement')
            if type_enseignement:
                where_conditions.append("UPPER(f.type) = UPPER(%s)")
                params.append(type_enseignement)
            else:
                # Par défaut, on prend ST1 comme dans vos requêtes
                where_conditions.append("UPPER(f.type) = 'ST1'")
                
            # Filtre province
            province = filters.get('province')
            if province:
                where_conditions.append("p.id = %s")
                params.append(province)
            
            # Filtre milieu
            milieu = filters.get('milieu')
            if milieu:
                where_conditions.append("UPPER(i.milieu) = UPPER(%s)")
                params.append(milieu)
            
            # Filtre secteur
            secteur = filters.get('secteur')
            if secteur:
                if secteur.upper() == 'PUBLIC':
                    where_conditions.append("(i.regime_gestion IS NOT NULL AND UPPER(i.regime_gestion) <> 'EPR')")
                elif secteur.upper() == 'PRIVE':
                    where_conditions.append("UPPER(i.regime_gestion) = 'EPR'")
            
            where_clause = " AND ".join(where_conditions)
            
            # Sélectionner la requête en fonction du type de rapport
            if rapport_type == 'secteur_regime':
                query = get_secteur_regime_query(where_clause, page_size, offset)
                count_query = get_secteur_regime_count_query(where_clause)
            elif rapport_type == 'province':
                query = get_province_query(where_clause, page_size, offset)
                count_query = get_province_count_query(where_clause)
            elif rapport_type == 'province_detail':
                query = get_province_detail_query(where_clause, page_size, offset)
                count_query = get_province_detail_count_query(where_clause)
            else:
                return JsonResponse({'success': False, 'error': 'Type de rapport non valide'})
            
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

def export_salles_excel(request):
    """Export Excel des salles organisées"""
    try:
        rapport_type = request.GET.get('rapport_type', 'secteur_regime')
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
        
        # Appliquer les filtres
        annee = filters.get('annee')
        if annee:
            where_conditions.append("f.idannee = %s")
            params.append(annee)
            
        type_enseignement = filters.get('type_enseignement')
        if type_enseignement:
            where_conditions.append("UPPER(f.type) = UPPER(%s)")
            params.append(type_enseignement)
        else:
            where_conditions.append("UPPER(f.type) = 'ST1'")
            
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
        if rapport_type == 'secteur_regime':
            query = get_secteur_regime_query(where_clause)
            title = "Salles Organisées par Secteur et Régime"
        elif rapport_type == 'province':
            query = get_province_query(where_clause)
            title = "Salles Organisées par Province"
        elif rapport_type == 'province_detail':
            query = get_province_detail_query(where_clause)
            title = "Salles Organisées par Province - Détail"
        else:
            query = get_secteur_regime_query(where_clause)
            title = "Salles Organisées"
        
        # Exécuter la requête
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Créer le fichier Excel
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="salles_organisees_{rapport_type}_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.xls"'
        
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Salles Organisées')
        
        # Styles
        header_style = xlwt.easyxf('font: bold on; align: horiz center; pattern: pattern solid, fore_color light_blue;')
        normal_style = xlwt.easyxf('align: horiz left;')
        number_style = xlwt.easyxf('align: horiz right;')
        total_style = xlwt.easyxf('font: bold on; align: horiz right; pattern: pattern solid, fore_color light_green;')
        
        # En-tête du document
        row_num = 0
        ws.write(row_num, 0, f"SALLES ORGANISÉES - {title}", header_style)
        row_num += 1
        ws.write(row_num, 0, f"Généré le: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
        row_num += 2
        
        # En-têtes des colonnes
        for col_num, column_title in enumerate(columns):
            ws.write(row_num, col_num, column_title.replace('_', ' ').title(), header_style)
            ws.col(col_num).width = 4000
        
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
        
        # Calculer les totaux
        if results:
            total_1ere = sum(row.get('nb_salles_organisees_1ere', 0) for row in results)
            total_2eme = sum(row.get('nb_salles_organisees_2eme', 0) for row in results)
            total_3eme = sum(row.get('nb_salles_organisees_3eme', 0) for row in results)
            total_general = sum(row.get('Total', 0) for row in results)
            
            row_num += 1
            ws.write(row_num, 0, "TOTAUX", total_style)
            ws.write(row_num, columns.index('nb_salles_organisees_1ere'), total_1ere, total_style)
            ws.write(row_num, columns.index('nb_salles_organisees_2eme'), total_2eme, total_style)
            ws.write(row_num, columns.index('nb_salles_organisees_3eme'), total_3eme, total_style)
            ws.write(row_num, columns.index('Total'), total_general, total_style)
        
        row_num += 2
        ws.write(row_num, 0, f"Total: {len(results)} enregistrements")
        
        wb.save(response)
        return response
        
    except Exception as e:
        return HttpResponse(f"Erreur lors de l'export Excel: {str(e)}")

def export_salles_pdf(request):
    """Export PDF des salles organisées"""
    try:
        rapport_type = request.GET.get('rapport_type', 'secteur_regime')
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
        
        # Appliquer les filtres
        annee = filters.get('annee')
        if annee:
            where_conditions.append("f.idannee = %s")
            params.append(annee)
            
        type_enseignement = filters.get('type_enseignement')
        if type_enseignement:
            where_conditions.append("UPPER(f.type) = UPPER(%s)")
            params.append(type_enseignement)
        else:
            where_conditions.append("UPPER(f.type) = 'ST1'")
            
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
        if rapport_type == 'secteur_regime':
            query = get_secteur_regime_query(where_clause)
            title = "Salles Organisées par Secteur et Régime"
        elif rapport_type == 'province':
            query = get_province_query(where_clause)
            title = "Salles Organisées par Province"
        elif rapport_type == 'province_detail':
            query = get_province_detail_query(where_clause)
            title = "Salles Organisées par Province - Détail"
        else:
            query = get_secteur_regime_query(where_clause)
            title = "Salles Organisées"
        
        # Exécuter la requête
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Créer le PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="salles_organisees_{rapport_type}_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.pdf"'
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        elements = []
        
        styles = getSampleStyleSheet()
        
        # Titre
        title_text = f"SALLES ORGANISÉES - {title}"
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
            
            # Ajouter les totaux
            if results:
                total_row = ['TOTAUX'] + [''] * (len(columns) - 4)
                total_1ere = sum(row.get('nb_salles_organisees_1ere', 0) for row in results)
                total_2eme = sum(row.get('nb_salles_organisees_2eme', 0) for row in results)
                total_3eme = sum(row.get('nb_salles_organisees_3eme', 0) for row in results)
                total_general = sum(row.get('Total', 0) for row in results)
                
                # Trouver les indices des colonnes de totaux
                col_names = [col.replace('_', ' ').title() for col in columns]
                if 'Nb Salles Organisees 1ere' in col_names:
                    idx = col_names.index('Nb Salles Organisees 1ere')
                    total_row[idx] = str(total_1ere)
                if 'Nb Salles Organisees 2eme' in col_names:
                    idx = col_names.index('Nb Salles Organisees 2eme')
                    total_row[idx] = str(total_2eme)
                if 'Nb Salles Organisees 3eme' in col_names:
                    idx = col_names.index('Nb Salles Organisees 3eme')
                    total_row[idx] = str(total_3eme)
                if 'Total' in col_names:
                    idx = col_names.index('Total')
                    total_row[idx] = str(total_general)
                
                table_data.append(total_row)
            
            # Créer le tableau
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
                ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -2), 8),
                ('BACKGROUND', (0, -1), (-1, -1), colors.lightgreen),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
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

def export_salles_csv(request):
    """Export CSV des salles organisées"""
    try:
        rapport_type = request.GET.get('rapport_type', 'secteur_regime')
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
        
        # Appliquer les filtres
        annee = filters.get('annee')
        if annee:
            where_conditions.append("f.idannee = %s")
            params.append(annee)
            
        type_enseignement = filters.get('type_enseignement')
        if type_enseignement:
            where_conditions.append("UPPER(f.type) = UPPER(%s)")
            params.append(type_enseignement)
        else:
            where_conditions.append("UPPER(f.type) = 'ST1'")
            
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
        if rapport_type == 'secteur_regime':
            query = get_secteur_regime_query(where_clause)
            title = "Salles Organisées par Secteur et Régime"
        elif rapport_type == 'province':
            query = get_province_query(where_clause)
            title = "Salles Organisées par Province"
        elif rapport_type == 'province_detail':
            query = get_province_detail_query(where_clause)
            title = "Salles Organisées par Province - Détail"
        else:
            query = get_secteur_regime_query(where_clause)
            title = "Salles Organisées"
        
        # Exécuter la requête
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Créer le CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="salles_organisees_{rapport_type}_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.csv"'
        
        response.write(u'\ufeff'.encode('utf8'))  # BOM pour Excel
        writer = csv.writer(response)
        
        # En-tête
        writer.writerow([f"SALLES ORGANISÉES - {title}"])
        writer.writerow([f"Généré le: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}"])
        writer.writerow([])
        
        # En-têtes des colonnes
        writer.writerow([col.replace('_', ' ').title() for col in columns])
        
        # Données
        for row in results:
            writer.writerow([str(row.get(col, '')) for col in columns])
        
        # Ajouter les totaux
        if results:
            total_1ere = sum(row.get('nb_salles_organisees_1ere', 0) for row in results)
            total_2eme = sum(row.get('nb_salles_organisees_2eme', 0) for row in results)
            total_3eme = sum(row.get('nb_salles_organisees_3eme', 0) for row in results)
            total_general = sum(row.get('Total', 0) for row in results)
            
            writer.writerow([])
            writer.writerow(['TOTAUX', '', '', '', total_1ere, total_2eme, total_3eme, total_general])
        
        writer.writerow([])
        writer.writerow([f"Total: {len(results)} enregistrements"])
        
        return response
        
    except Exception as e:
        return HttpResponse(f"Erreur lors de l'export CSV: {str(e)}")

# Fonctions pour les différentes requêtes (adaptées de vos requêtes)
def get_secteur_regime_query(where_clause, page_size=None, offset=0):
    base_query = f"""
    SELECT 
        f.idannee,
        UPPER(f.type) AS type,
        i.secteur_enseignement AS secteur,
        COALESCE(i.regime_gestion, 'NR') AS regime_gestion,
        SUM(COALESCE(c.nb_salles_organisees_1ere, 0)) AS nb_salles_organisees_1ere,
        SUM(COALESCE(c.nb_salles_organisees_2eme, 0)) AS nb_salles_organisees_2eme,
        SUM(COALESCE(c.nb_salles_organisees_3eme, 0)) AS nb_salles_organisees_3eme,
        SUM(
            COALESCE(c.nb_salles_organisees_1ere, 0) +
            COALESCE(c.nb_salles_organisees_2eme, 0) +
            COALESCE(c.nb_salles_organisees_3eme, 0)
        ) AS Total
    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    LEFT JOIN st1_infrastructure c ON f.id = c.form_st_id
    WHERE {where_clause}
    GROUP BY 
        f.idannee, 
        UPPER(f.type),
        i.secteur_enseignement, 
        i.regime_gestion
    ORDER BY 
        f.idannee, 
        UPPER(f.type),
        i.secteur_enseignement, 
        i.regime_gestion
    """
    
    if page_size is not None:
        base_query += f" LIMIT {page_size} OFFSET {offset}"
    
    return base_query

def get_province_query(where_clause, page_size=None, offset=0):
    base_query = f"""
    SELECT 
        p.id AS idProvince,
        p.libelle AS province,
        f.idannee,
        UPPER(f.type) AS type,
        SUM(COALESCE(c.nb_salles_organisees_1ere, 0)) AS nb_salles_organisees_1ere,
        SUM(COALESCE(c.nb_salles_organisees_2eme, 0)) AS nb_salles_organisees_2eme,
        SUM(COALESCE(c.nb_salles_organisees_3eme, 0)) AS nb_salles_organisees_3eme,
        SUM(
            COALESCE(c.nb_salles_organisees_1ere, 0) +
            COALESCE(c.nb_salles_organisees_2eme, 0) +
            COALESCE(c.nb_salles_organisees_3eme, 0)
        ) AS Total
    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    LEFT JOIN st1_infrastructure c ON f.id = c.form_st_id
    WHERE {where_clause}
    GROUP BY 
        p.id, 
        p.libelle, 
        f.idannee, 
        UPPER(f.type)
    ORDER BY 
        p.id, 
        f.idannee, 
        UPPER(f.type)
    """
    
    if page_size is not None:
        base_query += f" LIMIT {page_size} OFFSET {offset}"
    
    return base_query

def get_province_detail_query(where_clause, page_size=None, offset=0):
    base_query = f"""
    SELECT 
        p.id AS idProvince,
        p.libelle AS province,
        f.idannee,
        UPPER(f.type) AS type,
        SUM(COALESCE(c.nb_salles_organisees_1ere, 0)) AS `1ere Maternelle`,
        SUM(COALESCE(c.nb_salles_organisees_2eme, 0)) AS `2eme Maternelle`,
        SUM(COALESCE(c.nb_salles_organisees_3eme, 0)) AS `3eme Maternelle`,
        SUM(
            COALESCE(c.nb_salles_organisees_1ere, 0) +
            COALESCE(c.nb_salles_organisees_2eme, 0) +
            COALESCE(c.nb_salles_organisees_3eme, 0)
        ) AS Total
    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    LEFT JOIN st1_infrastructure c ON f.id = c.form_st_id
    WHERE {where_clause}
    GROUP BY 
        p.id,
        p.libelle,
        f.idannee, 
        UPPER(f.type)
    ORDER BY 
        p.id,
        f.idannee, 
        UPPER(f.type)
    """
    
    if page_size is not None:
        base_query += f" LIMIT {page_size} OFFSET {offset}"
    
    return base_query

# Fonctions de comptage pour la pagination
def get_secteur_regime_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        JOIN provinces p ON i.fk_province_id = p.id
        LEFT JOIN st1_infrastructure c ON f.id = c.form_st_id
        WHERE {where_clause}
        GROUP BY 
            f.idannee, 
            UPPER(f.type),
            i.secteur_enseignement, 
            i.regime_gestion
    ) as subquery
    """

def get_province_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        JOIN provinces p ON i.fk_province_id = p.id
        LEFT JOIN st1_infrastructure c ON f.id = c.form_st_id
        WHERE {where_clause}
        GROUP BY 
            p.id, 
            p.libelle, 
            f.idannee, 
            UPPER(f.type)
    ) as subquery
    """

def get_province_detail_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        JOIN provinces p ON i.fk_province_id = p.id
        LEFT JOIN st1_infrastructure c ON f.id = c.form_st_id
        WHERE {where_clause}
        GROUP BY 
            p.id,
            p.libelle,
            f.idannee, 
            UPPER(f.type)
    ) as subquery
    """

# Fonctions utilitaires pour les filtres (réutilisées)
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








# ELEVES 
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

def effectifs_st1(request):
    """Vue principale pour les effectifs ST1"""
    context = {
        'annees_scolaires': get_annees_scolaires(),
        'provinces': get_provinces(),
        'types_enseignement': get_types_enseignement(),
        'milieux': get_milieux(),
    }
    return render(request, 'annuaires/effectifs_st1.html', context)

@csrf_exempt
def get_effectifs_data(request):
    """Endpoint AJAX pour récupérer les données des effectifs avec pagination"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rapport_type = data.get('rapport_type')
            filters = data.get('filters', {})
            page = int(data.get('page', 1))
            page_size = int(data.get('page_size', 10))
            
            # Calculer l'offset pour la pagination
            offset = (page - 1) * page_size
            
            # Construire la clause WHERE avec les filtres
            where_conditions = ["f.responded = 1", "UPPER(f.type) = 'ST1'"]
            params = []
            
            # Appliquer les filtres
            annee = filters.get('annee')
            if annee:
                where_conditions.append("f.idannee = %s")
                params.append(annee)
                
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
            
            # Sélectionner la requête en fonction du type de rapport
            query_mapping = {
                'effectifs_par_age_national': get_effectifs_par_age_national_query(where_clause),
                'effectifs_regime_province': get_effectifs_regime_province_query(where_clause),
                'effectifs_secteur_national': get_effectifs_secteur_national_query(where_clause),
                'effectifs_province_detail': get_effectifs_province_detail_query(where_clause),
                'effectifs_par_age_sexe': get_effectifs_par_age_sexe_query(where_clause),
            }
            
            count_mapping = {
                'effectifs_par_age_national': get_effectifs_par_age_national_count_query(where_clause),
                'effectifs_regime_province': get_effectifs_regime_province_count_query(where_clause),
                'effectifs_secteur_national': get_effectifs_secteur_national_count_query(where_clause),
                'effectifs_province_detail': get_effectifs_province_detail_count_query(where_clause),
                'effectifs_par_age_sexe': get_effectifs_par_age_sexe_count_query(where_clause),
            }
            
            query = query_mapping.get(rapport_type, get_effectifs_par_age_national_query(where_clause))
            count_query = count_mapping.get(rapport_type, get_effectifs_par_age_national_count_query(where_clause))
            
            # Ajouter la pagination si nécessaire (sauf pour les rapports agrégés)
            if rapport_type in ['effectifs_par_age_national', 'effectifs_secteur_national', 'effectifs_par_age_sexe']:
                # Pas de pagination pour les petits rapports agrégés
                pass
            else:
                query += f" LIMIT {page_size} OFFSET {offset}"
            
            # Exécuter la requête de comptage
            with connection.cursor() as cursor:
                cursor.execute(count_query, params)
                total_count = cursor.fetchone()[0]
            
            # Exécuter la requête principale
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

# Fonctions pour les différentes requêtes
def get_effectifs_par_age_national_query(where_clause):
    return f"""
    SELECT 
        '1ère Maternelle' AS Niveau,
        f.idannee,
        -- Répartition par âge (Total = Filles + Garçons)
        SUM(COALESCE(e.effectif_garcons_moins_3ans_1ere, 0) + COALESCE(e.effectif_filles_moins_3ans_1ere, 0)) AS "-3ans",
        SUM(COALESCE(e.effectif_garcons_3ans_1ere, 0) + COALESCE(e.effectif_filles_3ans_1ere, 0)) AS "3ans",
        SUM(COALESCE(e.effectif_garcons_4ans_1ere, 0) + COALESCE(e.effectif_filles_4ans_1ere, 0)) AS "4ans",
        SUM(COALESCE(e.effectif_garcons_5ans_1ere, 0) + COALESCE(e.effectif_filles_5ans_1ere, 0)) AS "5ans",
        SUM(COALESCE(e.effectif_garcons_plus_5ans_1ere, 0) + COALESCE(e.effectif_filles_plus_5ans_1ere, 0)) AS "6ans",
        -- Total 1ère Maternelle
        SUM(COALESCE(e.effectif_garcons_moins_3ans_1ere,0) + COALESCE(e.effectif_filles_moins_3ans_1ere,0) +
            COALESCE(e.effectif_garcons_3ans_1ere,0) + COALESCE(e.effectif_filles_3ans_1ere,0) +
            COALESCE(e.effectif_garcons_4ans_1ere,0) + COALESCE(e.effectif_filles_4ans_1ere,0) +
            COALESCE(e.effectif_garcons_5ans_1ere,0) + COALESCE(e.effectif_filles_5ans_1ere,0) +
            COALESCE(e.effectif_garcons_plus_5ans_1ere,0) + COALESCE(e.effectif_filles_plus_5ans_1ere,0)) AS "Total général"

    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
    WHERE {where_clause}
    GROUP BY f.idannee

    UNION ALL

    SELECT 
        '2ème Maternelle' AS Niveau,
        f.idannee,
        -- Répartition par âge (Total = Filles + Garçons)
        SUM(COALESCE(e.effectif_garcons_moins_3ans_2eme, 0) + COALESCE(e.effectif_filles_moins_3ans_2eme, 0)) AS "-3ans",
        SUM(COALESCE(e.effectif_garcons_3ans_2eme, 0) + COALESCE(e.effectif_filles_3ans_2eme, 0)) AS "3ans",
        SUM(COALESCE(e.effectif_garcons_4ans_2eme, 0) + COALESCE(e.effectif_filles_4ans_2eme, 0)) AS "4ans",
        SUM(COALESCE(e.effectif_garcons_5ans_2eme, 0) + COALESCE(e.effectif_filles_5ans_2eme, 0)) AS "5ans",
        SUM(COALESCE(e.effectif_garcons_plus_5ans_2eme, 0) + COALESCE(e.effectif_filles_plus_5ans_2eme, 0)) AS "6ans",
        -- Total 2ème Maternelle
        SUM(COALESCE(e.effectif_garcons_moins_3ans_2eme,0) + COALESCE(e.effectif_filles_moins_3ans_2eme,0) +
            COALESCE(e.effectif_garcons_3ans_2eme,0) + COALESCE(e.effectif_filles_3ans_2eme,0) +
            COALESCE(e.effectif_garcons_4ans_2eme,0) + COALESCE(e.effectif_filles_4ans_2eme,0) +
            COALESCE(e.effectif_garcons_5ans_2eme,0) + COALESCE(e.effectif_filles_5ans_2eme,0) +
            COALESCE(e.effectif_garcons_plus_5ans_2eme,0) + COALESCE(e.effectif_filles_plus_5ans_2eme,0)) AS "Total général"

    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
    WHERE {where_clause}
    GROUP BY f.idannee

    UNION ALL

    SELECT 
        '3ème Maternelle' AS Niveau,
        f.idannee,
        -- Répartition par âge (Total = Filles + Garçons)
        SUM(COALESCE(e.effectif_garcons_moins_3ans_3eme, 0) + COALESCE(e.effectif_filles_moins_3ans_3eme, 0)) AS "-3ans",
        SUM(COALESCE(e.effectif_garcons_3ans_3eme, 0) + COALESCE(e.effectif_filles_3ans_3eme, 0)) AS "3ans",
        SUM(COALESCE(e.effectif_garcons_4ans_3eme, 0) + COALESCE(e.effectif_filles_4ans_3eme, 0)) AS "4ans",
        SUM(COALESCE(e.effectif_garcons_5ans_3eme, 0) + COALESCE(e.effectif_filles_5ans_3eme, 0)) AS "5ans",
        SUM(COALESCE(e.effectif_garcons_plus_5ans_3eme, 0) + COALESCE(e.effectif_filles_plus_5ans_3eme, 0)) AS "6ans",
        -- Total 3ème Maternelle
        SUM(COALESCE(e.effectif_garcons_moins_3ans_3eme,0) + COALESCE(e.effectif_filles_moins_3ans_3eme,0) +
            COALESCE(e.effectif_garcons_3ans_3eme,0) + COALESCE(e.effectif_filles_3ans_3eme,0) +
            COALESCE(e.effectif_garcons_4ans_3eme,0) + COALESCE(e.effectif_filles_4ans_3eme,0) +
            COALESCE(e.effectif_garcons_5ans_3eme,0) + COALESCE(e.effectif_filles_5ans_3eme,0) +
            COALESCE(e.effectif_garcons_plus_5ans_3eme,0) + COALESCE(e.effectif_filles_plus_5ans_3eme,0)) AS "Total général"

    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
    WHERE {where_clause}
    GROUP BY f.idannee

    UNION ALL

    SELECT 
        'Pré-primaire' AS Niveau,
        f.idannee,
        -- Pré-primaire (moins de 3 ans seulement) - Total des 3 classes
        SUM(COALESCE(e.effectif_garcons_moins_3ans_1ere, 0) + COALESCE(e.effectif_filles_moins_3ans_1ere, 0) +
            COALESCE(e.effectif_garcons_moins_3ans_2eme, 0) + COALESCE(e.effectif_filles_moins_3ans_2eme, 0) +
            COALESCE(e.effectif_garcons_moins_3ans_3eme, 0) + COALESCE(e.effectif_filles_moins_3ans_3eme, 0)) AS "-3ans",
        -- Les autres colonnes sont à 0 pour le pré-primaire
        0 AS "3ans",
        0 AS "4ans",
        0 AS "5ans",
        0 AS "6ans",
        -- Total pré-primaire (uniquement les moins de 3 ans)
        SUM(COALESCE(e.effectif_garcons_moins_3ans_1ere, 0) + COALESCE(e.effectif_filles_moins_3ans_1ere, 0) +
            COALESCE(e.effectif_garcons_moins_3ans_2eme, 0) + COALESCE(e.effectif_filles_moins_3ans_2eme, 0) +
            COALESCE(e.effectif_garcons_moins_3ans_3eme, 0) + COALESCE(e.effectif_filles_moins_3ans_3eme, 0)) AS "Total général"

    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
    WHERE {where_clause}
    GROUP BY f.idannee

    ORDER BY idannee,
             CASE WHEN Niveau = 'Pré-primaire' THEN 1
                  WHEN Niveau = '1ère Maternelle' THEN 2 
                  WHEN Niveau = '2ème Maternelle' THEN 3 
                  WHEN Niveau = '3ème Maternelle' THEN 4 
                  ELSE 5 END;
    """

def get_effectifs_regime_province_query(where_clause):
    return f"""
    SELECT
        p.id AS id,
        p.libelle AS "provinces.libelle",
        f.idannee AS idannee,
        'Garçons' AS sexe,
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ECC' THEN e.total_garcons ELSE 0 END) AS ECC,
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ECF' THEN e.total_garcons ELSE 0 END) AS ECF,
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ECI' THEN e.total_garcons ELSE 0 END) AS ECI,
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ECK' THEN e.total_garcons ELSE 0 END) AS ECK,
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ECP' THEN e.total_garcons ELSE 0 END) AS ECP,
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ECS' THEN e.total_garcons ELSE 0 END) AS ECS,
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ENC' THEN e.total_garcons ELSE 0 END) AS ENC,
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'AUTRES' THEN e.total_garcons ELSE 0 END) AS AUTRES,
        SUM(CASE WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN e.total_garcons ELSE 0 END) AS NR,
        -- Total Public (tout sauf EPR)
        SUM(CASE WHEN UPPER(i.regime_gestion) != 'EPR' AND (i.regime_gestion IS NOT NULL AND i.regime_gestion != '') THEN e.total_garcons ELSE 0 END) AS "Total Public",
        -- Privé (EPR)
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'EPR' THEN e.total_garcons ELSE 0 END) AS "Privé",
        -- Total Général
        SUM(e.total_garcons) AS "Total Général"
    FROM provinces p
    JOIN identifications i ON p.id = i.fk_province_id
    JOIN formulaires f ON f.identification_id = i.id
    JOIN (
        SELECT form_st_id,
               SUM(COALESCE(effectif_garcons_moins_3ans_1ere,0) + COALESCE(effectif_garcons_moins_3ans_2eme,0) + COALESCE(effectif_garcons_moins_3ans_3eme,0) +
                   COALESCE(effectif_garcons_3ans_1ere,0) + COALESCE(effectif_garcons_3ans_2eme,0) + COALESCE(effectif_garcons_3ans_3eme,0) +
                   COALESCE(effectif_garcons_4ans_1ere,0) + COALESCE(effectif_garcons_4ans_2eme,0) + COALESCE(effectif_garcons_4ans_3eme,0) +
                   COALESCE(effectif_garcons_5ans_1ere,0) + COALESCE(effectif_garcons_5ans_2eme,0) + COALESCE(effectif_garcons_5ans_3eme,0) +
                   COALESCE(effectif_garcons_plus_5ans_1ere,0) + COALESCE(effectif_garcons_plus_5ans_2eme,0) + COALESCE(effectif_garcons_plus_5ans_3eme,0)) AS total_garcons,
               SUM(COALESCE(effectif_filles_moins_3ans_1ere,0) + COALESCE(effectif_filles_moins_3ans_2eme,0) + COALESCE(effectif_filles_moins_3ans_3eme,0) +
                   COALESCE(effectif_filles_3ans_1ere,0) + COALESCE(effectif_filles_3ans_2eme,0) + COALESCE(effectif_filles_3ans_3eme,0) +
                   COALESCE(effectif_filles_4ans_1ere,0) + COALESCE(effectif_filles_4ans_2eme,0) + COALESCE(effectif_filles_4ans_3eme,0) +
                   COALESCE(effectif_filles_5ans_1ere,0) + COALESCE(effectif_filles_5ans_2eme,0) + COALESCE(effectif_filles_5ans_3eme,0) +
                   COALESCE(effectif_filles_plus_5ans_1ere,0) + COALESCE(effectif_filles_plus_5ans_2eme,0) + COALESCE(effectif_filles_plus_5ans_3eme,0)) AS total_filles
        FROM st1_effectifs_par_age
        GROUP BY form_st_id
    ) e ON e.form_st_id = f.id
    WHERE {where_clause}
    GROUP BY p.id, p.libelle, f.idannee

    UNION ALL

    SELECT
        p.id AS id,
        p.libelle AS "provinces.libelle",
        f.idannee AS idannee,
        'Filles' AS sexe,
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ECC' THEN e.total_filles ELSE 0 END) AS ECC,
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ECF' THEN e.total_filles ELSE 0 END) AS ECF,
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ECI' THEN e.total_filles ELSE 0 END) AS ECI,
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ECK' THEN e.total_filles ELSE 0 END) AS ECK,
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ECP' THEN e.total_filles ELSE 0 END) AS ECP,
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ECS' THEN e.total_filles ELSE 0 END) AS ECS,
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ENC' THEN e.total_filles ELSE 0 END) AS ENC,
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'AUTRES' THEN e.total_filles ELSE 0 END) AS AUTRES,
        SUM(CASE WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN e.total_filles ELSE 0 END) AS NR,
        -- Total Public (tout sauf EPR)
        SUM(CASE WHEN UPPER(i.regime_gestion) != 'EPR' AND (i.regime_gestion IS NOT NULL AND i.regime_gestion != '') THEN e.total_filles ELSE 0 END) AS "Total Public",
        -- Privé (EPR)
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'EPR' THEN e.total_filles ELSE 0 END) AS "Privé",
        -- Total Général
        SUM(e.total_filles) AS "Total Général"
    FROM provinces p
    JOIN identifications i ON p.id = i.fk_province_id
    JOIN formulaires f ON f.identification_id = i.id
    JOIN (
        SELECT form_st_id,
               SUM(COALESCE(effectif_garcons_moins_3ans_1ere,0) + COALESCE(effectif_garcons_moins_3ans_2eme,0) + COALESCE(effectif_garcons_moins_3ans_3eme,0) +
                   COALESCE(effectif_garcons_3ans_1ere,0) + COALESCE(effectif_garcons_3ans_2eme,0) + COALESCE(effectif_garcons_3ans_3eme,0) +
                   COALESCE(effectif_garcons_4ans_1ere,0) + COALESCE(effectif_garcons_4ans_2eme,0) + COALESCE(effectif_garcons_4ans_3eme,0) +
                   COALESCE(effectif_garcons_5ans_1ere,0) + COALESCE(effectif_garcons_5ans_2eme,0) + COALESCE(effectif_garcons_5ans_3eme,0) +
                   COALESCE(effectif_garcons_plus_5ans_1ere,0) + COALESCE(effectif_garcons_plus_5ans_2eme,0) + COALESCE(effectif_garcons_plus_5ans_3eme,0)) AS total_garcons,
               SUM(COALESCE(effectif_filles_moins_3ans_1ere,0) + COALESCE(effectif_filles_moins_3ans_2eme,0) + COALESCE(effectif_filles_moins_3ans_3eme,0) +
                   COALESCE(effectif_filles_3ans_1ere,0) + COALESCE(effectif_filles_3ans_2eme,0) + COALESCE(effectif_filles_3ans_3eme,0) +
                   COALESCE(effectif_filles_4ans_1ere,0) + COALESCE(effectif_filles_4ans_2eme,0) + COALESCE(effectif_filles_4ans_3eme,0) +
                   COALESCE(effectif_filles_5ans_1ere,0) + COALESCE(effectif_filles_5ans_2eme,0) + COALESCE(effectif_filles_5ans_3eme,0) +
                   COALESCE(effectif_filles_plus_5ans_1ere,0) + COALESCE(effectif_filles_plus_5ans_2eme,0) + COALESCE(effectif_filles_plus_5ans_3eme,0)) AS total_filles
        FROM st1_effectifs_par_age
        GROUP BY form_st_id
    ) e ON e.form_st_id = f.id
    WHERE {where_clause}
    GROUP BY p.id, p.libelle, f.idannee

    ORDER BY idannee, id,
             CASE WHEN sexe = 'Garçons' THEN 1 
                  WHEN sexe = 'Filles' THEN 2 
                  ELSE 3 END;
    """

def get_effectifs_secteur_national_query(where_clause):
    return f"""
    SELECT 
        CASE 
            WHEN UPPER(i.regime_gestion) = 'EPR' THEN 'Privé'
            WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN 'NR'
            ELSE 'Public'
        END AS secteur,
        COALESCE(i.regime_gestion, 'NR') AS regime_gestion,
        'Garçons' AS sexe,
        f.idannee,

        -- 👦 Garçons - 1ère Maternelle
        SUM(COALESCE(e.effectif_garcons_moins_3ans_1ere,0) + COALESCE(e.effectif_garcons_3ans_1ere,0) +
            COALESCE(e.effectif_garcons_4ans_1ere,0) + COALESCE(e.effectif_garcons_5ans_1ere,0) +
            COALESCE(e.effectif_garcons_plus_5ans_1ere,0)) AS 1ere_maternelle,

        -- 👦 Garçons - 2ème Maternelle
        SUM(COALESCE(e.effectif_garcons_moins_3ans_2eme,0) + COALESCE(e.effectif_garcons_3ans_2eme,0) +
            COALESCE(e.effectif_garcons_4ans_2eme,0) + COALESCE(e.effectif_garcons_5ans_2eme,0) +
            COALESCE(e.effectif_garcons_plus_5ans_2eme,0)) AS 2eme_maternelle,

        -- 👦 Garçons - 3ème Maternelle
        SUM(COALESCE(e.effectif_garcons_moins_3ans_3eme,0) + COALESCE(e.effectif_garcons_3ans_3eme,0) +
            COALESCE(e.effectif_garcons_4ans_3eme,0) + COALESCE(e.effectif_garcons_5ans_3eme,0) +
            COALESCE(e.effectif_garcons_plus_5ans_3eme,0)) AS 3eme_maternelle,

        -- 🟪 Garçons - Pré-primaire (moins de 3 ans seulement)
        SUM(
            COALESCE(e.effectif_garcons_moins_3ans_1ere,0) + 
            COALESCE(e.effectif_garcons_moins_3ans_2eme,0) + 
            COALESCE(e.effectif_garcons_moins_3ans_3eme,0)
        ) AS pre_primaire,

        -- 🔵 Garçons - Total général (tous les âges, toutes les classes)
        SUM(
            COALESCE(e.effectif_garcons_moins_3ans_1ere,0) + COALESCE(e.effectif_garcons_moins_3ans_2eme,0) + COALESCE(e.effectif_garcons_moins_3ans_3eme,0) +
            COALESCE(e.effectif_garcons_3ans_1ere,0) + COALESCE(e.effectif_garcons_3ans_2eme,0) + COALESCE(e.effectif_garcons_3ans_3eme,0) +
            COALESCE(e.effectif_garcons_4ans_1ere,0) + COALESCE(e.effectif_garcons_4ans_2eme,0) + COALESCE(e.effectif_garcons_4ans_3eme,0) +
            COALESCE(e.effectif_garcons_5ans_1ere,0) + COALESCE(e.effectif_garcons_5ans_2eme,0) + COALESCE(e.effectif_garcons_5ans_3eme,0) +
            COALESCE(e.effectif_garcons_plus_5ans_1ere,0) + COALESCE(e.effectif_garcons_plus_5ans_2eme,0) + COALESCE(e.effectif_garcons_plus_5ans_3eme,0)
        ) AS total_general

    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
    WHERE {where_clause}
    GROUP BY secteur, i.regime_gestion, f.idannee

    UNION ALL

    SELECT 
        CASE 
            WHEN UPPER(i.regime_gestion) = 'EPR' THEN 'Privé'
            WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN 'NR'
            ELSE 'Public'
        END AS secteur,
        COALESCE(i.regime_gestion, 'NR') AS regime_gestion,
        'Filles' AS sexe,
        f.idannee,

        -- 👧 Filles - 1ère Maternelle
        SUM(COALESCE(e.effectif_filles_moins_3ans_1ere,0) + COALESCE(e.effectif_filles_3ans_1ere,0) +
            COALESCE(e.effectif_filles_4ans_1ere,0) + COALESCE(e.effectif_filles_5ans_1ere,0) +
            COALESCE(e.effectif_filles_plus_5ans_1ere,0)) AS 1ere_maternelle,

        -- 👧 Filles - 2ème Maternelle
        SUM(COALESCE(e.effectif_filles_moins_3ans_2eme,0) + COALESCE(e.effectif_filles_3ans_2eme,0) +
            COALESCE(e.effectif_filles_4ans_2eme,0) + COALESCE(e.effectif_filles_5ans_2eme,0) +
            COALESCE(e.effectif_filles_plus_5ans_2eme,0)) AS 2eme_maternelle,

        -- 👧 Filles - 3ème Maternelle
        SUM(COALESCE(e.effectif_filles_moins_3ans_3eme,0) + COALESCE(e.effectif_filles_3ans_3eme,0) +
            COALESCE(e.effectif_filles_4ans_3eme,0) + COALESCE(e.effectif_filles_5ans_3eme,0) +
            COALESCE(e.effectif_filles_plus_5ans_3eme,0)) AS 3eme_maternelle,

        -- 🟪 Filles - Pré-primaire (moins de 3 ans seulement)
        SUM(
            COALESCE(e.effectif_filles_moins_3ans_1ere,0) + 
            COALESCE(e.effectif_filles_moins_3ans_2eme,0) + 
            COALESCE(e.effectif_filles_moins_3ans_3eme,0)
        ) AS pre_primaire,

        -- 🔵 Filles - Total général (tous les âges, toutes les classes)
        SUM(
            COALESCE(e.effectif_filles_moins_3ans_1ere,0) + COALESCE(e.effectif_filles_moins_3ans_2eme,0) + COALESCE(e.effectif_filles_moins_3ans_3eme,0) +
            COALESCE(e.effectif_filles_3ans_1ere,0) + COALESCE(e.effectif_filles_3ans_2eme,0) + COALESCE(e.effectif_filles_3ans_3eme,0) +
            COALESCE(e.effectif_filles_4ans_1ere,0) + COALESCE(e.effectif_filles_4ans_2eme,0) + COALESCE(e.effectif_filles_4ans_3eme,0) +
            COALESCE(e.effectif_filles_5ans_1ere,0) + COALESCE(e.effectif_filles_5ans_2eme,0) + COALESCE(e.effectif_filles_5ans_3eme,0) +
            COALESCE(e.effectif_filles_plus_5ans_1ere,0) + COALESCE(e.effectif_filles_plus_5ans_2eme,0) + COALESCE(e.effectif_filles_plus_5ans_3eme,0)
        ) AS total_general

    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
    WHERE {where_clause}
    GROUP BY secteur, i.regime_gestion, f.idannee

    UNION ALL

    SELECT 
        CASE 
            WHEN UPPER(i.regime_gestion) = 'EPR' THEN 'Privé'
            WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN 'NR'
            ELSE 'Public'
        END AS secteur,
        COALESCE(i.regime_gestion, 'NR') AS regime_gestion,
        'Total' AS sexe,
        f.idannee,

        -- 👨‍👩‍👧‍👦 Total - 1ère Maternelle
        SUM(
            COALESCE(e.effectif_garcons_moins_3ans_1ere,0) + COALESCE(e.effectif_filles_moins_3ans_1ere,0) +
            COALESCE(e.effectif_garcons_3ans_1ere,0) + COALESCE(e.effectif_filles_3ans_1ere,0) +
            COALESCE(e.effectif_garcons_4ans_1ere,0) + COALESCE(e.effectif_filles_4ans_1ere,0) +
            COALESCE(e.effectif_garcons_5ans_1ere,0) + COALESCE(e.effectif_filles_5ans_1ere,0) +
            COALESCE(e.effectif_garcons_plus_5ans_1ere,0) + COALESCE(e.effectif_filles_plus_5ans_1ere,0)
        ) AS 1ere_maternelle,

        -- 👨‍👩‍👧‍👦 Total - 2ème Maternelle
        SUM(
            COALESCE(e.effectif_garcons_moins_3ans_2eme,0) + COALESCE(e.effectif_filles_moins_3ans_2eme,0) +
            COALESCE(e.effectif_garcons_3ans_2eme,0) + COALESCE(e.effectif_filles_3ans_2eme,0) +
            COALESCE(e.effectif_garcons_4ans_2eme,0) + COALESCE(e.effectif_filles_4ans_2eme,0) +
            COALESCE(e.effectif_garcons_5ans_2eme,0) + COALESCE(e.effectif_filles_5ans_2eme,0) +
            COALESCE(e.effectif_garcons_plus_5ans_2eme,0) + COALESCE(e.effectif_filles_plus_5ans_2eme,0)
        ) AS 2eme_maternelle,

        -- 👨‍👩‍👧‍👦 Total - 3ème Maternelle
        SUM(
            COALESCE(e.effectif_garcons_moins_3ans_3eme,0) + COALESCE(e.effectif_filles_moins_3ans_3eme,0) +
            COALESCE(e.effectif_garcons_3ans_3eme,0) + COALESCE(e.effectif_filles_3ans_3eme,0) +
            COALESCE(e.effectif_garcons_4ans_3eme,0) + COALESCE(e.effectif_filles_4ans_3eme,0) +
            COALESCE(e.effectif_garcons_5ans_3eme,0) + COALESCE(e.effectif_filles_5ans_3eme,0) +
            COALESCE(e.effectif_garcons_plus_5ans_3eme,0) + COALESCE(e.effectif_filles_plus_5ans_3eme,0)
        ) AS 3eme_maternelle,

        -- 🟪 Total - Pré-primaire (moins de 3 ans seulement)
        SUM(
            COALESCE(e.effectif_garcons_moins_3ans_1ere,0) + COALESCE(e.effectif_filles_moins_3ans_1ere,0) +
            COALESCE(e.effectif_garcons_moins_3ans_2eme,0) + COALESCE(e.effectif_filles_moins_3ans_2eme,0) +
            COALESCE(e.effectif_garcons_moins_3ans_3eme,0) + COALESCE(e.effectif_filles_moins_3ans_3eme,0)
        ) AS pre_primaire,

        -- 🔵 Total - Total général (tous les âges, toutes les classes)
        SUM(
            COALESCE(e.effectif_garcons_moins_3ans_1ere,0) + COALESCE(e.effectif_filles_moins_3ans_1ere,0) +
            COALESCE(e.effectif_garcons_moins_3ans_2eme,0) + COALESCE(e.effectif_filles_moins_3ans_2eme,0) +
            COALESCE(e.effectif_garcons_moins_3ans_3eme,0) + COALESCE(e.effectif_filles_moins_3ans_3eme,0) +
            COALESCE(e.effectif_garcons_3ans_1ere,0) + COALESCE(e.effectif_filles_3ans_1ere,0) +
            COALESCE(e.effectif_garcons_3ans_2eme,0) + COALESCE(e.effectif_filles_3ans_2eme,0) +
            COALESCE(e.effectif_garcons_3ans_3eme,0) + COALESCE(e.effectif_filles_3ans_3eme,0) +
            COALESCE(e.effectif_garcons_4ans_1ere,0) + COALESCE(e.effectif_filles_4ans_1ere,0) +
            COALESCE(e.effectif_garcons_4ans_2eme,0) + COALESCE(e.effectif_filles_4ans_2eme,0) +
            COALESCE(e.effectif_garcons_4ans_3eme,0) + COALESCE(e.effectif_filles_4ans_3eme,0) +
            COALESCE(e.effectif_garcons_5ans_1ere,0) + COALESCE(e.effectif_filles_5ans_1ere,0) +
            COALESCE(e.effectif_garcons_5ans_2eme,0) + COALESCE(e.effectif_filles_5ans_2eme,0) +
            COALESCE(e.effectif_garcons_5ans_3eme,0) + COALESCE(e.effectif_filles_5ans_3eme,0) +
            COALESCE(e.effectif_garcons_plus_5ans_1ere,0) + COALESCE(e.effectif_filles_plus_5ans_1ere,0) +
            COALESCE(e.effectif_garcons_plus_5ans_2eme,0) + COALESCE(e.effectif_filles_plus_5ans_2eme,0) +
            COALESCE(e.effectif_garcons_plus_5ans_3eme,0) + COALESCE(e.effectif_filles_plus_5ans_3eme,0)
        ) AS total_general

    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
    WHERE {where_clause}
    GROUP BY secteur, i.regime_gestion, f.idannee

    ORDER BY idannee, secteur, regime_gestion, 
             CASE WHEN sexe = 'Garçons' THEN 1 
                  WHEN sexe = 'Filles' THEN 2 
                  ELSE 3 END;
    """

def get_effectifs_province_detail_query(where_clause):
    return f"""
    SELECT 
        p.id AS id,
        p.libelle AS "provinces.libelle",
        'Garçons' AS sexe,
        f.idannee,

        -- 👦 Garçons - 1ère Maternelle
        SUM(COALESCE(e.effectif_garcons_moins_3ans_1ere,0) + COALESCE(e.effectif_garcons_3ans_1ere,0) +
            COALESCE(e.effectif_garcons_4ans_1ere,0) + COALESCE(e.effectif_garcons_5ans_1ere,0) +
            COALESCE(e.effectif_garcons_plus_5ans_1ere,0)) AS 1ere_maternelle,

        -- 👦 Garçons - 2ème Maternelle
        SUM(COALESCE(e.effectif_garcons_moins_3ans_2eme,0) + COALESCE(e.effectif_garcons_3ans_2eme,0) +
            COALESCE(e.effectif_garcons_4ans_2eme,0) + COALESCE(e.effectif_garcons_5ans_2eme,0) +
            COALESCE(e.effectif_garcons_plus_5ans_2eme,0)) AS 2eme_maternelle,

        -- 👦 Garçons - 3ème Maternelle
        SUM(COALESCE(e.effectif_garcons_moins_3ans_3eme,0) + COALESCE(e.effectif_garcons_3ans_3eme,0) +
            COALESCE(e.effectif_garcons_4ans_3eme,0) + COALESCE(e.effectif_garcons_5ans_3eme,0) +
            COALESCE(e.effectif_garcons_plus_5ans_3eme,0)) AS 3eme_maternelle,

        -- 🟪 Garçons - Pré-primaire (moins de 3 ans seulement)
        SUM(
            COALESCE(e.effectif_garcons_moins_3ans_1ere,0) + 
            COALESCE(e.effectif_garcons_moins_3ans_2eme,0) + 
            COALESCE(e.effectif_garcons_moins_3ans_3eme,0)
        ) AS pre_primaire,

        -- 🔵 Garçons - Total général (tous les âges, toutes les classes)
        SUM(
            COALESCE(e.effectif_garcons_moins_3ans_1ere,0) + COALESCE(e.effectif_garcons_moins_3ans_2eme,0) + COALESCE(e.effectif_garcons_moins_3ans_3eme,0) +
            COALESCE(e.effectif_garcons_3ans_1ere,0) + COALESCE(e.effectif_garcons_3ans_2eme,0) + COALESCE(e.effectif_garcons_3ans_3eme,0) +
            COALESCE(e.effectif_garcons_4ans_1ere,0) + COALESCE(e.effectif_garcons_4ans_2eme,0) + COALESCE(e.effectif_garcons_4ans_3eme,0) +
            COALESCE(e.effectif_garcons_5ans_1ere,0) + COALESCE(e.effectif_garcons_5ans_2eme,0) + COALESCE(e.effectif_garcons_5ans_3eme,0) +
            COALESCE(e.effectif_garcons_plus_5ans_1ere,0) + COALESCE(e.effectif_garcons_plus_5ans_2eme,0) + COALESCE(e.effectif_garcons_plus_5ans_3eme,0)
        ) AS total_general,

        -- NR - Garçons (régime de gestion vide)
        SUM(CASE WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN 
            COALESCE(e.effectif_garcons_moins_3ans_1ere,0) + COALESCE(e.effectif_garcons_moins_3ans_2eme,0) + COALESCE(e.effectif_garcons_moins_3ans_3eme,0) +
            COALESCE(e.effectif_garcons_3ans_1ere,0) + COALESCE(e.effectif_garcons_3ans_2eme,0) + COALESCE(e.effectif_garcons_3ans_3eme,0) +
            COALESCE(e.effectif_garcons_4ans_1ere,0) + COALESCE(e.effectif_garcons_4ans_2eme,0) + COALESCE(e.effectif_garcons_4ans_3eme,0) +
            COALESCE(e.effectif_garcons_5ans_1ere,0) + COALESCE(e.effectif_garcons_5ans_2eme,0) + COALESCE(e.effectif_garcons_5ans_3eme,0) +
            COALESCE(e.effectif_garcons_plus_5ans_1ere,0) + COALESCE(e.effectif_garcons_plus_5ans_2eme,0) + COALESCE(e.effectif_garcons_plus_5ans_3eme,0)
        ELSE 0 END) AS NR

    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON p.id = i.fk_province_id
    LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
    WHERE {where_clause}
    GROUP BY p.id, p.libelle, f.idannee

    UNION ALL

    SELECT 
        p.id AS id,
        p.libelle AS "provinces.libelle",
        'Filles' AS sexe,
        f.idannee,

        -- 👧 Filles - 1ère Maternelle
        SUM(COALESCE(e.effectif_filles_moins_3ans_1ere,0) + COALESCE(e.effectif_filles_3ans_1ere,0) +
            COALESCE(e.effectif_filles_4ans_1ere,0) + COALESCE(e.effectif_filles_5ans_1ere,0) +
            COALESCE(e.effectif_filles_plus_5ans_1ere,0)) AS 1ere_maternelle,

        -- 👧 Filles - 2ème Maternelle
        SUM(COALESCE(e.effectif_filles_moins_3ans_2eme,0) + COALESCE(e.effectif_filles_3ans_2eme,0) +
            COALESCE(e.effectif_filles_4ans_2eme,0) + COALESCE(e.effectif_filles_5ans_2eme,0) +
            COALESCE(e.effectif_filles_plus_5ans_2eme,0)) AS 2eme_maternelle,

        -- 👧 Filles - 3ème Maternelle
        SUM(COALESCE(e.effectif_filles_moins_3ans_3eme,0) + COALESCE(e.effectif_filles_3ans_3eme,0) +
            COALESCE(e.effectif_filles_4ans_3eme,0) + COALESCE(e.effectif_filles_5ans_3eme,0) +
            COALESCE(e.effectif_filles_plus_5ans_3eme,0)) AS 3eme_maternelle,

        -- 🟪 Filles - Pré-primaire (moins de 3 ans seulement)
        SUM(
            COALESCE(e.effectif_filles_moins_3ans_1ere,0) + 
            COALESCE(e.effectif_filles_moins_3ans_2eme,0) + 
            COALESCE(e.effectif_filles_moins_3ans_3eme,0)
        ) AS pre_primaire,

        -- 🔵 Filles - Total général (tous les âges, toutes les classes)
        SUM(
            COALESCE(e.effectif_filles_moins_3ans_1ere,0) + COALESCE(e.effectif_filles_moins_3ans_2eme,0) + COALESCE(e.effectif_filles_moins_3ans_3eme,0) +
            COALESCE(e.effectif_filles_3ans_1ere,0) + COALESCE(e.effectif_filles_3ans_2eme,0) + COALESCE(e.effectif_filles_3ans_3eme,0) +
            COALESCE(e.effectif_filles_4ans_1ere,0) + COALESCE(e.effectif_filles_4ans_2eme,0) + COALESCE(e.effectif_filles_4ans_3eme,0) +
            COALESCE(e.effectif_filles_5ans_1ere,0) + COALESCE(e.effectif_filles_5ans_2eme,0) + COALESCE(e.effectif_filles_5ans_3eme,0) +
            COALESCE(e.effectif_filles_plus_5ans_1ere,0) + COALESCE(e.effectif_filles_plus_5ans_2eme,0) + COALESCE(e.effectif_filles_plus_5ans_3eme,0)
        ) AS total_general,

        -- NR - Filles (régime de gestion vide)
        SUM(CASE WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN 
            COALESCE(e.effectif_filles_moins_3ans_1ere,0) + COALESCE(e.effectif_filles_moins_3ans_2eme,0) + COALESCE(e.effectif_filles_moins_3ans_3eme,0) +
            COALESCE(e.effectif_filles_3ans_1ere,0) + COALESCE(e.effectif_filles_3ans_2eme,0) + COALESCE(e.effectif_filles_3ans_3eme,0) +
            COALESCE(e.effectif_filles_4ans_1ere,0) + COALESCE(e.effectif_filles_4ans_2eme,0) + COALESCE(e.effectif_filles_4ans_3eme,0) +
            COALESCE(e.effectif_filles_5ans_1ere,0) + COALESCE(e.effectif_filles_5ans_2eme,0) + COALESCE(e.effectif_filles_5ans_3eme,0) +
            COALESCE(e.effectif_filles_plus_5ans_1ere,0) + COALESCE(e.effectif_filles_plus_5ans_2eme,0) + COALESCE(e.effectif_filles_plus_5ans_3eme,0)
        ELSE 0 END) AS NR

    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON p.id = i.fk_province_id
    LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
    WHERE {where_clause}
    GROUP BY p.id, p.libelle, f.idannee

    UNION ALL

    SELECT 
        p.id AS id,
        p.libelle AS "provinces.libelle",
        'Total' AS sexe,
        f.idannee,

        -- 👨‍👩‍👧‍👦 Total - 1ère Maternelle
        SUM(
            COALESCE(e.effectif_garcons_moins_3ans_1ere,0) + COALESCE(e.effectif_filles_moins_3ans_1ere,0) +
            COALESCE(e.effectif_garcons_3ans_1ere,0) + COALESCE(e.effectif_filles_3ans_1ere,0) +
            COALESCE(e.effectif_garcons_4ans_1ere,0) + COALESCE(e.effectif_filles_4ans_1ere,0) +
            COALESCE(e.effectif_garcons_5ans_1ere,0) + COALESCE(e.effectif_filles_5ans_1ere,0) +
            COALESCE(e.effectif_garcons_plus_5ans_1ere,0) + COALESCE(e.effectif_filles_plus_5ans_1ere,0)
        ) AS 1ere_maternelle,

        -- 👨‍👩‍👧‍👦 Total - 2ème Maternelle
        SUM(
            COALESCE(e.effectif_garcons_moins_3ans_2eme,0) + COALESCE(e.effectif_filles_moins_3ans_2eme,0) +
            COALESCE(e.effectif_garcons_3ans_2eme,0) + COALESCE(e.effectif_filles_3ans_2eme,0) +
            COALESCE(e.effectif_garcons_4ans_2eme,0) + COALESCE(e.effectif_filles_4ans_2eme,0) +
            COALESCE(e.effectif_garcons_5ans_2eme,0) + COALESCE(e.effectif_filles_5ans_2eme,0) +
            COALESCE(e.effectif_garcons_plus_5ans_2eme,0) + COALESCE(e.effectif_filles_plus_5ans_2eme,0)
        ) AS 2eme_maternelle,

        -- 👨‍👩‍👧‍👦 Total - 3ème Maternelle
        SUM(
            COALESCE(e.effectif_garcons_moins_3ans_3eme,0) + COALESCE(e.effectif_filles_moins_3ans_3eme,0) +
            COALESCE(e.effectif_garcons_3ans_3eme,0) + COALESCE(e.effectif_filles_3ans_3eme,0) +
            COALESCE(e.effectif_garcons_4ans_3eme,0) + COALESCE(e.effectif_filles_4ans_3eme,0) +
            COALESCE(e.effectif_garcons_5ans_3eme,0) + COALESCE(e.effectif_filles_5ans_3eme,0) +
            COALESCE(e.effectif_garcons_plus_5ans_3eme,0) + COALESCE(e.effectif_filles_plus_5ans_3eme,0)
        ) AS 3eme_maternelle,

        -- 🟪 Total - Pré-primaire (moins de 3 ans seulement)
        SUM(
            COALESCE(e.effectif_garcons_moins_3ans_1ere,0) + COALESCE(e.effectif_filles_moins_3ans_1ere,0) +
            COALESCE(e.effectif_garcons_moins_3ans_2eme,0) + COALESCE(e.effectif_filles_moins_3ans_2eme,0) +
            COALESCE(e.effectif_garcons_moins_3ans_3eme,0) + COALESCE(e.effectif_filles_moins_3ans_3eme,0)
        ) AS pre_primaire,

        -- 🔵 Total - Total général (tous les âges, toutes les classes)
        SUM(
            COALESCE(e.effectif_garcons_moins_3ans_1ere,0) + COALESCE(e.effectif_filles_moins_3ans_1ere,0) +
            COALESCE(e.effectif_garcons_moins_3ans_2eme,0) + COALESCE(e.effectif_filles_moins_3ans_2eme,0) +
            COALESCE(e.effectif_garcons_moins_3ans_3eme,0) + COALESCE(e.effectif_filles_moins_3ans_3eme,0) +
            COALESCE(e.effectif_garcons_3ans_1ere,0) + COALESCE(e.effectif_filles_3ans_1ere,0) +
            COALESCE(e.effectif_garcons_3ans_2eme,0) + COALESCE(e.effectif_filles_3ans_2eme,0) +
            COALESCE(e.effectif_garcons_3ans_3eme,0) + COALESCE(e.effectif_filles_3ans_3eme,0) +
            COALESCE(e.effectif_garcons_4ans_1ere,0) + COALESCE(e.effectif_filles_4ans_1ere,0) +
            COALESCE(e.effectif_garcons_4ans_2eme,0) + COALESCE(e.effectif_filles_4ans_2eme,0) +
            COALESCE(e.effectif_garcons_4ans_3eme,0) + COALESCE(e.effectif_filles_4ans_3eme,0) +
            COALESCE(e.effectif_garcons_5ans_1ere,0) + COALESCE(e.effectif_filles_5ans_1ere,0) +
            COALESCE(e.effectif_garcons_5ans_2eme,0) + COALESCE(e.effectif_filles_5ans_2eme,0) +
            COALESCE(e.effectif_garcons_5ans_3eme,0) + COALESCE(e.effectif_filles_5ans_3eme,0) +
            COALESCE(e.effectif_garcons_plus_5ans_1ere,0) + COALESCE(e.effectif_filles_plus_5ans_1ere,0) +
            COALESCE(e.effectif_garcons_plus_5ans_2eme,0) + COALESCE(e.effectif_filles_plus_5ans_2eme,0) +
            COALESCE(e.effectif_garcons_plus_5ans_3eme,0) + COALESCE(e.effectif_filles_plus_5ans_3eme,0)
        ) AS total_general,

        -- NR - Total (régime de gestion vide)
        SUM(CASE WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN 
            COALESCE(e.effectif_garcons_moins_3ans_1ere,0) + COALESCE(e.effectif_filles_moins_3ans_1ere,0) +
            COALESCE(e.effectif_garcons_moins_3ans_2eme,0) + COALESCE(e.effectif_filles_moins_3ans_2eme,0) +
            COALESCE(e.effectif_garcons_moins_3ans_3eme,0) + COALESCE(e.effectif_filles_moins_3ans_3eme,0) +
            COALESCE(e.effectif_garcons_3ans_1ere,0) + COALESCE(e.effectif_filles_3ans_1ere,0) +
            COALESCE(e.effectif_garcons_3ans_2eme,0) + COALESCE(e.effectif_filles_3ans_2eme,0) +
            COALESCE(e.effectif_garcons_3ans_3eme,0) + COALESCE(e.effectif_filles_3ans_3eme,0) +
            COALESCE(e.effectif_garcons_4ans_1ere,0) + COALESCE(e.effectif_filles_4ans_1ere,0) +
            COALESCE(e.effectif_garcons_4ans_2eme,0) + COALESCE(e.effectif_filles_4ans_2eme,0) +
            COALESCE(e.effectif_garcons_4ans_3eme,0) + COALESCE(e.effectif_filles_4ans_3eme,0) +
            COALESCE(e.effectif_garcons_5ans_1ere,0) + COALESCE(e.effectif_filles_5ans_1ere,0) +
            COALESCE(e.effectif_garcons_5ans_2eme,0) + COALESCE(e.effectif_filles_5ans_2eme,0) +
            COALESCE(e.effectif_garcons_5ans_3eme,0) + COALESCE(e.effectif_filles_5ans_3eme,0) +
            COALESCE(e.effectif_garcons_plus_5ans_1ere,0) + COALESCE(e.effectif_filles_plus_5ans_1ere,0) +
            COALESCE(e.effectif_garcons_plus_5ans_2eme,0) + COALESCE(e.effectif_filles_plus_5ans_2eme,0) +
            COALESCE(e.effectif_garcons_plus_5ans_3eme,0) + COALESCE(e.effectif_filles_plus_5ans_3eme,0)
        ELSE 0 END) AS NR

    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON p.id = i.fk_province_id
    LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
    WHERE {where_clause}
    GROUP BY p.id, p.libelle, f.idannee

    ORDER BY idannee, id, 
             CASE WHEN sexe = 'Garçons' THEN 1 
                  WHEN sexe = 'Filles' THEN 2 
                  ELSE 3 END;
    """

def get_effectifs_par_age_sexe_query(where_clause):
    return f"""
    SELECT 
        '1ère Maternelle' AS Niveau,
        'Garçons' AS sexe,
        f.idannee,
        -- 👦 Garçons - Répartition par âge
        SUM(COALESCE(e.effectif_garcons_moins_3ans_1ere, 0)) AS "-3ans",
        SUM(COALESCE(e.effectif_garcons_3ans_1ere, 0)) AS "3ans",
        SUM(COALESCE(e.effectif_garcons_4ans_1ere, 0)) AS "4ans",
        SUM(COALESCE(e.effectif_garcons_5ans_1ere, 0)) AS "5ans",
        SUM(COALESCE(e.effectif_garcons_plus_5ans_1ere, 0)) AS "6ans",
        -- Total 1ère Maternelle
        SUM(COALESCE(e.effectif_garcons_moins_3ans_1ere,0) + COALESCE(e.effectif_garcons_3ans_1ere,0) +
            COALESCE(e.effectif_garcons_4ans_1ere,0) + COALESCE(e.effectif_garcons_5ans_1ere,0) +
            COALESCE(e.effectif_garcons_plus_5ans_1ere,0)) AS "Total général"

    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
    WHERE {where_clause}
    GROUP BY f.idannee

    UNION ALL

    SELECT 
        '2ème Maternelle' AS Niveau,
        'Garçons' AS sexe,
        f.idannee,
        -- 👦 Garçons - Répartition par âge
        SUM(COALESCE(e.effectif_garcons_moins_3ans_2eme, 0)) AS "-3ans",
        SUM(COALESCE(e.effectif_garcons_3ans_2eme, 0)) AS "3ans",
        SUM(COALESCE(e.effectif_garcons_4ans_2eme, 0)) AS "4ans",
        SUM(COALESCE(e.effectif_garcons_5ans_2eme, 0)) AS "5ans",
        SUM(COALESCE(e.effectif_garcons_plus_5ans_2eme, 0)) AS "6ans",
        -- Total 2ème Maternelle
        SUM(COALESCE(e.effectif_garcons_moins_3ans_2eme,0) + COALESCE(e.effectif_garcons_3ans_2eme,0) +
            COALESCE(e.effectif_garcons_4ans_2eme,0) + COALESCE(e.effectif_garcons_5ans_2eme,0) +
            COALESCE(e.effectif_garcons_plus_5ans_2eme,0)) AS "Total général"

    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
    WHERE {where_clause}
    GROUP BY f.idannee

    UNION ALL

    SELECT 
        '3ème Maternelle' AS Niveau,
        'Garçons' AS sexe,
        f.idannee,
        -- 👦 Garçons - Répartition par âge
        SUM(COALESCE(e.effectif_garcons_moins_3ans_3eme, 0)) AS "-3ans",
        SUM(COALESCE(e.effectif_garcons_3ans_3eme, 0)) AS "3ans",
        SUM(COALESCE(e.effectif_garcons_4ans_3eme, 0)) AS "4ans",
        SUM(COALESCE(e.effectif_garcons_5ans_3eme, 0)) AS "5ans",
        SUM(COALESCE(e.effectif_garcons_plus_5ans_3eme, 0)) AS "6ans",
        -- Total 3ème Maternelle
        SUM(COALESCE(e.effectif_garcons_moins_3ans_3eme,0) + COALESCE(e.effectif_garcons_3ans_3eme,0) +
            COALESCE(e.effectif_garcons_4ans_3eme,0) + COALESCE(e.effectif_garcons_5ans_3eme,0) +
            COALESCE(e.effectif_garcons_plus_5ans_3eme,0)) AS "Total général"

    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
    WHERE {where_clause}
    GROUP BY f.idannee

    UNION ALL

    SELECT 
        '1ère Maternelle' AS Niveau,
        'Filles' AS sexe,
        f.idannee,
        -- 👧 Filles - Répartition par âge
        SUM(COALESCE(e.effectif_filles_moins_3ans_1ere, 0)) AS "-3ans",
        SUM(COALESCE(e.effectif_filles_3ans_1ere, 0)) AS "3ans",
        SUM(COALESCE(e.effectif_filles_4ans_1ere, 0)) AS "4ans",
        SUM(COALESCE(e.effectif_filles_5ans_1ere, 0)) AS "5ans",
        SUM(COALESCE(e.effectif_filles_plus_5ans_1ere, 0)) AS "6ans",
        -- Total 1ère Maternelle
        SUM(COALESCE(e.effectif_filles_moins_3ans_1ere,0) + COALESCE(e.effectif_filles_3ans_1ere,0) +
            COALESCE(e.effectif_filles_4ans_1ere,0) + COALESCE(e.effectif_filles_5ans_1ere,0) +
            COALESCE(e.effectif_filles_plus_5ans_1ere,0)) AS "Total général"

    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
    WHERE {where_clause}
    GROUP BY f.idannee

    UNION ALL

    SELECT 
        '2ème Maternelle' AS Niveau,
        'Filles' AS sexe,
        f.idannee,
        -- 👧 Filles - Répartition par âge
        SUM(COALESCE(e.effectif_filles_moins_3ans_2eme, 0)) AS "-3ans",
        SUM(COALESCE(e.effectif_filles_3ans_2eme, 0)) AS "3ans",
        SUM(COALESCE(e.effectif_filles_4ans_2eme, 0)) AS "4ans",
        SUM(COALESCE(e.effectif_filles_5ans_2eme, 0)) AS "5ans",
        SUM(COALESCE(e.effectif_filles_plus_5ans_2eme, 0)) AS "6ans",
        -- Total 2ème Maternelle
        SUM(COALESCE(e.effectif_filles_moins_3ans_2eme,0) + COALESCE(e.effectif_filles_3ans_2eme,0) +
            COALESCE(e.effectif_filles_4ans_2eme,0) + COALESCE(e.effectif_filles_5ans_2eme,0) +
            COALESCE(e.effectif_filles_plus_5ans_2eme,0)) AS "Total général"

    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
    WHERE {where_clause}
    GROUP BY f.idannee

    UNION ALL

    SELECT 
        '3ème Maternelle' AS Niveau,
        'Filles' AS sexe,
        f.idannee,
        -- 👧 Filles - Répartition par âge
        SUM(COALESCE(e.effectif_filles_moins_3ans_3eme, 0)) AS "-3ans",
        SUM(COALESCE(e.effectif_filles_3ans_3eme, 0)) AS "3ans",
        SUM(COALESCE(e.effectif_filles_4ans_3eme, 0)) AS "4ans",
        SUM(COALESCE(e.effectif_filles_5ans_3eme, 0)) AS "5ans",
        SUM(COALESCE(e.effectif_filles_plus_5ans_3eme, 0)) AS "6ans",
        -- Total 3ème Maternelle
        SUM(COALESCE(e.effectif_filles_moins_3ans_3eme,0) + COALESCE(e.effectif_filles_3ans_3eme,0) +
            COALESCE(e.effectif_filles_4ans_3eme,0) + COALESCE(e.effectif_filles_5ans_3eme,0) +
            COALESCE(e.effectif_filles_plus_5ans_3eme,0)) AS "Total général"

    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
    WHERE {where_clause}
    GROUP BY f.idannee

    UNION ALL

    SELECT 
        '1ère Maternelle' AS Niveau,
        'Total' AS sexe,
        f.idannee,
        -- 👨‍👩‍👧‍👦 Total - Répartition par âge
        SUM(COALESCE(e.effectif_garcons_moins_3ans_1ere, 0) + COALESCE(e.effectif_filles_moins_3ans_1ere, 0)) AS "-3ans",
        SUM(COALESCE(e.effectif_garcons_3ans_1ere, 0) + COALESCE(e.effectif_filles_3ans_1ere, 0)) AS "3ans",
        SUM(COALESCE(e.effectif_garcons_4ans_1ere, 0) + COALESCE(e.effectif_filles_4ans_1ere, 0)) AS "4ans",
        SUM(COALESCE(e.effectif_garcons_5ans_1ere, 0) + COALESCE(e.effectif_filles_5ans_1ere, 0)) AS "5ans",
        SUM(COALESCE(e.effectif_garcons_plus_5ans_1ere, 0) + COALESCE(e.effectif_filles_plus_5ans_1ere, 0)) AS "6ans",
        -- Total 1ère Maternelle
        SUM(COALESCE(e.effectif_garcons_moins_3ans_1ere,0) + COALESCE(e.effectif_filles_moins_3ans_1ere,0) +
            COALESCE(e.effectif_garcons_3ans_1ere,0) + COALESCE(e.effectif_filles_3ans_1ere,0) +
            COALESCE(e.effectif_garcons_4ans_1ere,0) + COALESCE(e.effectif_filles_4ans_1ere,0) +
            COALESCE(e.effectif_garcons_5ans_1ere,0) + COALESCE(e.effectif_filles_5ans_1ere,0) +
            COALESCE(e.effectif_garcons_plus_5ans_1ere,0) + COALESCE(e.effectif_filles_plus_5ans_1ere,0)) AS "Total général"

    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
    WHERE {where_clause}
    GROUP BY f.idannee

    UNION ALL

    SELECT 
        '2ème Maternelle' AS Niveau,
        'Total' AS sexe,
        f.idannee,
        -- 👨‍👩‍👧‍👦 Total - Répartition par âge
        SUM(COALESCE(e.effectif_garcons_moins_3ans_2eme, 0) + COALESCE(e.effectif_filles_moins_3ans_2eme, 0)) AS "-3ans",
        SUM(COALESCE(e.effectif_garcons_3ans_2eme, 0) + COALESCE(e.effectif_filles_3ans_2eme, 0)) AS "3ans",
        SUM(COALESCE(e.effectif_garcons_4ans_2eme, 0) + COALESCE(e.effectif_filles_4ans_2eme, 0)) AS "4ans",
        SUM(COALESCE(e.effectif_garcons_5ans_2eme, 0) + COALESCE(e.effectif_filles_5ans_2eme, 0)) AS "5ans",
        SUM(COALESCE(e.effectif_garcons_plus_5ans_2eme, 0) + COALESCE(e.effectif_filles_plus_5ans_2eme, 0)) AS "6ans",
        -- Total 2ème Maternelle
        SUM(COALESCE(e.effectif_garcons_moins_3ans_2eme,0) + COALESCE(e.effectif_filles_moins_3ans_2eme,0) +
            COALESCE(e.effectif_garcons_3ans_2eme,0) + COALESCE(e.effectif_filles_3ans_2eme,0) +
            COALESCE(e.effectif_garcons_4ans_2eme,0) + COALESCE(e.effectif_filles_4ans_2eme,0) +
            COALESCE(e.effectif_garcons_5ans_2eme,0) + COALESCE(e.effectif_filles_5ans_2eme,0) +
            COALESCE(e.effectif_garcons_plus_5ans_2eme,0) + COALESCE(e.effectif_filles_plus_5ans_2eme,0)) AS "Total général"

    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
    WHERE {where_clause}
    GROUP BY f.idannee

    UNION ALL

    SELECT 
        '3ème Maternelle' AS Niveau,
        'Total' AS sexe,
        f.idannee,
        -- 👨‍👩‍👧‍👦 Total - Répartition par âge
        SUM(COALESCE(e.effectif_garcons_moins_3ans_3eme, 0) + COALESCE(e.effectif_filles_moins_3ans_3eme, 0)) AS "-3ans",
        SUM(COALESCE(e.effectif_garcons_3ans_3eme, 0) + COALESCE(e.effectif_filles_3ans_3eme, 0)) AS "3ans",
        SUM(COALESCE(e.effectif_garcons_4ans_3eme, 0) + COALESCE(e.effectif_filles_4ans_3eme, 0)) AS "4ans",
        SUM(COALESCE(e.effectif_garcons_5ans_3eme, 0) + COALESCE(e.effectif_filles_5ans_3eme, 0)) AS "5ans",
        SUM(COALESCE(e.effectif_garcons_plus_5ans_3eme, 0) + COALESCE(e.effectif_filles_plus_5ans_3eme, 0)) AS "6ans",
        -- Total 3ème Maternelle
        SUM(COALESCE(e.effectif_garcons_moins_3ans_3eme,0) + COALESCE(e.effectif_filles_moins_3ans_3eme,0) +
            COALESCE(e.effectif_garcons_3ans_3eme,0) + COALESCE(e.effectif_filles_3ans_3eme,0) +
            COALESCE(e.effectif_garcons_4ans_3eme,0) + COALESCE(e.effectif_filles_4ans_3eme,0) +
            COALESCE(e.effectif_garcons_5ans_3eme,0) + COALESCE(e.effectif_filles_5ans_3eme,0) +
            COALESCE(e.effectif_garcons_plus_5ans_3eme,0) + COALESCE(e.effectif_filles_plus_5ans_3eme,0)) AS "Total général"

    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
    WHERE {where_clause}
    GROUP BY f.idannee

    ORDER BY idannee,
             CASE WHEN Niveau = '1ère Maternelle' THEN 1 
                  WHEN Niveau = '2ème Maternelle' THEN 2 
                  WHEN Niveau = '3ème Maternelle' THEN 3 
                  ELSE 4 END,
             CASE WHEN sexe = 'Garçons' THEN 1 
                  WHEN sexe = 'Filles' THEN 2 
                  ELSE 3 END;
    """

# Fonctions de comptage pour la pagination
def get_effectifs_par_age_national_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY f.idannee, 
                 CASE WHEN '1ère Maternelle' THEN 1
                      WHEN '2ème Maternelle' THEN 2
                      WHEN '3ème Maternelle' THEN 3
                      ELSE 4 END
    ) as subquery
    """

def get_effectifs_regime_province_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM provinces p
        JOIN identifications i ON p.id = i.fk_province_id
        JOIN formulaires f ON f.identification_id = i.id
        JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY p.id, p.libelle, f.idannee, 'Garçons'
        
        UNION ALL
        
        SELECT 1
        FROM provinces p
        JOIN identifications i ON p.id = i.fk_province_id
        JOIN formulaires f ON f.identification_id = i.id
        JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY p.id, p.libelle, f.idannee, 'Filles'
    ) as subquery
    """

def get_effectifs_secteur_national_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY 
            CASE 
                WHEN UPPER(i.regime_gestion) = 'EPR' THEN 'Privé'
                WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN 'NR'
                ELSE 'Public'
            END,
            i.regime_gestion,
            f.idannee,
            'Garçons'
        
        UNION ALL
        
        SELECT 1
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY 
            CASE 
                WHEN UPPER(i.regime_gestion) = 'EPR' THEN 'Privé'
                WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN 'NR'
                ELSE 'Public'
            END,
            i.regime_gestion,
            f.idannee,
            'Filles'
            
        UNION ALL
        
        SELECT 1
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY 
            CASE 
                WHEN UPPER(i.regime_gestion) = 'EPR' THEN 'Privé'
                WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN 'NR'
                ELSE 'Public'
            END,
            i.regime_gestion,
            f.idannee,
            'Total'
    ) as subquery
    """

def get_effectifs_province_detail_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        JOIN provinces p ON p.id = i.fk_province_id
        LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY p.id, p.libelle, f.idannee, 'Garçons'
        
        UNION ALL
        
        SELECT 1
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        JOIN provinces p ON p.id = i.fk_province_id
        LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY p.id, p.libelle, f.idannee, 'Filles'
        
        UNION ALL
        
        SELECT 1
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        JOIN provinces p ON p.id = i.fk_province_id
        LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY p.id, p.libelle, f.idannee, 'Total'
    ) as subquery
    """

def get_effectifs_par_age_sexe_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY f.idannee, '1ère Maternelle', 'Garçons'
        
        UNION ALL
        
        SELECT 1
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY f.idannee, '2ème Maternelle', 'Garçons'
        
        UNION ALL
        
        SELECT 1
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY f.idannee, '3ème Maternelle', 'Garçons'
        
        UNION ALL
        
        SELECT 1
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY f.idannee, '1ère Maternelle', 'Filles'
        
        UNION ALL
        
        SELECT 1
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY f.idannee, '2ème Maternelle', 'Filles'
        
        UNION ALL
        
        SELECT 1
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY f.idannee, '3ème Maternelle', 'Filles'
        
        UNION ALL
        
        SELECT 1
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY f.idannee, '1ère Maternelle', 'Total'
        
        UNION ALL
        
        SELECT 1
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY f.idannee, '2ème Maternelle', 'Total'
        
        UNION ALL
        
        SELECT 1
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        LEFT JOIN st1_effectifs_par_age e ON e.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY f.idannee, '3ème Maternelle', 'Total'
    ) as subquery
    """

# Fonctions d'export
def export_effectifs_excel(request):
    """Export Excel des effectifs ST1"""
    try:
        rapport_type = request.GET.get('rapport_type', 'effectifs_par_age_national')
        filters = {
            'annee': request.GET.get('annee', ''),
            'province': request.GET.get('province', ''),
            'milieu': request.GET.get('milieu', ''),
            'secteur': request.GET.get('secteur', '')
        }
        
        # Construire la clause WHERE
        where_conditions = ["f.responded = 1", "UPPER(f.type) = 'ST1'"]
        params = []
        
        # Appliquer les filtres
        annee = filters.get('annee')
        if annee:
            where_conditions.append("f.idannee = %s")
            params.append(annee)
            
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
        
        # Mapping des titres
        titre_mapping = {
            'effectifs_par_age_national': "Effectifs par Âge - Vue Nationale",
            'effectifs_regime_province': "Effectifs par Régime et Province",
            'effectifs_secteur_national': "Effectifs par Secteur - Vue Nationale",
            'effectifs_province_detail': "Effectifs par Province - Détail",
            'effectifs_par_age_sexe': "Effectifs par Âge et Sexe"
        }
        
        # Sélectionner la requête
        query_mapping = {
            'effectifs_par_age_national': get_effectifs_par_age_national_query(where_clause),
            'effectifs_regime_province': get_effectifs_regime_province_query(where_clause),
            'effectifs_secteur_national': get_effectifs_secteur_national_query(where_clause),
            'effectifs_province_detail': get_effectifs_province_detail_query(where_clause),
            'effectifs_par_age_sexe': get_effectifs_par_age_sexe_query(where_clause),
        }
        
        query = query_mapping.get(rapport_type, get_effectifs_par_age_national_query(where_clause))
        title = titre_mapping.get(rapport_type, "Effectifs ST1")
        
        # Exécuter la requête
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Créer le fichier Excel
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="effectifs_st1_{rapport_type}_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.xls"'
        
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Effectifs ST1')
        
        # Styles
        header_style = xlwt.easyxf('font: bold on; align: horiz center; pattern: pattern solid, fore_color light_blue;')
        normal_style = xlwt.easyxf('align: horiz left;')
        number_style = xlwt.easyxf('align: horiz right;')
        total_style = xlwt.easyxf('font: bold on; align: horiz right; pattern: pattern solid, fore_color light_green;')
        
        # En-tête du document
        row_num = 0
        ws.write(row_num, 0, f"EFFECTIFS ST1 - {title}", header_style)
        row_num += 1
        ws.write(row_num, 0, f"Généré le: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
        row_num += 2
        
        # En-têtes des colonnes
        for col_num, column_title in enumerate(columns):
            ws.write(row_num, col_num, column_title.replace('_', ' ').title(), header_style)
            ws.col(col_num).width = 4000
        
        row_num += 1
        
        # Données
        for row in results:
            for col_num, column_title in enumerate(columns):
                value = row.get(column_title, '')
                if isinstance(value, (int, float)):
                    # Appliquer un style spécial pour les totaux
                    if 'total' in column_title.lower() or 'general' in column_title.lower():
                        ws.write(row_num, col_num, value, total_style)
                    else:
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

def export_effectifs_pdf(request):
    """Export PDF des effectifs ST1"""
    try:
        rapport_type = request.GET.get('rapport_type', 'effectifs_par_age_national')
        filters = {
            'annee': request.GET.get('annee', ''),
            'province': request.GET.get('province', ''),
            'milieu': request.GET.get('milieu', ''),
            'secteur': request.GET.get('secteur', '')
        }
        
        # Construire la clause WHERE (même logique que export_excel)
        where_conditions = ["f.responded = 1", "UPPER(f.type) = 'ST1'"]
        params = []
        
        # Appliquer les filtres
        annee = filters.get('annee')
        if annee:
            where_conditions.append("f.idannee = %s")
            params.append(annee)
            
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
        
        # Mapping des titres
        titre_mapping = {
            'effectifs_par_age_national': "Effectifs par Âge - Vue Nationale",
            'effectifs_regime_province': "Effectifs par Régime et Province",
            'effectifs_secteur_national': "Effectifs par Secteur - Vue Nationale",
            'effectifs_province_detail': "Effectifs par Province - Détail",
            'effectifs_par_age_sexe': "Effectifs par Âge et Sexe"
        }
        
        # Sélectionner la requête
        query_mapping = {
            'effectifs_par_age_national': get_effectifs_par_age_national_query(where_clause),
            'effectifs_regime_province': get_effectifs_regime_province_query(where_clause),
            'effectifs_secteur_national': get_effectifs_secteur_national_query(where_clause),
            'effectifs_province_detail': get_effectifs_province_detail_query(where_clause),
            'effectifs_par_age_sexe': get_effectifs_par_age_sexe_query(where_clause),
        }
        
        query = query_mapping.get(rapport_type, get_effectifs_par_age_national_query(where_clause))
        title = titre_mapping.get(rapport_type, "Effectifs ST1")
        
        # Exécuter la requête
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Créer le PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="effectifs_st1_{rapport_type}_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.pdf"'
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        elements = []
        
        styles = getSampleStyleSheet()
        
        # Titre
        title_text = f"EFFECTIFS ST1 - {title}"
        elements.append(Paragraph(title_text, styles['Title']))
        
        # Date de génération
        date_text = f"Généré le: {datetime.datetime.now().strftime('%d/%m/%Y à %H:%M')}"
        elements.append(Paragraph(date_text, styles['Normal']))
        
        # Filtres appliqués
        filters_text = "Filtres appliqués: "
        filters_list = []
        if filters['annee']:
            filters_list.append(f"Année: {filters['annee']}")
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

def export_effectifs_csv(request):
    """Export CSV des effectifs ST1"""
    try:
        rapport_type = request.GET.get('rapport_type', 'effectifs_par_age_national')
        filters = {
            'annee': request.GET.get('annee', ''),
            'province': request.GET.get('province', ''),
            'milieu': request.GET.get('milieu', ''),
            'secteur': request.GET.get('secteur', '')
        }
        
        # Construire la clause WHERE (même logique que export_excel)
        where_conditions = ["f.responded = 1", "UPPER(f.type) = 'ST1'"]
        params = []
        
        # Appliquer les filtres
        annee = filters.get('annee')
        if annee:
            where_conditions.append("f.idannee = %s")
            params.append(annee)
            
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
        
        # Mapping des titres
        titre_mapping = {
            'effectifs_par_age_national': "Effectifs par Âge - Vue Nationale",
            'effectifs_regime_province': "Effectifs par Régime et Province",
            'effectifs_secteur_national': "Effectifs par Secteur - Vue Nationale",
            'effectifs_province_detail': "Effectifs par Province - Détail",
            'effectifs_par_age_sexe': "Effectifs par Âge et Sexe"
        }
        
        # Sélectionner la requête
        query_mapping = {
            'effectifs_par_age_national': get_effectifs_par_age_national_query(where_clause),
            'effectifs_regime_province': get_effectifs_regime_province_query(where_clause),
            'effectifs_secteur_national': get_effectifs_secteur_national_query(where_clause),
            'effectifs_province_detail': get_effectifs_province_detail_query(where_clause),
            'effectifs_par_age_sexe': get_effectifs_par_age_sexe_query(where_clause),
        }
        
        query = query_mapping.get(rapport_type, get_effectifs_par_age_national_query(where_clause))
        title = titre_mapping.get(rapport_type, "Effectifs ST1")
        
        # Exécuter la requête
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Créer le CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="effectifs_st1_{rapport_type}_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.csv"'
        
        response.write(u'\ufeff'.encode('utf8'))  # BOM pour Excel
        writer = csv.writer(response)
        
        # En-tête
        writer.writerow([f"EFFECTIFS ST1 - {title}"])
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

# Fonctions utilitaires pour les filtres
def get_annees_scolaires():
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT idannee FROM formulaires WHERE responded = 1 AND UPPER(type) = 'ST1' ORDER BY idannee DESC")
        return [row[0] for row in cursor.fetchall()]

def get_provinces():
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, libelle FROM provinces ORDER BY libelle")
        return [{'id': row[0], 'libelle': row[1]} for row in cursor.fetchall()]

def get_types_enseignement():
    return ['ST1']  # Spécifique aux effectifs ST1

def get_milieux():
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











# ENSEIGNANTS
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

def annuaire_enseignants(request):
    """Vue principale pour l'annuaire des enseignants"""
    context = {
        'annees_scolaires': get_annees_scolaires(),
        'provinces': get_provinces(),
        'types_enseignement': get_types_enseignement(),
        'milieux': get_milieux(),
    }
    return render(request, 'annuaires/annuaire_enseignants.html', context)

@csrf_exempt
def get_enseignants_data(request):
    """Endpoint AJAX pour récupérer les données des enseignants avec pagination"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rapport_type = data.get('rapport_type')
            filters = data.get('filters', {})
            page = int(data.get('page', 1))
            page_size = int(data.get('page_size', 10))
            
            # Calculer l'offset pour la pagination
            offset = (page - 1) * page_size
            
            # Appliquer TOUS les filtres
            where_conditions = ["f.responded = 1", "UPPER(f.type) = 'ST1'"]
            params = []
            
            # Filtre année scolaire
            annee = filters.get('annee')
            if annee:
                where_conditions.append("f.idannee = %s")
                params.append(annee)
                
            # Filtre province
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
            
            # Sélectionner la requête en fonction du type de rapport
            if rapport_type == 'effectif_milieu_province':
                query = get_effectif_milieu_province_query(where_clause, page_size, offset)
                count_query = get_effectif_milieu_province_count_query(where_clause)
            elif rapport_type == 'effectif_regime_province':
                query = get_effectif_regime_province_query(where_clause, page_size, offset)
                count_query = get_effectif_regime_province_count_query(where_clause)
            elif rapport_type == 'niveau_formation_province':
                query = get_niveau_formation_province_query(where_clause, page_size, offset)
                count_query = get_niveau_formation_province_count_query(where_clause)
            elif rapport_type == 'niveau_formation_national':
                query = get_niveau_formation_national_query(where_clause, page_size, offset)
                count_query = get_niveau_formation_national_count_query(where_clause)
            elif rapport_type == 'diplome_niveau_maternelle':
                query = get_diplome_niveau_maternelle_query(where_clause, page_size, offset)
                count_query = get_diplome_niveau_maternelle_count_query(where_clause)
            elif rapport_type == 'effectif_regime_sexe_province':
                query = get_effectif_regime_sexe_province_query(where_clause, page_size, offset)
                count_query = get_effectif_regime_sexe_province_count_query(where_clause)
            elif rapport_type == 'effectif_regime_province_simple':
                query = get_effectif_regime_province_simple_query(where_clause, page_size, offset)
                count_query = get_effectif_regime_province_simple_count_query(where_clause)
            elif rapport_type == 'effectif_milieu_public_province':
                query = get_effectif_milieu_public_province_query(where_clause, page_size, offset)
                count_query = get_effectif_milieu_public_province_count_query(where_clause)
            elif rapport_type == 'pourcentage_niveau_national':
                query = get_pourcentage_niveau_national_query(where_clause, page_size, offset)
                count_query = get_pourcentage_niveau_national_count_query(where_clause)
            else:
                query = get_normal_enseignants_query(where_clause, page_size, offset)
                count_query = get_normal_enseignants_count_query(where_clause)
            
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

def export_enseignants_excel(request):
    """Export Excel des données enseignants"""
    try:
        rapport_type = request.GET.get('rapport_type', 'normal')
        filters = {
            'annee': request.GET.get('annee', ''),
            'province': request.GET.get('province', ''),
            'milieu': request.GET.get('milieu', ''),
            'secteur': request.GET.get('secteur', '')
        }
        
        # Récupérer les données
        where_conditions = ["f.responded = 1", "UPPER(f.type) = 'ST1'"]
        params = []
        
        # Appliquer les mêmes filtres
        annee = filters.get('annee')
        if annee:
            where_conditions.append("f.idannee = %s")
            params.append(annee)
            
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
        if rapport_type == 'effectif_milieu_province':
            query = get_effectif_milieu_province_query(where_clause)
            title = "Effectif par Milieu et Province"
        elif rapport_type == 'effectif_regime_province':
            query = get_effectif_regime_province_query(where_clause)
            title = "Effectif par Régime et Province"
        elif rapport_type == 'niveau_formation_province':
            query = get_niveau_formation_province_query(where_clause)
            title = "Niveau de Formation par Province"
        elif rapport_type == 'niveau_formation_national':
            query = get_niveau_formation_national_query(where_clause)
            title = "Niveau de Formation National"
        elif rapport_type == 'diplome_niveau_maternelle':
            query = get_diplome_niveau_maternelle_query(where_clause)
            title = "Diplôme par Niveau Maternelle"
        elif rapport_type == 'effectif_regime_sexe_province':
            query = get_effectif_regime_sexe_province_query(where_clause)
            title = "Effectif par Régime et Sexe par Province"
        elif rapport_type == 'effectif_regime_province_simple':
            query = get_effectif_regime_province_simple_query(where_clause)
            title = "Effectif par Régime et Province (Simple)"
        elif rapport_type == 'effectif_milieu_public_province':
            query = get_effectif_milieu_public_province_query(where_clause)
            title = "Effectif par Milieu Public par Province"
        elif rapport_type == 'pourcentage_niveau_national':
            query = get_pourcentage_niveau_national_query(where_clause)
            title = "Pourcentage par Niveau de Formation National"
        else:
            query = get_normal_enseignants_query(where_clause)
            title = "Liste des Enseignants"
        
        # Exécuter la requête
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Créer le fichier Excel
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="enseignants_{rapport_type}_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.xls"'
        
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Enseignants')
        
        # Styles
        header_style = xlwt.easyxf('font: bold on; align: horiz center; pattern: pattern solid, fore_color light_blue;')
        normal_style = xlwt.easyxf('align: horiz left;')
        number_style = xlwt.easyxf('align: horiz right;')
        
        # En-tête du document
        row_num = 0
        ws.write(row_num, 0, f"RAPPORT DES ENSEIGNANTS - {title}", header_style)
        row_num += 1
        ws.write(row_num, 0, f"Généré le: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
        row_num += 2
        
        # En-têtes des colonnes
        for col_num, column_title in enumerate(columns):
            ws.write(row_num, col_num, column_title.replace('_', ' ').title(), header_style)
            ws.col(col_num).width = 4000
        
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

def export_enseignants_pdf(request):
    """Export PDF des données enseignants"""
    try:
        rapport_type = request.GET.get('rapport_type', 'normal')
        filters = {
            'annee': request.GET.get('annee', ''),
            'province': request.GET.get('province', ''),
            'milieu': request.GET.get('milieu', ''),
            'secteur': request.GET.get('secteur', '')
        }
        
        # Récupérer les données
        where_conditions = ["f.responded = 1", "UPPER(f.type) = 'ST1'"]
        params = []
        
        # Appliquer les filtres
        annee = filters.get('annee')
        if annee:
            where_conditions.append("f.idannee = %s")
            params.append(annee)
            
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
        if rapport_type == 'effectif_milieu_province':
            query = get_effectif_milieu_province_query(where_clause)
            title = "Effectif par Milieu et Province"
        elif rapport_type == 'effectif_regime_province':
            query = get_effectif_regime_province_query(where_clause)
            title = "Effectif par Régime et Province"
        elif rapport_type == 'niveau_formation_province':
            query = get_niveau_formation_province_query(where_clause)
            title = "Niveau de Formation par Province"
        elif rapport_type == 'niveau_formation_national':
            query = get_niveau_formation_national_query(where_clause)
            title = "Niveau de Formation National"
        elif rapport_type == 'diplome_niveau_maternelle':
            query = get_diplome_niveau_maternelle_query(where_clause)
            title = "Diplôme par Niveau Maternelle"
        elif rapport_type == 'effectif_regime_sexe_province':
            query = get_effectif_regime_sexe_province_query(where_clause)
            title = "Effectif par Régime et Sexe par Province"
        elif rapport_type == 'effectif_regime_province_simple':
            query = get_effectif_regime_province_simple_query(where_clause)
            title = "Effectif par Régime et Province (Simple)"
        elif rapport_type == 'effectif_milieu_public_province':
            query = get_effectif_milieu_public_province_query(where_clause)
            title = "Effectif par Milieu Public par Province"
        elif rapport_type == 'pourcentage_niveau_national':
            query = get_pourcentage_niveau_national_query(where_clause)
            title = "Pourcentage par Niveau de Formation National"
        else:
            query = get_normal_enseignants_query(where_clause)
            title = "Liste des Enseignants"
        
        # Exécuter la requête
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Créer le PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="enseignants_{rapport_type}_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.pdf"'
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        elements = []
        
        styles = getSampleStyleSheet()
        
        # Titre
        title_text = f"RAPPORT DES ENSEIGNANTS - {title}"
        elements.append(Paragraph(title_text, styles['Title']))
        
        # Date de génération
        date_text = f"Généré le: {datetime.datetime.now().strftime('%d/%m/%Y à %H:%M')}"
        elements.append(Paragraph(date_text, styles['Normal']))
        
        # Filtres appliqués
        filters_text = "Filtres appliqués: "
        filters_list = []
        if filters['annee']:
            filters_list.append(f"Année: {filters['annee']}")
        if filters['province']:
            filters_list.append(f"Province: {filters['province']}")
        if filters['milieu']:
            filters_list.append(f"Milieu: {filters['milieu']}")
        if filters['secteur']:
            filters_list.append(f"Secteur: {filters['secteur']}")
        
        if filters_list:
            filters_text += " | ".join(filters_list)
            elements.append(Paragraph(filters_text, styles['Normal']))
        
        elements.append(Paragraph(" ", styles['Normal']))
        
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

def export_enseignants_csv(request):
    """Export CSV des données enseignants"""
    try:
        rapport_type = request.GET.get('rapport_type', 'normal')
        filters = {
            'annee': request.GET.get('annee', ''),
            'province': request.GET.get('province', ''),
            'milieu': request.GET.get('milieu', ''),
            'secteur': request.GET.get('secteur', '')
        }
        
        # Récupérer les données
        where_conditions = ["f.responded = 1", "UPPER(f.type) = 'ST1'"]
        params = []
        
        # Appliquer les filtres
        annee = filters.get('annee')
        if annee:
            where_conditions.append("f.idannee = %s")
            params.append(annee)
            
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
        if rapport_type == 'effectif_milieu_province':
            query = get_effectif_milieu_province_query(where_clause)
            title = "Effectif par Milieu et Province"
        elif rapport_type == 'effectif_regime_province':
            query = get_effectif_regime_province_query(where_clause)
            title = "Effectif par Régime et Province"
        elif rapport_type == 'niveau_formation_province':
            query = get_niveau_formation_province_query(where_clause)
            title = "Niveau de Formation par Province"
        elif rapport_type == 'niveau_formation_national':
            query = get_niveau_formation_national_query(where_clause)
            title = "Niveau de Formation National"
        elif rapport_type == 'diplome_niveau_maternelle':
            query = get_diplome_niveau_maternelle_query(where_clause)
            title = "Diplôme par Niveau Maternelle"
        elif rapport_type == 'effectif_regime_sexe_province':
            query = get_effectif_regime_sexe_province_query(where_clause)
            title = "Effectif par Régime et Sexe par Province"
        elif rapport_type == 'effectif_regime_province_simple':
            query = get_effectif_regime_province_simple_query(where_clause)
            title = "Effectif par Régime et Province (Simple)"
        elif rapport_type == 'effectif_milieu_public_province':
            query = get_effectif_milieu_public_province_query(where_clause)
            title = "Effectif par Milieu Public par Province"
        elif rapport_type == 'pourcentage_niveau_national':
            query = get_pourcentage_niveau_national_query(where_clause)
            title = "Pourcentage par Niveau de Formation National"
        else:
            query = get_normal_enseignants_query(where_clause)
            title = "Liste des Enseignants"
        
        # Exécuter la requête
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Créer le CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="enseignants_{rapport_type}_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.csv"'
        
        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response)
        
        # En-tête
        writer.writerow([f"RAPPORT DES ENSEIGNANTS - {title}"])
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

# Fonctions pour les différentes requêtes enseignants
def get_effectif_milieu_province_query(where_clause, page_size=None, offset=0):
    limit_clause = f" LIMIT {page_size} OFFSET {offset}" if page_size else ""
    return f"""
    SELECT
        p.id AS "id",
        p.libelle AS "province",
        idannee,
        SUM(CASE WHEN UPPER(i.milieu) = 'URBAIN' THEN total_niveau ELSE 0 END) AS "Urbain",
        SUM(CASE WHEN UPPER(i.milieu) = 'RURAL' THEN total_niveau ELSE 0 END) AS "Rural",
        SUM(CASE WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN total_niveau ELSE 0 END) AS "NR",
        SUM(CASE WHEN UPPER(i.milieu) = 'URBAIN' THEN total_niveau ELSE 0 END) +
        SUM(CASE WHEN UPPER(i.milieu) = 'RURAL' THEN total_niveau ELSE 0 END) +
        SUM(CASE WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN total_niveau ELSE 0 END) AS "Total Général"
    FROM (
        SELECT
            f.id,
            f.idannee,
            f.identification_id,
            COALESCE(e.enseignants_d4_hommes_1ere,0) + COALESCE(e.enseignants_d4_hommes_2eme,0) + COALESCE(e.enseignants_d4_hommes_3eme,0) +
            COALESCE(e.enseignants_d4_femmes_1ere,0) + COALESCE(e.enseignants_d4_femmes_2eme,0) + COALESCE(e.enseignants_d4_femmes_3eme,0) +
            COALESCE(e.enseignants_em_hommes_1ere,0) + COALESCE(e.enseignants_em_hommes_2eme,0) + COALESCE(e.enseignants_em_hommes_3eme,0) +
            COALESCE(e.enseignants_em_femmes_1ere,0) + COALESCE(e.enseignants_em_femmes_2eme,0) + COALESCE(e.enseignants_em_femmes_3eme,0) +
            COALESCE(e.enseignants_d4p_hommes_1ere,0) + COALESCE(e.enseignants_d4p_hommes_2eme,0) + COALESCE(e.enseignants_d4p_hommes_3eme,0) +
            COALESCE(e.enseignants_d4p_femmes_1ere,0) + COALESCE(e.enseignants_d4p_femmes_2eme,0) + COALESCE(e.enseignants_d4p_femmes_3eme,0) +
            COALESCE(e.enseignants_p6_hommes_1ere,0) + COALESCE(e.enseignants_p6_hommes_2eme,0) + COALESCE(e.enseignants_p6_hommes_3eme,0) +
            COALESCE(e.enseignants_p6_femmes_1ere,0) + COALESCE(e.enseignants_p6_femmes_2eme,0) + COALESCE(e.enseignants_p6_femmes_3eme,0) +
            COALESCE(e.enseignants_d6_hommes_1ere,0) + COALESCE(e.enseignants_d6_hommes_2eme,0) + COALESCE(e.enseignants_d6_hommes_3eme,0) +
            COALESCE(e.enseignants_d6_femmes_1ere,0) + COALESCE(e.enseignants_d6_femmes_2eme,0) + COALESCE(e.enseignants_d6_femmes_3eme,0) +
            COALESCE(e.enseignants_autres_hommes_1ere,0) + COALESCE(e.enseignants_autres_hommes_2eme,0) + COALESCE(e.enseignants_autres_hommes_3eme,0) +
            COALESCE(e.enseignants_autres_femmes_1ere,0) + COALESCE(e.enseignants_autres_femmes_2eme,0) + COALESCE(e.enseignants_autres_femmes_3eme,0) AS total_niveau
        FROM formulaires f
        LEFT JOIN st1_enseignant e ON e.form_st_id = f.id
        WHERE {where_clause}
    ) AS aggregated_data
    JOIN identifications i ON aggregated_data.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    GROUP BY p.id, p.libelle, idannee
    ORDER BY p.id, idannee
    {limit_clause};
    """

def get_effectif_regime_province_query(where_clause, page_size=None, offset=0):
    limit_clause = f" LIMIT {page_size} OFFSET {offset}" if page_size else ""
    return f"""
    SELECT
        p.id AS "id",
        p.libelle AS "province",
        idannee,
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ECC' THEN total_niveau ELSE 0 END) AS "ECC",
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ECF' THEN total_niveau ELSE 0 END) AS "ECF",
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ECI' THEN total_niveau ELSE 0 END) AS "ECI",
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ECK' THEN total_niveau ELSE 0 END) AS "ECK",
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ECP' THEN total_niveau ELSE 0 END) AS "ECP",
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ECS' THEN total_niveau ELSE 0 END) AS "ECS",
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ENC' THEN total_niveau ELSE 0 END) AS "ENC",
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'AUTRES' THEN total_niveau ELSE 0 END) AS "AUTRES",
        SUM(CASE WHEN UPPER(i.regime_gestion) != 'EPR' AND i.regime_gestion IS NOT NULL AND i.regime_gestion != '' THEN total_niveau ELSE 0 END) AS "Public",
        SUM(CASE WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN total_niveau ELSE 0 END) AS "NR"
    FROM (
        SELECT
            f.id,
            f.idannee,
            f.identification_id,
            COALESCE(e.enseignants_d4_hommes_1ere,0) + COALESCE(e.enseignants_d4_hommes_2eme,0) + COALESCE(e.enseignants_d4_hommes_3eme,0) +
            COALESCE(e.enseignants_d4_femmes_1ere,0) + COALESCE(e.enseignants_d4_femmes_2eme,0) + COALESCE(e.enseignants_d4_femmes_3eme,0) +
            COALESCE(e.enseignants_em_hommes_1ere,0) + COALESCE(e.enseignants_em_hommes_2eme,0) + COALESCE(e.enseignants_em_hommes_3eme,0) +
            COALESCE(e.enseignants_em_femmes_1ere,0) + COALESCE(e.enseignants_em_femmes_2eme,0) + COALESCE(e.enseignants_em_femmes_3eme,0) +
            COALESCE(e.enseignants_d4p_hommes_1ere,0) + COALESCE(e.enseignants_d4p_hommes_2eme,0) + COALESCE(e.enseignants_d4p_hommes_3eme,0) +
            COALESCE(e.enseignants_d4p_femmes_1ere,0) + COALESCE(e.enseignants_d4p_femmes_2eme,0) + COALESCE(e.enseignants_d4p_femmes_3eme,0) +
            COALESCE(e.enseignants_p6_hommes_1ere,0) + COALESCE(e.enseignants_p6_hommes_2eme,0) + COALESCE(e.enseignants_p6_hommes_3eme,0) +
            COALESCE(e.enseignants_p6_femmes_1ere,0) + COALESCE(e.enseignants_p6_femmes_2eme,0) + COALESCE(e.enseignants_p6_femmes_3eme,0) +
            COALESCE(e.enseignants_d6_hommes_1ere,0) + COALESCE(e.enseignants_d6_hommes_2eme,0) + COALESCE(e.enseignants_d6_hommes_3eme,0) +
            COALESCE(e.enseignants_d6_femmes_1ere,0) + COALESCE(e.enseignants_d6_femmes_2eme,0) + COALESCE(e.enseignants_d6_femmes_3eme,0) +
            COALESCE(e.enseignants_autres_hommes_1ere,0) + COALESCE(e.enseignants_autres_hommes_2eme,0) + COALESCE(e.enseignants_autres_hommes_3eme,0) +
            COALESCE(e.enseignants_autres_femmes_1ere,0) + COALESCE(e.enseignants_autres_femmes_2eme,0) + COALESCE(e.enseignants_autres_femmes_3eme,0) AS total_niveau
        FROM formulaires f
        LEFT JOIN st1_enseignant e ON e.form_st_id = f.id
        WHERE {where_clause}
    ) AS aggregated_data
    JOIN identifications i ON aggregated_data.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    GROUP BY p.id, p.libelle, idannee
    ORDER BY p.id, idannee
    {limit_clause};
    """

def get_niveau_formation_province_query(where_clause, page_size=None, offset=0):
    limit_clause = f" LIMIT {page_size} OFFSET {offset}" if page_size else ""
    return f"""
    SELECT
        p.id AS "province_id",
        p.libelle AS "province",
        sexe,
        idannee,
        SUM(D4) AS "D4",
        SUM(EM) AS "EM",
        SUM(D4P) AS "D4P",
        SUM(P6) AS "P6",
        SUM(D6) AS "D6",
        SUM(AUTRES) AS "AUTRES",
        SUM(CASE WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN total_niveau ELSE 0 END) AS "NR",
        SUM(total_niveau) AS "Total Général"
    FROM (
        SELECT
            f.id,
            f.idannee,
            f.identification_id,
            'Hommes' AS sexe,
            COALESCE(e.enseignants_d4_hommes_1ere,0) + COALESCE(e.enseignants_d4_hommes_2eme,0) + COALESCE(e.enseignants_d4_hommes_3eme,0) AS D4,
            COALESCE(e.enseignants_em_hommes_1ere,0) + COALESCE(e.enseignants_em_hommes_2eme,0) + COALESCE(e.enseignants_em_hommes_3eme,0) AS EM,
            COALESCE(e.enseignants_d4p_hommes_1ere,0) + COALESCE(e.enseignants_d4p_hommes_2eme,0) + COALESCE(e.enseignants_d4p_hommes_3eme,0) AS D4P,
            COALESCE(e.enseignants_p6_hommes_1ere,0) + COALESCE(e.enseignants_p6_hommes_2eme,0) + COALESCE(e.enseignants_p6_hommes_3eme,0) AS P6,
            COALESCE(e.enseignants_d6_hommes_1ere,0) + COALESCE(e.enseignants_d6_hommes_2eme,0) + COALESCE(e.enseignants_d6_hommes_3eme,0) AS D6,
            COALESCE(e.enseignants_autres_hommes_1ere,0) + COALESCE(e.enseignants_autres_hommes_2eme,0) + COALESCE(e.enseignants_autres_hommes_3eme,0) AS AUTRES,
            COALESCE(e.enseignants_d4_hommes_1ere,0) + COALESCE(e.enseignants_d4_hommes_2eme,0) + COALESCE(e.enseignants_d4_hommes_3eme,0) +
            COALESCE(e.enseignants_em_hommes_1ere,0) + COALESCE(e.enseignants_em_hommes_2eme,0) + COALESCE(e.enseignants_em_hommes_3eme,0) +
            COALESCE(e.enseignants_d4p_hommes_1ere,0) + COALESCE(e.enseignants_d4p_hommes_2eme,0) + COALESCE(e.enseignants_d4p_hommes_3eme,0) +
            COALESCE(e.enseignants_p6_hommes_1ere,0) + COALESCE(e.enseignants_p6_hommes_2eme,0) + COALESCE(e.enseignants_p6_hommes_3eme,0) +
            COALESCE(e.enseignants_d6_hommes_1ere,0) + COALESCE(e.enseignants_d6_hommes_2eme,0) + COALESCE(e.enseignants_d6_hommes_3eme,0) +
            COALESCE(e.enseignants_autres_hommes_1ere,0) + COALESCE(e.enseignants_autres_hommes_2eme,0) + COALESCE(e.enseignants_autres_hommes_3eme,0) AS total_niveau
        FROM formulaires f
        LEFT JOIN st1_enseignant e ON e.form_st_id = f.id
        WHERE {where_clause}
        UNION ALL
        SELECT
            f.id,
            f.idannee,
            f.identification_id,
            'Femmes' AS sexe,
            COALESCE(e.enseignants_d4_femmes_1ere,0) + COALESCE(e.enseignants_d4_femmes_2eme,0) + COALESCE(e.enseignants_d4_femmes_3eme,0) AS D4,
            COALESCE(e.enseignants_em_femmes_1ere,0) + COALESCE(e.enseignants_em_femmes_2eme,0) + COALESCE(e.enseignants_em_femmes_3eme,0) AS EM,
            COALESCE(e.enseignants_d4p_femmes_1ere,0) + COALESCE(e.enseignants_d4p_femmes_2eme,0) + COALESCE(e.enseignants_d4p_femmes_3eme,0) AS D4P,
            COALESCE(e.enseignants_p6_femmes_1ere,0) + COALESCE(e.enseignants_p6_femmes_2eme,0) + COALESCE(e.enseignants_p6_femmes_3eme,0) AS P6,
            COALESCE(e.enseignants_d6_femmes_1ere,0) + COALESCE(e.enseignants_d6_femmes_2eme,0) + COALESCE(e.enseignants_d6_femmes_3eme,0) AS D6,
            COALESCE(e.enseignants_autres_femmes_1ere,0) + COALESCE(e.enseignants_autres_femmes_2eme,0) + COALESCE(e.enseignants_autres_femmes_3eme,0) AS AUTRES,
            COALESCE(e.enseignants_d4_femmes_1ere,0) + COALESCE(e.enseignants_d4_femmes_2eme,0) + COALESCE(e.enseignants_d4_femmes_3eme,0) +
            COALESCE(e.enseignants_em_femmes_1ere,0) + COALESCE(e.enseignants_em_femmes_2eme,0) + COALESCE(e.enseignants_em_femmes_3eme,0) +
            COALESCE(e.enseignants_d4p_femmes_1ere,0) + COALESCE(e.enseignants_d4p_femmes_2eme,0) + COALESCE(e.enseignants_d4p_femmes_3eme,0) +
            COALESCE(e.enseignants_p6_femmes_1ere,0) + COALESCE(e.enseignants_p6_femmes_2eme,0) + COALESCE(e.enseignants_p6_femmes_3eme,0) +
            COALESCE(e.enseignants_d6_femmes_1ere,0) + COALESCE(e.enseignants_d6_femmes_2eme,0) + COALESCE(e.enseignants_d6_femmes_3eme,0) +
            COALESCE(e.enseignants_autres_femmes_1ere,0) + COALESCE(e.enseignants_autres_femmes_2eme,0) + COALESCE(e.enseignants_autres_femmes_3eme,0) AS total_niveau
        FROM formulaires f
        LEFT JOIN st1_enseignant e ON e.form_st_id = f.id
        WHERE {where_clause}
        UNION ALL
        SELECT
            f.id,
            f.idannee,
            f.identification_id,
            'Total' AS sexe,
            COALESCE(e.enseignants_d4_hommes_1ere,0) + COALESCE(e.enseignants_d4_hommes_2eme,0) + COALESCE(e.enseignants_d4_hommes_3eme,0) +
            COALESCE(e.enseignants_d4_femmes_1ere,0) + COALESCE(e.enseignants_d4_femmes_2eme,0) + COALESCE(e.enseignants_d4_femmes_3eme,0) AS D4,
            COALESCE(e.enseignants_em_hommes_1ere,0) + COALESCE(e.enseignants_em_hommes_2eme,0) + COALESCE(e.enseignants_em_hommes_3eme,0) +
            COALESCE(e.enseignants_em_femmes_1ere,0) + COALESCE(e.enseignants_em_femmes_2eme,0) + COALESCE(e.enseignants_em_femmes_3eme,0) AS EM,
            COALESCE(e.enseignants_d4p_hommes_1ere,0) + COALESCE(e.enseignants_d4p_hommes_2eme,0) + COALESCE(e.enseignants_d4p_hommes_3eme,0) +
            COALESCE(e.enseignants_d4p_femmes_1ere,0) + COALESCE(e.enseignants_d4p_femmes_2eme,0) + COALESCE(e.enseignants_d4p_femmes_3eme,0) AS D4P,
            COALESCE(e.enseignants_p6_hommes_1ere,0) + COALESCE(e.enseignants_p6_hommes_2eme,0) + COALESCE(e.enseignants_p6_hommes_3eme,0) +
            COALESCE(e.enseignants_p6_femmes_1ere,0) + COALESCE(e.enseignants_p6_femmes_2eme,0) + COALESCE(e.enseignants_p6_femmes_3eme,0) AS P6,
            COALESCE(e.enseignants_d6_hommes_1ere,0) + COALESCE(e.enseignants_d6_hommes_2eme,0) + COALESCE(e.enseignants_d6_hommes_3eme,0) +
            COALESCE(e.enseignants_d6_femmes_1ere,0) + COALESCE(e.enseignants_d6_femmes_2eme,0) + COALESCE(e.enseignants_d6_femmes_3eme,0) AS D6,
            COALESCE(e.enseignants_autres_hommes_1ere,0) + COALESCE(e.enseignants_autres_hommes_2eme,0) + COALESCE(e.enseignants_autres_hommes_3eme,0) +
            COALESCE(e.enseignants_autres_femmes_1ere,0) + COALESCE(e.enseignants_autres_femmes_2eme,0) + COALESCE(e.enseignants_autres_femmes_3eme,0) AS AUTRES,
            COALESCE(e.enseignants_d4_hommes_1ere,0) + COALESCE(e.enseignants_d4_hommes_2eme,0) + COALESCE(e.enseignants_d4_hommes_3eme,0) +
            COALESCE(e.enseignants_d4_femmes_1ere,0) + COALESCE(e.enseignants_d4_femmes_2eme,0) + COALESCE(e.enseignants_d4_femmes_3eme,0) +
            COALESCE(e.enseignants_em_hommes_1ere,0) + COALESCE(e.enseignants_em_hommes_2eme,0) + COALESCE(e.enseignants_em_hommes_3eme,0) +
            COALESCE(e.enseignants_em_femmes_1ere,0) + COALESCE(e.enseignants_em_femmes_2eme,0) + COALESCE(e.enseignants_em_femmes_3eme,0) +
            COALESCE(e.enseignants_d4p_hommes_1ere,0) + COALESCE(e.enseignants_d4p_hommes_2eme,0) + COALESCE(e.enseignants_d4p_hommes_3eme,0) +
            COALESCE(e.enseignants_d4p_femmes_1ere,0) + COALESCE(e.enseignants_d4p_femmes_2eme,0) + COALESCE(e.enseignants_d4p_femmes_3eme,0) +
            COALESCE(e.enseignants_p6_hommes_1ere,0) + COALESCE(e.enseignants_p6_hommes_2eme,0) + COALESCE(e.enseignants_p6_hommes_3eme,0) +
            COALESCE(e.enseignants_p6_femmes_1ere,0) + COALESCE(e.enseignants_p6_femmes_2eme,0) + COALESCE(e.enseignants_p6_femmes_3eme,0) +
            COALESCE(e.enseignants_d6_hommes_1ere,0) + COALESCE(e.enseignants_d6_hommes_2eme,0) + COALESCE(e.enseignants_d6_hommes_3eme,0) +
            COALESCE(e.enseignants_d6_femmes_1ere,0) + COALESCE(e.enseignants_d6_femmes_2eme,0) + COALESCE(e.enseignants_d6_femmes_3eme,0) +
            COALESCE(e.enseignants_autres_hommes_1ere,0) + COALESCE(e.enseignants_autres_hommes_2eme,0) + COALESCE(e.enseignants_autres_hommes_3eme,0) +
            COALESCE(e.enseignants_autres_femmes_1ere,0) + COALESCE(e.enseignants_autres_femmes_2eme,0) + COALESCE(e.enseignants_autres_femmes_3eme,0) AS total_niveau
        FROM formulaires f
        LEFT JOIN st1_enseignant e ON e.form_st_id = f.id
        WHERE {where_clause}
    ) AS aggregated_data
    JOIN identifications i ON aggregated_data.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    GROUP BY p.id, p.libelle, sexe, idannee
    ORDER BY p.id, idannee, sexe
    {limit_clause};
    """

def get_niveau_formation_national_query(where_clause, page_size=None, offset=0):
    limit_clause = f" LIMIT {page_size} OFFSET {offset}" if page_size else ""
    return f"""
    SELECT 
        CASE 
            WHEN UPPER(i.regime_gestion) = 'EPR' THEN 'Privé'
            WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN 'NR'
            ELSE 'Public'
        END AS secteur,
        COALESCE(NULLIF(i.regime_gestion, ''), 'NR') AS "regime de gestion",
        sexe,
        idannee,
        SUM(D4) AS "D4",
        SUM(EM) AS "EM",
        SUM(D4P) AS "D4P",
        SUM(P6) AS "P6",
        SUM(D6) AS "D6",
        SUM(AUTRES) AS "AUTRES",
        SUM(CASE WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN total_niveau ELSE 0 END) AS "NR",
        SUM(total_niveau) AS "Total Général"
    FROM (
        SELECT 
            f.id,
            f.idannee,
            f.identification_id,
            'Hommes' AS sexe,
            COALESCE(e.enseignants_d4_hommes_1ere,0) + COALESCE(e.enseignants_d4_hommes_2eme,0) + COALESCE(e.enseignants_d4_hommes_3eme,0) AS D4,
            COALESCE(e.enseignants_em_hommes_1ere,0) + COALESCE(e.enseignants_em_hommes_2eme,0) + COALESCE(e.enseignants_em_hommes_3eme,0) AS EM,
            COALESCE(e.enseignants_d4p_hommes_1ere,0) + COALESCE(e.enseignants_d4p_hommes_2eme,0) + COALESCE(e.enseignants_d4p_hommes_3eme,0) AS D4P,
            COALESCE(e.enseignants_p6_hommes_1ere,0) + COALESCE(e.enseignants_p6_hommes_2eme,0) + COALESCE(e.enseignants_p6_hommes_3eme,0) AS P6,
            COALESCE(e.enseignants_d6_hommes_1ere,0) + COALESCE(e.enseignants_d6_hommes_2eme,0) + COALESCE(e.enseignants_d6_hommes_3eme,0) AS D6,
            COALESCE(e.enseignants_autres_hommes_1ere,0) + COALESCE(e.enseignants_autres_hommes_2eme,0) + COALESCE(e.enseignants_autres_hommes_3eme,0) AS AUTRES,
            COALESCE(e.enseignants_d4_hommes_1ere,0) + COALESCE(e.enseignants_d4_hommes_2eme,0) + COALESCE(e.enseignants_d4_hommes_3eme,0) +
            COALESCE(e.enseignants_em_hommes_1ere,0) + COALESCE(e.enseignants_em_hommes_2eme,0) + COALESCE(e.enseignants_em_hommes_3eme,0) +
            COALESCE(e.enseignants_d4p_hommes_1ere,0) + COALESCE(e.enseignants_d4p_hommes_2eme,0) + COALESCE(e.enseignants_d4p_hommes_3eme,0) +
            COALESCE(e.enseignants_p6_hommes_1ere,0) + COALESCE(e.enseignants_p6_hommes_2eme,0) + COALESCE(e.enseignants_p6_hommes_3eme,0) +
            COALESCE(e.enseignants_d6_hommes_1ere,0) + COALESCE(e.enseignants_d6_hommes_2eme,0) + COALESCE(e.enseignants_d6_hommes_3eme,0) +
            COALESCE(e.enseignants_autres_hommes_1ere,0) + COALESCE(e.enseignants_autres_hommes_2eme,0) + COALESCE(e.enseignants_autres_hommes_3eme,0) AS total_niveau
        FROM formulaires f
        LEFT JOIN st1_enseignant e ON e.form_st_id = f.id
        WHERE {where_clause}
        UNION ALL
        SELECT 
            f.id,
            f.idannee,
            f.identification_id,
            'Femmes' AS sexe,
            COALESCE(e.enseignants_d4_femmes_1ere,0) + COALESCE(e.enseignants_d4_femmes_2eme,0) + COALESCE(e.enseignants_d4_femmes_3eme,0) AS D4,
            COALESCE(e.enseignants_em_femmes_1ere,0) + COALESCE(e.enseignants_em_femmes_2eme,0) + COALESCE(e.enseignants_em_femmes_3eme,0) AS EM,
            COALESCE(e.enseignants_d4p_femmes_1ere,0) + COALESCE(e.enseignants_d4p_femmes_2eme,0) + COALESCE(e.enseignants_d4p_femmes_3eme,0) AS D4P,
            COALESCE(e.enseignants_p6_femmes_1ere,0) + COALESCE(e.enseignants_p6_femmes_2eme,0) + COALESCE(e.enseignants_p6_femmes_3eme,0) AS P6,
            COALESCE(e.enseignants_d6_femmes_1ere,0) + COALESCE(e.enseignants_d6_femmes_2eme,0) + COALESCE(e.enseignants_d6_femmes_3eme,0) AS D6,
            COALESCE(e.enseignants_autres_femmes_1ere,0) + COALESCE(e.enseignants_autres_femmes_2eme,0) + COALESCE(e.enseignants_autres_femmes_3eme,0) AS AUTRES,
            COALESCE(e.enseignants_d4_femmes_1ere,0) + COALESCE(e.enseignants_d4_femmes_2eme,0) + COALESCE(e.enseignants_d4_femmes_3eme,0) +
            COALESCE(e.enseignants_em_femmes_1ere,0) + COALESCE(e.enseignants_em_femmes_2eme,0) + COALESCE(e.enseignants_em_femmes_3eme,0) +
            COALESCE(e.enseignants_d4p_femmes_1ere,0) + COALESCE(e.enseignants_d4p_femmes_2eme,0) + COALESCE(e.enseignants_d4p_femmes_3eme,0) +
            COALESCE(e.enseignants_p6_femmes_1ere,0) + COALESCE(e.enseignants_p6_femmes_2eme,0) + COALESCE(e.enseignants_p6_femmes_3eme,0) +
            COALESCE(e.enseignants_d6_femmes_1ere,0) + COALESCE(e.enseignants_d6_femmes_2eme,0) + COALESCE(e.enseignants_d6_femmes_3eme,0) +
            COALESCE(e.enseignants_autres_femmes_1ere,0) + COALESCE(e.enseignants_autres_femmes_2eme,0) + COALESCE(e.enseignants_autres_femmes_3eme,0) AS total_niveau
        FROM formulaires f
        LEFT JOIN st1_enseignant e ON e.form_st_id = f.id
        WHERE {where_clause}
        UNION ALL
        SELECT 
            f.id,
            f.idannee,
            f.identification_id,
            'Total' AS sexe,
            COALESCE(e.enseignants_d4_hommes_1ere,0) + COALESCE(e.enseignants_d4_hommes_2eme,0) + COALESCE(e.enseignants_d4_hommes_3eme,0) +
            COALESCE(e.enseignants_d4_femmes_1ere,0) + COALESCE(e.enseignants_d4_femmes_2eme,0) + COALESCE(e.enseignants_d4_femmes_3eme,0) AS D4,
            COALESCE(e.enseignants_em_hommes_1ere,0) + COALESCE(e.enseignants_em_hommes_2eme,0) + COALESCE(e.enseignants_em_hommes_3eme,0) +
            COALESCE(e.enseignants_em_femmes_1ere,0) + COALESCE(e.enseignants_em_femmes_2eme,0) + COALESCE(e.enseignants_em_femmes_3eme,0) AS EM,
            COALESCE(e.enseignants_d4p_hommes_1ere,0) + COALESCE(e.enseignants_d4p_hommes_2eme,0) + COALESCE(e.enseignants_d4p_hommes_3eme,0) +
            COALESCE(e.enseignants_d4p_femmes_1ere,0) + COALESCE(e.enseignants_d4p_femmes_2eme,0) + COALESCE(e.enseignants_d4p_femmes_3eme,0) AS D4P,
            COALESCE(e.enseignants_p6_hommes_1ere,0) + COALESCE(e.enseignants_p6_hommes_2eme,0) + COALESCE(e.enseignants_p6_hommes_3eme,0) +
            COALESCE(e.enseignants_p6_femmes_1ere,0) + COALESCE(e.enseignants_p6_femmes_2eme,0) + COALESCE(e.enseignants_p6_femmes_3eme,0) AS P6,
            COALESCE(e.enseignants_d6_hommes_1ere,0) + COALESCE(e.enseignants_d6_hommes_2eme,0) + COALESCE(e.enseignants_d6_hommes_3eme,0) +
            COALESCE(e.enseignants_d6_femmes_1ere,0) + COALESCE(e.enseignants_d6_femmes_2eme,0) + COALESCE(e.enseignants_d6_femmes_3eme,0) AS D6,
            COALESCE(e.enseignants_autres_hommes_1ere,0) + COALESCE(e.enseignants_autres_hommes_2eme,0) + COALESCE(e.enseignants_autres_hommes_3eme,0) +
            COALESCE(e.enseignants_autres_femmes_1ere,0) + COALESCE(e.enseignants_autres_femmes_2eme,0) + COALESCE(e.enseignants_autres_femmes_3eme,0) AS AUTRES,
            COALESCE(e.enseignants_d4_hommes_1ere,0) + COALESCE(e.enseignants_d4_hommes_2eme,0) + COALESCE(e.enseignants_d4_hommes_3eme,0) +
            COALESCE(e.enseignants_d4_femmes_1ere,0) + COALESCE(e.enseignants_d4_femmes_2eme,0) + COALESCE(e.enseignants_d4_femmes_3eme,0) +
            COALESCE(e.enseignants_em_hommes_1ere,0) + COALESCE(e.enseignants_em_hommes_2eme,0) + COALESCE(e.enseignants_em_hommes_3eme,0) +
            COALESCE(e.enseignants_em_femmes_1ere,0) + COALESCE(e.enseignants_em_femmes_2eme,0) + COALESCE(e.enseignants_em_femmes_3eme,0) +
            COALESCE(e.enseignants_d4p_hommes_1ere,0) + COALESCE(e.enseignants_d4p_hommes_2eme,0) + COALESCE(e.enseignants_d4p_hommes_3eme,0) +
            COALESCE(e.enseignants_d4p_femmes_1ere,0) + COALESCE(e.enseignants_d4p_femmes_2eme,0) + COALESCE(e.enseignants_d4p_femmes_3eme,0) +
            COALESCE(e.enseignants_p6_hommes_1ere,0) + COALESCE(e.enseignants_p6_hommes_2eme,0) + COALESCE(e.enseignants_p6_hommes_3eme,0) +
            COALESCE(e.enseignants_p6_femmes_1ere,0) + COALESCE(e.enseignants_p6_femmes_2eme,0) + COALESCE(e.enseignants_p6_femmes_3eme,0) +
            COALESCE(e.enseignants_d6_hommes_1ere,0) + COALESCE(e.enseignants_d6_hommes_2eme,0) + COALESCE(e.enseignants_d6_hommes_3eme,0) +
            COALESCE(e.enseignants_d6_femmes_1ere,0) + COALESCE(e.enseignants_d6_femmes_2eme,0) + COALESCE(e.enseignants_d6_femmes_3eme,0) +
            COALESCE(e.enseignants_autres_hommes_1ere,0) + COALESCE(e.enseignants_autres_hommes_2eme,0) + COALESCE(e.enseignants_autres_hommes_3eme,0) +
            COALESCE(e.enseignants_autres_femmes_1ere,0) + COALESCE(e.enseignants_autres_femmes_2eme,0) + COALESCE(e.enseignants_autres_femmes_3eme,0) AS total_niveau
        FROM formulaires f
        LEFT JOIN st1_enseignant e ON e.form_st_id = f.id
        WHERE {where_clause}
    ) AS aggregated_data
    JOIN identifications i ON aggregated_data.identification_id = i.id
    GROUP BY secteur, "regime de gestion", sexe, idannee
    ORDER BY secteur, "regime de gestion", 
             CASE WHEN sexe = 'Hommes' THEN 1 
                  WHEN sexe = 'Femmes' THEN 2 
                  ELSE 3 END,
             idannee
    {limit_clause};
    """

def get_diplome_niveau_maternelle_query(where_clause, page_size=None, offset=0):
    limit_clause = f" LIMIT {page_size} OFFSET {offset}" if page_size else ""
    return f"""
    SELECT * FROM (
        SELECT
            CASE 
                WHEN idannee IN ('16', '17') THEN idannee
                ELSE 'NR'
            END AS idannee,
            COALESCE(NULLIF(diplome, ''), 'NR') AS diplome,
            IFNULL(sexe, 'Total') AS sexe,
            SUM(CASE WHEN niveau = '1ere Maternelle' THEN effectif ELSE 0 END) AS '1ere Maternelle',
            SUM(CASE WHEN niveau = '2eme Maternelle' THEN effectif ELSE 0 END) AS '2eme Maternelle',
            SUM(CASE WHEN niveau = '3eme Maternelle' THEN effectif ELSE 0 END) AS '3eme Maternelle',
            SUM(effectif) AS Total
        FROM (
            -- Sous-requête avec toutes les combinaisons diplôme/sexe/niveau
            SELECT
                'D4' AS diplome,
                'Hommes' AS sexe,
                f.idannee,
                '1ere Maternelle' AS niveau,
                SUM(COALESCE(e.enseignants_d4_hommes_1ere, 0)) AS effectif
            FROM formulaires f
            LEFT JOIN st1_enseignant e ON e.form_st_id = f.id
            WHERE {where_clause}
            GROUP BY f.idannee
            UNION ALL
            SELECT 'D4', 'Femmes', f.idannee, '1ere Maternelle', SUM(COALESCE(e.enseignants_d4_femmes_1ere, 0))
            FROM formulaires f LEFT JOIN st1_enseignant e ON e.form_st_id = f.id WHERE {where_clause} GROUP BY f.idannee
            UNION ALL SELECT 'EM', 'Hommes', f.idannee, '1ere Maternelle', SUM(COALESCE(e.enseignants_em_hommes_1ere, 0)) FROM formulaires f LEFT JOIN st1_enseignant e ON e.form_st_id = f.id WHERE {where_clause} GROUP BY f.idannee
            UNION ALL SELECT 'EM', 'Femmes', f.idannee, '1ere Maternelle', SUM(COALESCE(e.enseignants_em_femmes_1ere, 0)) FROM formulaires f LEFT JOIN st1_enseignant e ON e.form_st_id = f.id WHERE {where_clause} GROUP BY f.idannee
            UNION ALL SELECT 'D4', 'Hommes', f.idannee, '2eme Maternelle', SUM(COALESCE(e.enseignants_d4_hommes_2eme, 0)) FROM formulaires f LEFT JOIN st1_enseignant e ON e.form_st_id = f.id WHERE {where_clause} GROUP BY f.idannee
            UNION ALL SELECT 'D4', 'Femmes', f.idannee, '2eme Maternelle', SUM(COALESCE(e.enseignants_d4_femmes_2eme, 0)) FROM formulaires f LEFT JOIN st1_enseignant e ON e.form_st_id = f.id WHERE {where_clause} GROUP BY f.idannee
            UNION ALL SELECT 'EM', 'Hommes', f.idannee, '2eme Maternelle', SUM(COALESCE(e.enseignants_em_hommes_2eme, 0)) FROM formulaires f LEFT JOIN st1_enseignant e ON e.form_st_id = f.id WHERE {where_clause} GROUP BY f.idannee
            UNION ALL SELECT 'EM', 'Femmes', f.idannee, '2eme Maternelle', SUM(COALESCE(e.enseignants_em_femmes_2eme, 0)) FROM formulaires f LEFT JOIN st1_enseignant e ON e.form_st_id = f.id WHERE {where_clause} GROUP BY f.idannee
            UNION ALL SELECT 'D4', 'Hommes', f.idannee, '3eme Maternelle', SUM(COALESCE(e.enseignants_d4_hommes_3eme, 0)) FROM formulaires f LEFT JOIN st1_enseignant e ON e.form_st_id = f.id WHERE {where_clause} GROUP BY f.idannee
            UNION ALL SELECT 'D4', 'Femmes', f.idannee, '3eme Maternelle', SUM(COALESCE(e.enseignants_d4_femmes_3eme, 0)) FROM formulaires f LEFT JOIN st1_enseignant e ON e.form_st_id = f.id WHERE {where_clause} GROUP BY f.idannee
            UNION ALL SELECT 'EM', 'Hommes', f.idannee, '3eme Maternelle', SUM(COALESCE(e.enseignants_em_hommes_3eme, 0)) FROM formulaires f LEFT JOIN st1_enseignant e ON e.form_st_id = f.id WHERE {where_clause} GROUP BY f.idannee
            UNION ALL SELECT 'EM', 'Femmes', f.idannee, '3eme Maternelle', SUM(COALESCE(e.enseignants_em_femmes_3eme, 0)) FROM formulaires f LEFT JOIN st1_enseignant e ON e.form_st_id = f.id WHERE {where_clause} GROUP BY f.idannee
            UNION ALL SELECT 'D4P', 'Hommes', f.idannee, '1ere Maternelle', SUM(COALESCE(e.enseignants_d4p_hommes_1ere, 0)) FROM formulaires f LEFT JOIN st1_enseignant e ON e.form_st_id = f.id WHERE {where_clause} GROUP BY f.idannee
            UNION ALL SELECT 'D4P', 'Femmes', f.idannee, '1ere Maternelle', SUM(COALESCE(e.enseignants_d4p_femmes_1ere, 0)) FROM formulaires f LEFT JOIN st1_enseignant e ON e.form_st_id = f.id WHERE {where_clause} GROUP BY f.idannee
            UNION ALL SELECT 'P6', 'Hommes', f.idannee, '1ere Maternelle', SUM(COALESCE(e.enseignants_p6_hommes_1ere, 0)) FROM formulaires f LEFT JOIN st1_enseignant e ON e.form_st_id = f.id WHERE {where_clause} GROUP BY f.idannee
            UNION ALL SELECT 'P6', 'Femmes', f.idannee, '1ere Maternelle', SUM(COALESCE(e.enseignants_p6_femmes_1ere, 0)) FROM formulaires f LEFT JOIN st1_enseignant e ON e.form_st_id = f.id WHERE {where_clause} GROUP BY f.idannee
            UNION ALL SELECT 'D6', 'Hommes', f.idannee, '1ere Maternelle', SUM(COALESCE(e.enseignants_d6_hommes_1ere, 0)) FROM formulaires f LEFT JOIN st1_enseignant e ON e.form_st_id = f.id WHERE {where_clause} GROUP BY f.idannee
            UNION ALL SELECT 'D6', 'Femmes', f.idannee, '1ere Maternelle', SUM(COALESCE(e.enseignants_d6_femmes_1ere, 0)) FROM formulaires f LEFT JOIN st1_enseignant e ON e.form_st_id = f.id WHERE {where_clause} GROUP BY f.idannee
            UNION ALL SELECT 'AUTRES', 'Hommes', f.idannee, '1ere Maternelle', SUM(COALESCE(e.enseignants_autres_hommes_1ere, 0)) FROM formulaires f LEFT JOIN st1_enseignant e ON e.form_st_id = f.id WHERE {where_clause} GROUP BY f.idannee
            UNION ALL SELECT 'AUTRES', 'Femmes', f.idannee, '1ere Maternelle', SUM(COALESCE(e.enseignants_autres_femmes_1ere, 0)) FROM formulaires f LEFT JOIN st1_enseignant e ON e.form_st_id = f.id WHERE {where_clause} GROUP BY f.idannee
            -- Répéter pour les autres niveaux avec les nouveaux diplômes...
        ) AS source_data
        GROUP BY idannee, diplome, sexe WITH ROLLUP
    ) AS results
    WHERE sexe IS NOT NULL OR diplome IS NOT NULL
    ORDER BY 
        CASE WHEN idannee = 'NR' THEN 1 ELSE 0 END,
        idannee,
        CASE WHEN diplome = 'NR' THEN 1 ELSE 0 END,
        diplome,
        CASE WHEN sexe = 'Total' THEN 2 ELSE 1 END
    {limit_clause};
    """

def get_effectif_regime_sexe_province_query(where_clause, page_size=None, offset=0):
    limit_clause = f" LIMIT {page_size} OFFSET {offset}" if page_size else ""
    return f"""
    SELECT
        p.id AS "id",
        p.libelle AS "province",
        sexe,
        idannee,
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ECC' THEN total_niveau ELSE 0 END) AS "ECC",
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ECF' THEN total_niveau ELSE 0 END) AS "ECF",
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ECI' THEN total_niveau ELSE 0 END) AS "ECI",
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ECK' THEN total_niveau ELSE 0 END) AS "ECK",
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ECP' THEN total_niveau ELSE 0 END) AS "ECP",
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ECS' THEN total_niveau ELSE 0 END) AS "ECS",
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ENC' THEN total_niveau ELSE 0 END) AS "ENC",
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'AUTRES' THEN total_niveau ELSE 0 END) AS "AUTRES",
        SUM(CASE WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN total_niveau ELSE 0 END) AS "NR",
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'EPR' THEN total_niveau ELSE 0 END) AS "Privé",
        SUM(total_niveau) AS "Total Général"
    FROM (
        SELECT
            f.id,
            f.idannee,
            f.identification_id,
            'Hommes' AS sexe,
            COALESCE(e.enseignants_d4_hommes_1ere,0) + COALESCE(e.enseignants_d4_hommes_2eme,0) + COALESCE(e.enseignants_d4_hommes_3eme,0) +
            COALESCE(e.enseignants_em_hommes_1ere,0) + COALESCE(e.enseignants_em_hommes_2eme,0) + COALESCE(e.enseignants_em_hommes_3eme,0) +
            COALESCE(e.enseignants_d4p_hommes_1ere,0) + COALESCE(e.enseignants_d4p_hommes_2eme,0) + COALESCE(e.enseignants_d4p_hommes_3eme,0) +
            COALESCE(e.enseignants_p6_hommes_1ere,0) + COALESCE(e.enseignants_p6_hommes_2eme,0) + COALESCE(e.enseignants_p6_hommes_3eme,0) +
            COALESCE(e.enseignants_d6_hommes_1ere,0) + COALESCE(e.enseignants_d6_hommes_2eme,0) + COALESCE(e.enseignants_d6_hommes_3eme,0) +
            COALESCE(e.enseignants_autres_hommes_1ere,0) + COALESCE(e.enseignants_autres_hommes_2eme,0) + COALESCE(e.enseignants_autres_hommes_3eme,0) AS total_niveau
        FROM formulaires f
        LEFT JOIN st1_enseignant e ON e.form_st_id = f.id
        WHERE {where_clause}
        UNION ALL
        SELECT
            f.id,
            f.idannee,
            f.identification_id,
            'Femmes' AS sexe,
            COALESCE(e.enseignants_d4_femmes_1ere,0) + COALESCE(e.enseignants_d4_femmes_2eme,0) + COALESCE(e.enseignants_d4_femmes_3eme,0) +
            COALESCE(e.enseignants_em_femmes_1ere,0) + COALESCE(e.enseignants_em_femmes_2eme,0) + COALESCE(e.enseignants_em_femmes_3eme,0) +
            COALESCE(e.enseignants_d4p_femmes_1ere,0) + COALESCE(e.enseignants_d4p_femmes_2eme,0) + COALESCE(e.enseignants_d4p_femmes_3eme,0) +
            COALESCE(e.enseignants_p6_femmes_1ere,0) + COALESCE(e.enseignants_p6_femmes_2eme,0) + COALESCE(e.enseignants_p6_femmes_3eme,0) +
            COALESCE(e.enseignants_d6_femmes_1ere,0) + COALESCE(e.enseignants_d6_femmes_2eme,0) + COALESCE(e.enseignants_d6_femmes_3eme,0) +
            COALESCE(e.enseignants_autres_femmes_1ere,0) + COALESCE(e.enseignants_autres_femmes_2eme,0) + COALESCE(e.enseignants_autres_femmes_3eme,0) AS total_niveau
        FROM formulaires f
        LEFT JOIN st1_enseignant e ON e.form_st_id = f.id
        WHERE {where_clause}
        UNION ALL
        SELECT
            f.id,
            f.idannee,
            f.identification_id,
            'Total' AS sexe,
            COALESCE(e.enseignants_d4_hommes_1ere,0) + COALESCE(e.enseignants_d4_hommes_2eme,0) + COALESCE(e.enseignants_d4_hommes_3eme,0) +
            COALESCE(e.enseignants_d4_femmes_1ere,0) + COALESCE(e.enseignants_d4_femmes_2eme,0) + COALESCE(e.enseignants_d4_femmes_3eme,0) +
            COALESCE(e.enseignants_em_hommes_1ere,0) + COALESCE(e.enseignants_em_hommes_2eme,0) + COALESCE(e.enseignants_em_hommes_3eme,0) +
            COALESCE(e.enseignants_em_femmes_1ere,0) + COALESCE(e.enseignants_em_femmes_2eme,0) + COALESCE(e.enseignants_em_femmes_3eme,0) +
            COALESCE(e.enseignants_d4p_hommes_1ere,0) + COALESCE(e.enseignants_d4p_hommes_2eme,0) + COALESCE(e.enseignants_d4p_hommes_3eme,0) +
            COALESCE(e.enseignants_d4p_femmes_1ere,0) + COALESCE(e.enseignants_d4p_femmes_2eme,0) + COALESCE(e.enseignants_d4p_femmes_3eme,0) +
            COALESCE(e.enseignants_p6_hommes_1ere,0) + COALESCE(e.enseignants_p6_hommes_2eme,0) + COALESCE(e.enseignants_p6_hommes_3eme,0) +
            COALESCE(e.enseignants_p6_femmes_1ere,0) + COALESCE(e.enseignants_p6_femmes_2eme,0) + COALESCE(e.enseignants_p6_femmes_3eme,0) +
            COALESCE(e.enseignants_d6_hommes_1ere,0) + COALESCE(e.enseignants_d6_hommes_2eme,0) + COALESCE(e.enseignants_d6_hommes_3eme,0) +
            COALESCE(e.enseignants_d6_femmes_1ere,0) + COALESCE(e.enseignants_d6_femmes_2eme,0) + COALESCE(e.enseignants_d6_femmes_3eme,0) +
            COALESCE(e.enseignants_autres_hommes_1ere,0) + COALESCE(e.enseignants_autres_hommes_2eme,0) + COALESCE(e.enseignants_autres_hommes_3eme,0) +
            COALESCE(e.enseignants_autres_femmes_1ere,0) + COALESCE(e.enseignants_autres_femmes_2eme,0) + COALESCE(e.enseignants_autres_femmes_3eme,0) AS total_niveau
        FROM formulaires f
        LEFT JOIN st1_enseignant e ON e.form_st_id = f.id
        WHERE {where_clause}
    ) AS aggregated_data
    JOIN identifications i ON aggregated_data.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    GROUP BY p.id, p.libelle, sexe, idannee
    ORDER BY p.id, idannee, sexe
    {limit_clause};
    """

def get_effectif_regime_province_simple_query(where_clause, page_size=None, offset=0):
    limit_clause = f" LIMIT {page_size} OFFSET {offset}" if page_size else ""
    return f"""
    SELECT
        p.id AS "id",
        p.libelle AS "province",
        idannee,
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ECC' THEN total_tous_champs ELSE 0 END) AS "ECC",
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ECF' THEN total_tous_champs ELSE 0 END) AS "ECF",
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ECI' THEN total_tous_champs ELSE 0 END) AS "ECI",
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ECK' THEN total_tous_champs ELSE 0 END) AS "ECK",
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ECP' THEN total_tous_champs ELSE 0 END) AS "ECP",
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ECS' THEN total_tous_champs ELSE 0 END) AS "ECS",
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'ENC' THEN total_tous_champs ELSE 0 END) AS "ENC",
        SUM(CASE WHEN UPPER(i.regime_gestion) = 'AUTRES' THEN total_tous_champs ELSE 0 END) AS "AUTRES",
        SUM(CASE WHEN UPPER(i.regime_gestion) != 'EPR' AND i.regime_gestion IS NOT NULL AND i.regime_gestion != '' THEN total_tous_champs ELSE 0 END) AS "Public",
        SUM(CASE WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN total_tous_champs ELSE 0 END) AS "NR"
    FROM (
        SELECT
            f.id,
            f.idannee,
            f.identification_id,
            COALESCE(e.enseignants_d4_hommes_1ere,0) + COALESCE(e.enseignants_d4_hommes_2eme,0) + COALESCE(e.enseignants_d4_hommes_3eme,0) +
            COALESCE(e.enseignants_d4_femmes_1ere,0) + COALESCE(e.enseignants_d4_femmes_2eme,0) + COALESCE(e.enseignants_d4_femmes_3eme,0) +
            COALESCE(e.enseignants_em_hommes_1ere,0) + COALESCE(e.enseignants_em_hommes_2eme,0) + COALESCE(e.enseignants_em_hommes_3eme,0) +
            COALESCE(e.enseignants_em_femmes_1ere,0) + COALESCE(e.enseignants_em_femmes_2eme,0) + COALESCE(e.enseignants_em_femmes_3eme,0) +
            COALESCE(e.enseignants_d4p_hommes_1ere,0) + COALESCE(e.enseignants_d4p_hommes_2eme,0) + COALESCE(e.enseignants_d4p_hommes_3eme,0) +
            COALESCE(e.enseignants_d4p_femmes_1ere,0) + COALESCE(e.enseignants_d4p_femmes_2eme,0) + COALESCE(e.enseignants_d4p_femmes_3eme,0) +
            COALESCE(e.enseignants_p6_hommes_1ere,0) + COALESCE(e.enseignants_p6_hommes_2eme,0) + COALESCE(e.enseignants_p6_hommes_3eme,0) +
            COALESCE(e.enseignants_p6_femmes_1ere,0) + COALESCE(e.enseignants_p6_femmes_2eme,0) + COALESCE(e.enseignants_p6_femmes_3eme,0) +
            COALESCE(e.enseignants_d6_hommes_1ere,0) + COALESCE(e.enseignants_d6_hommes_2eme,0) + COALESCE(e.enseignants_d6_hommes_3eme,0) +
            COALESCE(e.enseignants_d6_femmes_1ere,0) + COALESCE(e.enseignants_d6_femmes_2eme,0) + COALESCE(e.enseignants_d6_femmes_3eme,0) +
            COALESCE(e.enseignants_autres_hommes_1ere,0) + COALESCE(e.enseignants_autres_hommes_2eme,0) + COALESCE(e.enseignants_autres_hommes_3eme,0) +
            COALESCE(e.enseignants_autres_femmes_1ere,0) + COALESCE(e.enseignants_autres_femmes_2eme,0) + COALESCE(e.enseignants_autres_femmes_3eme,0) AS total_tous_champs
        FROM formulaires f
        LEFT JOIN st1_enseignant e ON e.form_st_id = f.id
        WHERE {where_clause}
    ) AS aggregated_data
    JOIN identifications i ON aggregated_data.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    GROUP BY p.id, p.libelle, idannee
    ORDER BY p.id, idannee
    {limit_clause};
    """

def get_effectif_milieu_public_province_query(where_clause, page_size=None, offset=0):
    limit_clause = f" LIMIT {page_size} OFFSET {offset}" if page_size else ""
    return f"""
    SELECT
        p.id AS "id",
        p.libelle AS "province",
        idannee,
        SUM(CASE WHEN UPPER(i.milieu) = 'URBAIN' THEN total_tous_champs ELSE 0 END) AS "URBAIN",
        SUM(CASE WHEN UPPER(i.milieu) = 'RURAL' THEN total_tous_champs ELSE 0 END) AS "RURAL",
        SUM(CASE WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN total_tous_champs ELSE 0 END) AS "NR",
        SUM(CASE WHEN UPPER(i.milieu) = 'URBAIN' THEN total_tous_champs ELSE 0 END) +
        SUM(CASE WHEN UPPER(i.milieu) = 'RURAL' THEN total_tous_champs ELSE 0 END) +
        SUM(CASE WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN total_tous_champs ELSE 0 END) AS "Total_general"
    FROM (
        SELECT
            f.id,
            f.idannee,
            f.identification_id,
            COALESCE(e.enseignants_d4_hommes_1ere,0) + COALESCE(e.enseignants_d4_hommes_2eme,0) + COALESCE(e.enseignants_d4_hommes_3eme,0) +
            COALESCE(e.enseignants_d4_femmes_1ere,0) + COALESCE(e.enseignants_d4_femmes_2eme,0) + COALESCE(e.enseignants_d4_femmes_3eme,0) +
            COALESCE(e.enseignants_em_hommes_1ere,0) + COALESCE(e.enseignants_em_hommes_2eme,0) + COALESCE(e.enseignants_em_hommes_3eme,0) +
            COALESCE(e.enseignants_em_femmes_1ere,0) + COALESCE(e.enseignants_em_femmes_2eme,0) + COALESCE(e.enseignants_em_femmes_3eme,0) +
            COALESCE(e.enseignants_d4p_hommes_1ere,0) + COALESCE(e.enseignants_d4p_hommes_2eme,0) + COALESCE(e.enseignants_d4p_hommes_3eme,0) +
            COALESCE(e.enseignants_d4p_femmes_1ere,0) + COALESCE(e.enseignants_d4p_femmes_2eme,0) + COALESCE(e.enseignants_d4p_femmes_3eme,0) +
            COALESCE(e.enseignants_p6_hommes_1ere,0) + COALESCE(e.enseignants_p6_hommes_2eme,0) + COALESCE(e.enseignants_p6_hommes_3eme,0) +
            COALESCE(e.enseignants_p6_femmes_1ere,0) + COALESCE(e.enseignants_p6_femmes_2eme,0) + COALESCE(e.enseignants_p6_femmes_3eme,0) +
            COALESCE(e.enseignants_d6_hommes_1ere,0) + COALESCE(e.enseignants_d6_hommes_2eme,0) + COALESCE(e.enseignants_d6_hommes_3eme,0) +
            COALESCE(e.enseignants_d6_femmes_1ere,0) + COALESCE(e.enseignants_d6_femmes_2eme,0) + COALESCE(e.enseignants_d6_femmes_3eme,0) +
            COALESCE(e.enseignants_autres_hommes_1ere,0) + COALESCE(e.enseignants_autres_hommes_2eme,0) + COALESCE(e.enseignants_autres_hommes_3eme,0) +
            COALESCE(e.enseignants_autres_femmes_1ere,0) + COALESCE(e.enseignants_autres_femmes_2eme,0) + COALESCE(e.enseignants_autres_femmes_3eme,0) AS total_tous_champs
        FROM formulaires f
        LEFT JOIN st1_enseignant e ON e.form_st_id = f.id
        WHERE {where_clause}
    ) AS aggregated_data
    JOIN identifications i ON aggregated_data.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE UPPER(i.regime_gestion) != 'EPR' OR i.regime_gestion IS NULL OR i.regime_gestion = ''
    GROUP BY p.id, p.libelle, idannee
    ORDER BY p.id, idannee
    {limit_clause};
    """

def get_pourcentage_niveau_national_query(where_clause, page_size=None, offset=0):
    limit_clause = f" LIMIT {page_size} OFFSET {offset}" if page_size else ""
    return f"""
    SELECT 
        CASE 
            WHEN UPPER(i.regime_gestion) = 'EPR' THEN 'Privé'
            WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN 'NR'
            ELSE 'Public'
        END AS secteur,
        COALESCE(NULLIF(i.regime_gestion, ''), 'NR') AS "regime de gestion",
        f.idannee,
        ROUND(
            (
                SUM(COALESCE(e.enseignants_d4_hommes_1ere,0) + COALESCE(e.enseignants_d4_hommes_2eme,0) + COALESCE(e.enseignants_d4_hommes_3eme,0) +
                    COALESCE(e.enseignants_d4_femmes_1ere,0) + COALESCE(e.enseignants_d4_femmes_2eme,0) + COALESCE(e.enseignants_d4_femmes_3eme,0)
                ) * 100.0 
            ) / 
            NULLIF(
                SUM(
                    COALESCE(e.enseignants_d4_hommes_1ere,0) + COALESCE(e.enseignants_d4_hommes_2eme,0) + COALESCE(e.enseignants_d4_hommes_3eme,0) +
                    COALESCE(e.enseignants_d4_femmes_1ere,0) + COALESCE(e.enseignants_d4_femmes_2eme,0) + COALESCE(e.enseignants_d4_femmes_3eme,0) +
                    COALESCE(e.enseignants_em_hommes_1ere,0) + COALESCE(e.enseignants_em_hommes_2eme,0) + COALESCE(e.enseignants_em_hommes_3eme,0) +
                    COALESCE(e.enseignants_em_femmes_1ere,0) + COALESCE(e.enseignants_em_femmes_2eme,0) + COALESCE(e.enseignants_em_femmes_3eme,0) +
                    COALESCE(e.enseignants_d4p_hommes_1ere,0) + COALESCE(e.enseignants_d4p_hommes_2eme,0) + COALESCE(e.enseignants_d4p_hommes_3eme,0) +
                    COALESCE(e.enseignants_d4p_femmes_1ere,0) + COALESCE(e.enseignants_d4p_femmes_2eme,0) + COALESCE(e.enseignants_d4p_femmes_3eme,0) +
                    COALESCE(e.enseignants_p6_hommes_1ere,0) + COALESCE(e.enseignants_p6_hommes_2eme,0) + COALESCE(e.enseignants_p6_hommes_3eme,0) +
                    COALESCE(e.enseignants_p6_femmes_1ere,0) + COALESCE(e.enseignants_p6_femmes_2eme,0) + COALESCE(e.enseignants_p6_femmes_3eme,0) +
                    COALESCE(e.enseignants_d6_hommes_1ere,0) + COALESCE(e.enseignants_d6_hommes_2eme,0) + COALESCE(e.enseignants_d6_hommes_3eme,0) +
                    COALESCE(e.enseignants_d6_femmes_1ere,0) + COALESCE(e.enseignants_d6_femmes_2eme,0) + COALESCE(e.enseignants_d6_femmes_3eme,0) +
                    COALESCE(e.enseignants_autres_hommes_1ere,0) + COALESCE(e.enseignants_autres_hommes_2eme,0) + COALESCE(e.enseignants_autres_hommes_3eme,0) +
                    COALESCE(e.enseignants_autres_femmes_1ere,0) + COALESCE(e.enseignants_autres_femmes_2eme,0) + COALESCE(e.enseignants_autres_femmes_3eme,0)
                ), 0
            ), 2
        ) AS "D4 (%)",
        ROUND(
            (
                SUM(COALESCE(e.enseignants_em_hommes_1ere,0) + COALESCE(e.enseignants_em_hommes_2eme,0) + COALESCE(e.enseignants_em_hommes_3eme,0) +
                    COALESCE(e.enseignants_em_femmes_1ere,0) + COALESCE(e.enseignants_em_femmes_2eme,0) + COALESCE(e.enseignants_em_femmes_3eme,0)
                ) * 100.0 
            ) / 
            NULLIF(
                SUM(
                    COALESCE(e.enseignants_d4_hommes_1ere,0) + COALESCE(e.enseignants_d4_hommes_2eme,0) + COALESCE(e.enseignants_d4_hommes_3eme,0) +
                    COALESCE(e.enseignants_d4_femmes_1ere,0) + COALESCE(e.enseignants_d4_femmes_2eme,0) + COALESCE(e.enseignants_d4_femmes_3eme,0) +
                    COALESCE(e.enseignants_em_hommes_1ere,0) + COALESCE(e.enseignants_em_hommes_2eme,0) + COALESCE(e.enseignants_em_hommes_3eme,0) +
                    COALESCE(e.enseignants_em_femmes_1ere,0) + COALESCE(e.enseignants_em_femmes_2eme,0) + COALESCE(e.enseignants_em_femmes_3eme,0) +
                    COALESCE(e.enseignants_d4p_hommes_1ere,0) + COALESCE(e.enseignants_d4p_hommes_2eme,0) + COALESCE(e.enseignants_d4p_hommes_3eme,0) +
                    COALESCE(e.enseignants_d4p_femmes_1ere,0) + COALESCE(e.enseignants_d4p_femmes_2eme,0) + COALESCE(e.enseignants_d4p_femmes_3eme,0) +
                    COALESCE(e.enseignants_p6_hommes_1ere,0) + COALESCE(e.enseignants_p6_hommes_2eme,0) + COALESCE(e.enseignants_p6_hommes_3eme,0) +
                    COALESCE(e.enseignants_p6_femmes_1ere,0) + COALESCE(e.enseignants_p6_femmes_2eme,0) + COALESCE(e.enseignants_p6_femmes_3eme,0) +
                    COALESCE(e.enseignants_d6_hommes_1ere,0) + COALESCE(e.enseignants_d6_hommes_2eme,0) + COALESCE(e.enseignants_d6_hommes_3eme,0) +
                    COALESCE(e.enseignants_d6_femmes_1ere,0) + COALESCE(e.enseignants_d6_femmes_2eme,0) + COALESCE(e.enseignants_d6_femmes_3eme,0) +
                    COALESCE(e.enseignants_autres_hommes_1ere,0) + COALESCE(e.enseignants_autres_hommes_2eme,0) + COALESCE(e.enseignants_autres_hommes_3eme,0) +
                    COALESCE(e.enseignants_autres_femmes_1ere,0) + COALESCE(e.enseignants_autres_femmes_2eme,0) + COALESCE(e.enseignants_autres_femmes_3eme,0)
                ), 0
            ), 2
        ) AS "EM (%)",
        ROUND(
            (
                SUM(COALESCE(e.enseignants_d4p_hommes_1ere,0) + COALESCE(e.enseignants_d4p_hommes_2eme,0) + COALESCE(e.enseignants_d4p_hommes_3eme,0) +
                    COALESCE(e.enseignants_d4p_femmes_1ere,0) + COALESCE(e.enseignants_d4p_femmes_2eme,0) + COALESCE(e.enseignants_d4p_femmes_3eme,0)
                ) * 100.0 
            ) / 
            NULLIF(
                SUM(
                    COALESCE(e.enseignants_d4_hommes_1ere,0) + COALESCE(e.enseignants_d4_hommes_2eme,0) + COALESCE(e.enseignants_d4_hommes_3eme,0) +
                    COALESCE(e.enseignants_d4_femmes_1ere,0) + COALESCE(e.enseignants_d4_femmes_2eme,0) + COALESCE(e.enseignants_d4_femmes_3eme,0) +
                    COALESCE(e.enseignants_em_hommes_1ere,0) + COALESCE(e.enseignants_em_hommes_2eme,0) + COALESCE(e.enseignants_em_hommes_3eme,0) +
                    COALESCE(e.enseignants_em_femmes_1ere,0) + COALESCE(e.enseignants_em_femmes_2eme,0) + COALESCE(e.enseignants_em_femmes_3eme,0) +
                    COALESCE(e.enseignants_d4p_hommes_1ere,0) + COALESCE(e.enseignants_d4p_hommes_2eme,0) + COALESCE(e.enseignants_d4p_hommes_3eme,0) +
                    COALESCE(e.enseignants_d4p_femmes_1ere,0) + COALESCE(e.enseignants_d4p_femmes_2eme,0) + COALESCE(e.enseignants_d4p_femmes_3eme,0) +
                    COALESCE(e.enseignants_p6_hommes_1ere,0) + COALESCE(e.enseignants_p6_hommes_2eme,0) + COALESCE(e.enseignants_p6_hommes_3eme,0) +
                    COALESCE(e.enseignants_p6_femmes_1ere,0) + COALESCE(e.enseignants_p6_femmes_2eme,0) + COALESCE(e.enseignants_p6_femmes_3eme,0) +
                    COALESCE(e.enseignants_d6_hommes_1ere,0) + COALESCE(e.enseignants_d6_hommes_2eme,0) + COALESCE(e.enseignants_d6_hommes_3eme,0) +
                    COALESCE(e.enseignants_d6_femmes_1ere,0) + COALESCE(e.enseignants_d6_femmes_2eme,0) + COALESCE(e.enseignants_d6_femmes_3eme,0) +
                    COALESCE(e.enseignants_autres_hommes_1ere,0) + COALESCE(e.enseignants_autres_hommes_2eme,0) + COALESCE(e.enseignants_autres_hommes_3eme,0) +
                    COALESCE(e.enseignants_autres_femmes_1ere,0) + COALESCE(e.enseignants_autres_femmes_2eme,0) + COALESCE(e.enseignants_autres_femmes_3eme,0)
                ), 0
            ), 2
        ) AS "D4P (%)",
        ROUND(
            (
                SUM(COALESCE(e.enseignants_p6_hommes_1ere,0) + COALESCE(e.enseignants_p6_hommes_2eme,0) + COALESCE(e.enseignants_p6_hommes_3eme,0) +
                    COALESCE(e.enseignants_p6_femmes_1ere,0) + COALESCE(e.enseignants_p6_femmes_2eme,0) + COALESCE(e.enseignants_p6_femmes_3eme,0)
                ) * 100.0 
            ) / 
            NULLIF(
                SUM(
                    COALESCE(e.enseignants_d4_hommes_1ere,0) + COALESCE(e.enseignants_d4_hommes_2eme,0) + COALESCE(e.enseignants_d4_hommes_3eme,0) +
                    COALESCE(e.enseignants_d4_femmes_1ere,0) + COALESCE(e.enseignants_d4_femmes_2eme,0) + COALESCE(e.enseignants_d4_femmes_3eme,0) +
                    COALESCE(e.enseignants_em_hommes_1ere,0) + COALESCE(e.enseignants_em_hommes_2eme,0) + COALESCE(e.enseignants_em_hommes_3eme,0) +
                    COALESCE(e.enseignants_em_femmes_1ere,0) + COALESCE(e.enseignants_em_femmes_2eme,0) + COALESCE(e.enseignants_em_femmes_3eme,0) +
                    COALESCE(e.enseignants_d4p_hommes_1ere,0) + COALESCE(e.enseignants_d4p_hommes_2eme,0) + COALESCE(e.enseignants_d4p_hommes_3eme,0) +
                    COALESCE(e.enseignants_d4p_femmes_1ere,0) + COALESCE(e.enseignants_d4p_femmes_2eme,0) + COALESCE(e.enseignants_d4p_femmes_3eme,0) +
                    COALESCE(e.enseignants_p6_hommes_1ere,0) + COALESCE(e.enseignants_p6_hommes_2eme,0) + COALESCE(e.enseignants_p6_hommes_3eme,0) +
                    COALESCE(e.enseignants_p6_femmes_1ere,0) + COALESCE(e.enseignants_p6_femmes_2eme,0) + COALESCE(e.enseignants_p6_femmes_3eme,0) +
                    COALESCE(e.enseignants_d6_hommes_1ere,0) + COALESCE(e.enseignants_d6_hommes_2eme,0) + COALESCE(e.enseignants_d6_hommes_3eme,0) +
                    COALESCE(e.enseignants_d6_femmes_1ere,0) + COALESCE(e.enseignants_d6_femmes_2eme,0) + COALESCE(e.enseignants_d6_femmes_3eme,0) +
                    COALESCE(e.enseignants_autres_hommes_1ere,0) + COALESCE(e.enseignants_autres_hommes_2eme,0) + COALESCE(e.enseignants_autres_hommes_3eme,0) +
                    COALESCE(e.enseignants_autres_femmes_1ere,0) + COALESCE(e.enseignants_autres_femmes_2eme,0) + COALESCE(e.enseignants_autres_femmes_3eme,0)
                ), 0
            ), 2
        ) AS "P6 (%)",
        ROUND(
            (
                SUM(COALESCE(e.enseignants_d6_hommes_1ere,0) + COALESCE(e.enseignants_d6_hommes_2eme,0) + COALESCE(e.enseignants_d6_hommes_3eme,0) +
                    COALESCE(e.enseignants_d6_femmes_1ere,0) + COALESCE(e.enseignants_d6_femmes_2eme,0) + COALESCE(e.enseignants_d6_femmes_3eme,0)
                ) * 100.0 
            ) / 
            NULLIF(
                SUM(
                    COALESCE(e.enseignants_d4_hommes_1ere,0) + COALESCE(e.enseignants_d4_hommes_2eme,0) + COALESCE(e.enseignants_d4_hommes_3eme,0) +
                    COALESCE(e.enseignants_d4_femmes_1ere,0) + COALESCE(e.enseignants_d4_femmes_2eme,0) + COALESCE(e.enseignants_d4_femmes_3eme,0) +
                    COALESCE(e.enseignants_em_hommes_1ere,0) + COALESCE(e.enseignants_em_hommes_2eme,0) + COALESCE(e.enseignants_em_hommes_3eme,0) +
                    COALESCE(e.enseignants_em_femmes_1ere,0) + COALESCE(e.enseignants_em_femmes_2eme,0) + COALESCE(e.enseignants_em_femmes_3eme,0) +
                    COALESCE(e.enseignants_d4p_hommes_1ere,0) + COALESCE(e.enseignants_d4p_hommes_2eme,0) + COALESCE(e.enseignants_d4p_hommes_3eme,0) +
                    COALESCE(e.enseignants_d4p_femmes_1ere,0) + COALESCE(e.enseignants_d4p_femmes_2eme,0) + COALESCE(e.enseignants_d4p_femmes_3eme,0) +
                    COALESCE(e.enseignants_p6_hommes_1ere,0) + COALESCE(e.enseignants_p6_hommes_2eme,0) + COALESCE(e.enseignants_p6_hommes_3eme,0) +
                    COALESCE(e.enseignants_p6_femmes_1ere,0) + COALESCE(e.enseignants_p6_femmes_2eme,0) + COALESCE(e.enseignants_p6_femmes_3eme,0) +
                    COALESCE(e.enseignants_d6_hommes_1ere,0) + COALESCE(e.enseignants_d6_hommes_2eme,0) + COALESCE(e.enseignants_d6_hommes_3eme,0) +
                    COALESCE(e.enseignants_d6_femmes_1ere,0) + COALESCE(e.enseignants_d6_femmes_2eme,0) + COALESCE(e.enseignants_d6_femmes_3eme,0) +
                    COALESCE(e.enseignants_autres_hommes_1ere,0) + COALESCE(e.enseignants_autres_hommes_2eme,0) + COALESCE(e.enseignants_autres_hommes_3eme,0) +
                    COALESCE(e.enseignants_autres_femmes_1ere,0) + COALESCE(e.enseignants_autres_femmes_2eme,0) + COALESCE(e.enseignants_autres_femmes_3eme,0)
                ), 0
            ), 2
        ) AS "D6 (%)",
        ROUND(
            (
                SUM(COALESCE(e.enseignants_autres_hommes_1ere,0) + COALESCE(e.enseignants_autres_hommes_2eme,0) + COALESCE(e.enseignants_autres_hommes_3eme,0) +
                    COALESCE(e.enseignants_autres_femmes_1ere,0) + COALESCE(e.enseignants_autres_femmes_2eme,0) + COALESCE(e.enseignants_autres_femmes_3eme,0)
                ) * 100.0 
            ) / 
            NULLIF(
                SUM(
                    COALESCE(e.enseignants_d4_hommes_1ere,0) + COALESCE(e.enseignants_d4_hommes_2eme,0) + COALESCE(e.enseignants_d4_hommes_3eme,0) +
                    COALESCE(e.enseignants_d4_femmes_1ere,0) + COALESCE(e.enseignants_d4_femmes_2eme,0) + COALESCE(e.enseignants_d4_femmes_3eme,0) +
                    COALESCE(e.enseignants_em_hommes_1ere,0) + COALESCE(e.enseignants_em_hommes_2eme,0) + COALESCE(e.enseignants_em_hommes_3eme,0) +
                    COALESCE(e.enseignants_em_femmes_1ere,0) + COALESCE(e.enseignants_em_femmes_2eme,0) + COALESCE(e.enseignants_em_femmes_3eme,0) +
                    COALESCE(e.enseignants_d4p_hommes_1ere,0) + COALESCE(e.enseignants_d4p_hommes_2eme,0) + COALESCE(e.enseignants_d4p_hommes_3eme,0) +
                    COALESCE(e.enseignants_d4p_femmes_1ere,0) + COALESCE(e.enseignants_d4p_femmes_2eme,0) + COALESCE(e.enseignants_d4p_femmes_3eme,0) +
                    COALESCE(e.enseignants_p6_hommes_1ere,0) + COALESCE(e.enseignants_p6_hommes_2eme,0) + COALESCE(e.enseignants_p6_hommes_3eme,0) +
                    COALESCE(e.enseignants_p6_femmes_1ere,0) + COALESCE(e.enseignants_p6_femmes_2eme,0) + COALESCE(e.enseignants_p6_femmes_3eme,0) +
                    COALESCE(e.enseignants_d6_hommes_1ere,0) + COALESCE(e.enseignants_d6_hommes_2eme,0) + COALESCE(e.enseignants_d6_hommes_3eme,0) +
                    COALESCE(e.enseignants_d6_femmes_1ere,0) + COALESCE(e.enseignants_d6_femmes_2eme,0) + COALESCE(e.enseignants_d6_femmes_3eme,0) +
                    COALESCE(e.enseignants_autres_hommes_1ere,0) + COALESCE(e.enseignants_autres_hommes_2eme,0) + COALESCE(e.enseignants_autres_hommes_3eme,0) +
                    COALESCE(e.enseignants_autres_femmes_1ere,0) + COALESCE(e.enseignants_autres_femmes_2eme,0) + COALESCE(e.enseignants_autres_femmes_3eme,0)
                ), 0
            ), 2
        ) AS "AUTRES (%)",
        CASE 
            WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN 'NR'
            ELSE ''
        END AS "NR"
    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    LEFT JOIN st1_enseignant e ON e.form_st_id = f.id
    WHERE {where_clause}
    GROUP BY secteur, i.regime_gestion, f.idannee
    ORDER BY secteur, "regime de gestion", idannee
    {limit_clause};
    """

def get_normal_enseignants_query(where_clause, page_size=None, offset=0):
    limit_clause = f" LIMIT {page_size} OFFSET {offset}" if page_size else ""
    return f"""
    SELECT 
        f.id,
        f.idannee AS annee_scolaire,
        p.libelle AS province,
        CONCAT('Établissement ', f.id) AS nom_etablissement,
        'Adresse non disponible' AS adresse,
        'Téléphone non disponible' AS telephone,
        'Directeur non spécifié' AS directeur,
        'Actif' AS statut,
        f.created_at
    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE {where_clause}
    ORDER BY p.libelle, f.idannee
    {limit_clause};
    """

# Fonctions de comptage pour la pagination
def get_effectif_milieu_province_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM (
            SELECT f.id, f.idannee, f.identification_id
            FROM formulaires f
            LEFT JOIN st1_enseignant e ON e.form_st_id = f.id
            WHERE {where_clause}
        ) AS aggregated_data
        JOIN identifications i ON aggregated_data.identification_id = i.id
        JOIN provinces p ON i.fk_province_id = p.id
        GROUP BY p.id, p.libelle, idannee
    ) as subquery
    """

def get_effectif_regime_province_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM (
            SELECT f.id, f.idannee, f.identification_id
            FROM formulaires f
            LEFT JOIN st1_enseignant e ON e.form_st_id = f.id
            WHERE {where_clause}
        ) AS aggregated_data
        JOIN identifications i ON aggregated_data.identification_id = i.id
        JOIN provinces p ON i.fk_province_id = p.id
        GROUP BY p.id, p.libelle, idannee
    ) as subquery
    """

def get_niveau_formation_province_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM (
            SELECT f.id, f.idannee, f.identification_id, 'Hommes' AS sexe FROM formulaires f LEFT JOIN st1_enseignant e ON e.form_st_id = f.id WHERE {where_clause}
            UNION ALL SELECT f.id, f.idannee, f.identification_id, 'Femmes' AS sexe FROM formulaires f LEFT JOIN st1_enseignant e ON e.form_st_id = f.id WHERE {where_clause}
            UNION ALL SELECT f.id, f.idannee, f.identification_id, 'Total' AS sexe FROM formulaires f LEFT JOIN st1_enseignant e ON e.form_st_id = f.id WHERE {where_clause}
        ) AS aggregated_data
        JOIN identifications i ON aggregated_data.identification_id = i.id
        JOIN provinces p ON i.fk_province_id = p.id
        GROUP BY p.id, p.libelle, sexe, idannee
    ) as subquery
    """

def get_niveau_formation_national_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM (
            SELECT f.id, f.idannee, f.identification_id, 'Hommes' AS sexe FROM formulaires f LEFT JOIN st1_enseignant e ON e.form_st_id = f.id WHERE {where_clause}
            UNION ALL SELECT f.id, f.idannee, f.identification_id, 'Femmes' AS sexe FROM formulaires f LEFT JOIN st1_enseignant e ON e.form_st_id = f.id WHERE {where_clause}
            UNION ALL SELECT f.id, f.idannee, f.identification_id, 'Total' AS sexe FROM formulaires f LEFT JOIN st1_enseignant e ON e.form_st_id = f.id WHERE {where_clause}
        ) AS aggregated_data
        JOIN identifications i ON aggregated_data.identification_id = i.id
        GROUP BY CASE 
            WHEN UPPER(i.regime_gestion) = 'EPR' THEN 'Privé'
            WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN 'NR'
            ELSE 'Public'
        END, COALESCE(NULLIF(i.regime_gestion, ''), 'NR'), sexe, idannee
    ) as subquery
    """

def get_diplome_niveau_maternelle_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM (
            SELECT idannee, diplome, sexe
            FROM (
                -- Sous-requête simplifiée pour le comptage
                SELECT f.idannee, 'D4' AS diplome, 'Hommes' AS sexe FROM formulaires f WHERE {where_clause} GROUP BY f.idannee
                UNION ALL SELECT f.idannee, 'D4', 'Femmes' FROM formulaires f WHERE {where_clause} GROUP BY f.idannee
                UNION ALL SELECT f.idannee, 'EM', 'Hommes' FROM formulaires f WHERE {where_clause} GROUP BY f.idannee
                UNION ALL SELECT f.idannee, 'EM', 'Femmes' FROM formulaires f WHERE {where_clause} GROUP BY f.idannee
                -- Ajouter d'autres combinaisons si nécessaire pour le comptage
            ) AS source_data
            GROUP BY idannee, diplome, sexe WITH ROLLUP
        ) AS results
        WHERE sexe IS NOT NULL OR diplome IS NOT NULL
    ) as subquery
    """

def get_effectif_regime_sexe_province_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM (
            SELECT f.id, f.idannee, f.identification_id, 'Hommes' AS sexe FROM formulaires f LEFT JOIN st1_enseignant e ON e.form_st_id = f.id WHERE {where_clause}
            UNION ALL SELECT f.id, f.idannee, f.identification_id, 'Femmes' AS sexe FROM formulaires f LEFT JOIN st1_enseignant e ON e.form_st_id = f.id WHERE {where_clause}
            UNION ALL SELECT f.id, f.idannee, f.identification_id, 'Total' AS sexe FROM formulaires f LEFT JOIN st1_enseignant e ON e.form_st_id = f.id WHERE {where_clause}
        ) AS aggregated_data
        JOIN identifications i ON aggregated_data.identification_id = i.id
        JOIN provinces p ON i.fk_province_id = p.id
        GROUP BY p.id, p.libelle, sexe, idannee
    ) as subquery
    """

def get_effectif_regime_province_simple_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM (
            SELECT f.id, f.idannee, f.identification_id
            FROM formulaires f
            LEFT JOIN st1_enseignant e ON e.form_st_id = f.id
            WHERE {where_clause}
        ) AS aggregated_data
        JOIN identifications i ON aggregated_data.identification_id = i.id
        JOIN provinces p ON i.fk_province_id = p.id
        GROUP BY p.id, p.libelle, idannee
    ) as subquery
    """

def get_effectif_milieu_public_province_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM (
            SELECT f.id, f.idannee, f.identification_id
            FROM formulaires f
            LEFT JOIN st1_enseignant e ON e.form_st_id = f.id
            WHERE {where_clause}
        ) AS aggregated_data
        JOIN identifications i ON aggregated_data.identification_id = i.id
        JOIN provinces p ON i.fk_province_id = p.id
        WHERE UPPER(i.regime_gestion) != 'EPR' OR i.regime_gestion IS NULL OR i.regime_gestion = ''
        GROUP BY p.id, p.libelle, idannee
    ) as subquery
    """

def get_pourcentage_niveau_national_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        LEFT JOIN st1_enseignant e ON e.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY CASE 
            WHEN UPPER(i.regime_gestion) = 'EPR' THEN 'Privé'
            WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN 'NR'
            ELSE 'Public'
        END, i.regime_gestion, f.idannee
    ) as subquery
    """

def get_normal_enseignants_count_query(where_clause):
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
        cursor.execute("SELECT DISTINCT idannee FROM formulaires WHERE responded = 1 AND UPPER(type) = 'ST1' ORDER BY idannee DESC")
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










# Manuels et guides
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

def guides_manuels_view(request):
    """Vue principale pour les guides et manuels"""
    context = {
        'annees_scolaires': get_annees_scolaires(),
        'provinces': get_provinces(),
        'types_enseignement': get_types_enseignement(),
        'milieux': get_milieux(),
    }
    return render(request, 'annuaires/guides_manuels.html', context)

@csrf_exempt
def get_guides_manuels_data(request):
    """Endpoint AJAX pour récupérer les données des tableaux avec pagination"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rapport_type = data.get('rapport_type')
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
                
            # Filtre type d'enseignement
            type_enseignement = filters.get('type_enseignement')
            if type_enseignement:
                where_conditions.append("UPPER(f.type) = UPPER(%s)")
                params.append(type_enseignement)
                
            # Filtre province
            province = filters.get('province')
            if province:
                where_conditions.append("p.id = %s")
                params.append(province)
            
            # Filtre milieu
            milieu = filters.get('milieu')
            if milieu:
                where_conditions.append("UPPER(i.milieu) = UPPER(%s)")
                params.append(milieu)
            
            # Filtre secteur
            secteur = filters.get('secteur')
            if secteur:
                if secteur.upper() == 'PUBLIC':
                    where_conditions.append("(i.regime_gestion IS NOT NULL AND UPPER(i.regime_gestion) <> 'EPR')")
                elif secteur.upper() == 'PRIVE':
                    where_conditions.append("UPPER(i.regime_gestion) = 'EPR'")
            
            where_clause = " AND ".join(where_conditions)
            
            # Sélectionner la requête en fonction du type de rapport
            if rapport_type == 'guides_secteur':
                query = get_guides_secteur_query(where_clause)
                count_query = get_guides_secteur_count_query(where_clause)
            elif rapport_type == 'guides_province':
                query = get_guides_province_query(where_clause)
                count_query = get_guides_province_count_query(where_clause)
            elif rapport_type == 'manuels_secteur':
                query = get_manuels_secteur_query(where_clause)
                count_query = get_manuels_secteur_count_query(where_clause)
            elif rapport_type == 'manuels_province':
                query = get_manuels_province_query(where_clause)
                count_query = get_manuels_province_count_query(where_clause)
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

def export_guides_excel(request):
    """Export Excel du tableau actuel"""
    try:
        rapport_type = request.GET.get('rapport_type', 'normal')
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
        
        # Appliquer les mêmes filtres
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
        if rapport_type == 'guides_secteur':
            query = get_guides_secteur_query(where_clause)
            title = "Guides par Secteur"
        elif rapport_type == 'guides_province':
            query = get_guides_province_query(where_clause)
            title = "Guides par Province"
        elif rapport_type == 'manuels_secteur':
            query = get_manuels_secteur_query(where_clause)
            title = "Manuels par Secteur"
        elif rapport_type == 'manuels_province':
            query = get_manuels_province_query(where_clause)
            title = "Manuels par Province"
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
        response['Content-Disposition'] = f'attachment; filename="guides_manuels_{rapport_type}_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.xls"'
        
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Guides_Manuels')
        
        # Styles
        header_style = xlwt.easyxf('font: bold on; align: horiz center; pattern: pattern solid, fore_color light_blue;')
        normal_style = xlwt.easyxf('align: horiz left;')
        number_style = xlwt.easyxf('align: horiz right;')
        
        # En-tête du document
        row_num = 0
        ws.write(row_num, 0, f"GUIDES ET MANUELS - {title}", header_style)
        row_num += 1
        ws.write(row_num, 0, f"Généré le: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
        row_num += 2
        
        # En-têtes des colonnes
        for col_num, column_title in enumerate(columns):
            ws.write(row_num, col_num, column_title.replace('_', ' ').title(), header_style)
            ws.col(col_num).width = 4000
        
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

def export_guides_pdf(request):
    """Export PDF du tableau actuel"""
    try:
        rapport_type = request.GET.get('rapport_type', 'normal')
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
        if rapport_type == 'guides_secteur':
            query = get_guides_secteur_query(where_clause)
            title = "Guides par Secteur"
        elif rapport_type == 'guides_province':
            query = get_guides_province_query(where_clause)
            title = "Guides par Province"
        elif rapport_type == 'manuels_secteur':
            query = get_manuels_secteur_query(where_clause)
            title = "Manuels par Secteur"
        elif rapport_type == 'manuels_province':
            query = get_manuels_province_query(where_clause)
            title = "Manuels par Province"
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
        response['Content-Disposition'] = f'attachment; filename="guides_manuels_{rapport_type}_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.pdf"'
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        elements = []
        
        styles = getSampleStyleSheet()
        
        # Titre
        title_text = f"GUIDES ET MANUELS - {title}"
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
                ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
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

def export_guides_csv(request):
    """Export CSV du tableau actuel"""
    try:
        rapport_type = request.GET.get('rapport_type', 'normal')
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
        if rapport_type == 'guides_secteur':
            query = get_guides_secteur_query(where_clause)
            title = "Guides par Secteur"
        elif rapport_type == 'guides_province':
            query = get_guides_province_query(where_clause)
            title = "Guides par Province"
        elif rapport_type == 'manuels_secteur':
            query = get_manuels_secteur_query(where_clause)
            title = "Manuels par Secteur"
        elif rapport_type == 'manuels_province':
            query = get_manuels_province_query(where_clause)
            title = "Manuels par Province"
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
        response['Content-Disposition'] = f'attachment; filename="guides_manuels_{rapport_type}_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.csv"'
        
        response.write(u'\ufeff'.encode('utf8'))  # BOM pour Excel
        writer = csv.writer(response)
        
        # En-tête
        writer.writerow([f"GUIDES ET MANUELS - {title}"])
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
def get_guides_secteur_query(where_clause):
    return f"""
    SELECT
        CASE
            WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
            ELSE i.secteur_enseignement
        END AS secteur,
        'Autres' AS type_guide,
        CASE
            WHEN SUM(COALESCE(m.guides_autres_1ere, 0)) = 0 THEN 'NR'
            ELSE CAST(SUM(COALESCE(m.guides_autres_1ere, 0)) AS CHAR)
        END AS "1ere_maternelle",
        CASE
            WHEN SUM(COALESCE(m.guides_autres_2eme, 0)) = 0 THEN 'NR'
            ELSE CAST(SUM(COALESCE(m.guides_autres_2eme, 0)) AS CHAR)
        END AS "2eme_maternelle",
        CASE
            WHEN SUM(COALESCE(m.guides_autres_3eme, 0)) = 0 THEN 'NR'
            ELSE CAST(SUM(COALESCE(m.guides_autres_3eme, 0)) AS CHAR)
        END AS "3eme_maternelle",
        CASE
            WHEN SUM(COALESCE(m.guides_autres_1ere, 0) + COALESCE(m.guides_autres_2eme, 0) + COALESCE(m.guides_autres_3eme, 0)) = 0 THEN 'NR'
            ELSE CAST(SUM(COALESCE(m.guides_autres_1ere, 0) + COALESCE(m.guides_autres_2eme, 0) + COALESCE(m.guides_autres_3eme, 0)) AS CHAR)
        END AS "total_autres"
    FROM formulaires f
    LEFT JOIN st1_guides_educateurs m ON m.form_st_id = f.id
    JOIN identifications i ON f.identification_id = i.id
    WHERE {where_clause} AND UPPER(f.type) = 'ST1'
    GROUP BY
        CASE
            WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
            ELSE i.secteur_enseignement
        END

    UNION ALL

    SELECT
        CASE
            WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
            ELSE i.secteur_enseignement
        END AS secteur,
        'Comptage' AS type_guide,
        CASE
            WHEN SUM(COALESCE(m.guides_comptage_1ere, 0)) = 0 THEN 'NR'
            ELSE CAST(SUM(COALESCE(m.guides_comptage_1ere, 0)) AS CHAR)
        END AS "1ere_maternelle",
        CASE
            WHEN SUM(COALESCE(m.guides_comptage_2eme, 0)) = 0 THEN 'NR'
            ELSE CAST(SUM(COALESCE(m.guides_comptage_2eme, 0)) AS CHAR)
        END AS "2eme_maternelle",
        CASE
            WHEN SUM(COALESCE(m.guides_comptage_3eme, 0)) = 0 THEN 'NR'
            ELSE CAST(SUM(COALESCE(m.guides_comptage_3eme, 0)) AS CHAR)
        END AS "3eme_maternelle",
        CASE
            WHEN SUM(COALESCE(m.guides_comptage_1ere, 0) + COALESCE(m.guides_comptage_2eme, 0) + COALESCE(m.guides_comptage_3eme, 0)) = 0 THEN 'NR'
            ELSE CAST(SUM(COALESCE(m.guides_comptage_1ere, 0) + COALESCE(m.guides_comptage_2eme, 0) + COALESCE(m.guides_comptage_3eme, 0)) AS CHAR)
        END AS "total_comptage"
    FROM formulaires f
    LEFT JOIN st1_guides_educateurs m ON m.form_st_id = f.id
    JOIN identifications i ON f.identification_id = i.id
    WHERE {where_clause} AND UPPER(f.type) = 'ST1'
    GROUP BY
        CASE
            WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
            ELSE i.secteur_enseignement
        END

    UNION ALL

    SELECT
        CASE
            WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
            ELSE i.secteur_enseignement
        END AS secteur,
        'Etude du Milieu' AS type_guide,
        CASE
            WHEN SUM(COALESCE(m.guides_etude_du_milieu_1ere, 0)) = 0 THEN 'NR'
            ELSE CAST(SUM(COALESCE(m.guides_etude_du_milieu_1ere, 0)) AS CHAR)
        END AS "1ere_maternelle",
        CASE
            WHEN SUM(COALESCE(m.guides_etude_du_milieu_2eme, 0)) = 0 THEN 'NR'
            ELSE CAST(SUM(COALESCE(m.guides_etude_du_milieu_2eme, 0)) AS CHAR)
        END AS "2eme_maternelle",
        CASE
            WHEN SUM(COALESCE(m.guides_etude_du_milieu_3eme, 0)) = 0 THEN 'NR'
            ELSE CAST(SUM(COALESCE(m.guides_etude_du_milieu_3eme, 0)) AS CHAR)
        END AS "3eme_maternelle",
        CASE
            WHEN SUM(COALESCE(m.guides_etude_du_milieu_1ere, 0) + COALESCE(m.guides_etude_du_milieu_2eme, 0) + COALESCE(m.guides_etude_du_milieu_3eme, 0)) = 0 THEN 'NR'
            ELSE CAST(SUM(COALESCE(m.guides_etude_du_milieu_1ere, 0) + COALESCE(m.guides_etude_du_milieu_2eme, 0) + COALESCE(m.guides_etude_du_milieu_3eme, 0)) AS CHAR)
        END AS "total_etude_du_milieu"
    FROM formulaires f
    LEFT JOIN st1_guides_educateurs m ON m.form_st_id = f.id
    JOIN identifications i ON f.identification_id = i.id
    WHERE {where_clause} AND UPPER(f.type) = 'ST1'
    GROUP BY
        CASE
            WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
            ELSE i.secteur_enseignement
        END

    UNION ALL

    SELECT
        CASE
            WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
            ELSE i.secteur_enseignement
        END AS secteur,
        'Eveil' AS type_guide,
        CASE
            WHEN SUM(COALESCE(m.guides_eveil_1ere, 0)) = 0 THEN 'NR'
            ELSE CAST(SUM(COALESCE(m.guides_eveil_1ere, 0)) AS CHAR)
        END AS "1ere_maternelle",
        CASE
            WHEN SUM(COALESCE(m.guides_eveil_2eme, 0)) = 0 THEN 'NR'
            ELSE CAST(SUM(COALESCE(m.guides_eveil_2eme, 0)) AS CHAR)
        END AS "2eme_maternelle",
        CASE
            WHEN SUM(COALESCE(m.guides_eveil_3eme, 0)) = 0 THEN 'NR'
            ELSE CAST(SUM(COALESCE(m.guides_eveil_3eme, 0)) AS CHAR)
        END AS "3eme_maternelle",
        CASE
            WHEN SUM(COALESCE(m.guides_eveil_1ere, 0) + COALESCE(m.guides_eveil_2eme, 0) + COALESCE(m.guides_eveil_3eme, 0)) = 0 THEN 'NR'
            ELSE CAST(SUM(COALESCE(m.guides_eveil_1ere, 0) + COALESCE(m.guides_eveil_2eme, 0) + COALESCE(m.guides_eveil_3eme, 0)) AS CHAR)
        END AS "total_eveil"
    FROM formulaires f
    LEFT JOIN st1_guides_educateurs m ON m.form_st_id = f.id
    JOIN identifications i ON f.identification_id = i.id
    WHERE {where_clause} AND UPPER(f.type) = 'ST1'
    GROUP BY
        CASE
            WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
            ELSE i.secteur_enseignement
        END

    UNION ALL

    SELECT
        CASE
            WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
            ELSE i.secteur_enseignement
        END AS secteur,
        'Français' AS type_guide,
        CASE
            WHEN SUM(COALESCE(m.guides_francais_1ere, 0)) = 0 THEN 'NR'
            ELSE CAST(SUM(COALESCE(m.guides_francais_1ere, 0)) AS CHAR)
        END AS "1ere_maternelle",
        CASE
            WHEN SUM(COALESCE(m.guides_francais_2eme, 0)) = 0 THEN 'NR'
            ELSE CAST(SUM(COALESCE(m.guides_francais_2eme, 0)) AS CHAR)
        END AS "2eme_maternelle",
        CASE
            WHEN SUM(COALESCE(m.guides_francais_3eme, 0)) = 0 THEN 'NR'
            ELSE CAST(SUM(COALESCE(m.guides_francais_3eme, 0)) AS CHAR)
        END AS "3eme_maternelle",
        CASE
            WHEN SUM(COALESCE(m.guides_francais_1ere, 0) + COALESCE(m.guides_francais_2eme, 0) + COALESCE(m.guides_francais_3eme, 0)) = 0 THEN 'NR'
            ELSE CAST(SUM(COALESCE(m.guides_francais_1ere, 0) + COALESCE(m.guides_francais_2eme, 0) + COALESCE(m.guides_francais_3eme, 0)) AS CHAR)
        END AS "total_francais"
    FROM formulaires f
    LEFT JOIN st1_guides_educateurs m ON m.form_st_id = f.id
    JOIN identifications i ON f.identification_id = i.id
    WHERE {where_clause} AND UPPER(f.type) = 'ST1'
    GROUP BY
        CASE
            WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
            ELSE i.secteur_enseignement
        END

    UNION ALL

    SELECT
        CASE
            WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
            ELSE i.secteur_enseignement
        END AS secteur,
        'Thèmes Transversaux' AS type_guide,
        CASE
            WHEN SUM(COALESCE(m.guides_themes_transversaux_1ere, 0)) = 0 THEN 'NR'
            ELSE CAST(SUM(COALESCE(m.guides_themes_transversaux_1ere, 0)) AS CHAR)
        END AS "1ere_maternelle",
        CASE
            WHEN SUM(COALESCE(m.guides_themes_transversaux_2eme, 0)) = 0 THEN 'NR'
            ELSE CAST(SUM(COALESCE(m.guides_themes_transversaux_2eme, 0)) AS CHAR)
        END AS "2eme_maternelle",
        CASE
            WHEN SUM(COALESCE(m.guides_themes_transversaux_3eme, 0)) = 0 THEN 'NR'
            ELSE CAST(SUM(COALESCE(m.guides_themes_transversaux_3eme, 0)) AS CHAR)
        END AS "3eme_maternelle",
        CASE
            WHEN SUM(COALESCE(m.guides_themes_transversaux_1ere, 0) + COALESCE(m.guides_themes_transversaux_2eme, 0) + COALESCE(m.guides_themes_transversaux_3eme, 0)) = 0 THEN 'NR'
            ELSE CAST(SUM(COALESCE(m.guides_themes_transversaux_1ere, 0) + COALESCE(m.guides_themes_transversaux_2eme, 0) + COALESCE(m.guides_themes_transversaux_3eme, 0)) AS CHAR)
        END AS "total_themes_transversaux"
    FROM formulaires f
    LEFT JOIN st1_guides_educateurs m ON m.form_st_id = f.id
    JOIN identifications i ON f.identification_id = i.id
    WHERE {where_clause} AND UPPER(f.type) = 'ST1'
    GROUP BY
        CASE
            WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
            ELSE i.secteur_enseignement
        END

    ORDER BY secteur, type_guide;
    """

def get_guides_province_query(where_clause):
    return f"""
    SELECT
        p.id AS province_id,
        p.libelle AS province,
        'Autres' AS type_guide,
        SUM(COALESCE(m.guides_autres_1ere, 0)) AS "1ere_maternelle",
        SUM(COALESCE(m.guides_autres_2eme, 0)) AS "2eme_maternelle",
        SUM(COALESCE(m.guides_autres_3eme, 0)) AS "3eme_maternelle",
        SUM(COALESCE(m.guides_autres_1ere, 0) + COALESCE(m.guides_autres_2eme, 0) + COALESCE(m.guides_autres_3eme, 0)) AS "total_autres"
    FROM formulaires f
    LEFT JOIN st1_guides_educateurs m ON m.form_st_id = f.id
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE {where_clause} AND UPPER(f.type) = 'ST1'
    GROUP BY p.id, p.libelle

    UNION ALL

    SELECT
        p.id AS province_id,
        p.libelle AS province,
        'Comptage' AS type_guide,
        SUM(COALESCE(m.guides_comptage_1ere, 0)) AS "1ere_maternelle",
        SUM(COALESCE(m.guides_comptage_2eme, 0)) AS "2eme_maternelle",
        SUM(COALESCE(m.guides_comptage_3eme, 0)) AS "3eme_maternelle",
        SUM(COALESCE(m.guides_comptage_1ere, 0) + COALESCE(m.guides_comptage_2eme, 0) + COALESCE(m.guides_comptage_3eme, 0)) AS "total_comptage"
    FROM formulaires f
    LEFT JOIN st1_guides_educateurs m ON m.form_st_id = f.id
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE {where_clause} AND UPPER(f.type) = 'ST1'
    GROUP BY p.id, p.libelle

    UNION ALL

    SELECT
        p.id AS province_id,
        p.libelle AS province,
        'Etude du Milieu' AS type_guide,
        SUM(COALESCE(m.guides_etude_du_milieu_1ere, 0)) AS "1ere_maternelle",
        SUM(COALESCE(m.guides_etude_du_milieu_2eme, 0)) AS "2eme_maternelle",
        SUM(COALESCE(m.guides_etude_du_milieu_3eme, 0)) AS "3eme_maternelle",
        SUM(COALESCE(m.guides_etude_du_milieu_1ere, 0) + COALESCE(m.guides_etude_du_milieu_2eme, 0) + COALESCE(m.guides_etude_du_milieu_3eme, 0)) AS "total_etude_du_milieu"
    FROM formulaires f
    LEFT JOIN st1_guides_educateurs m ON m.form_st_id = f.id
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE {where_clause} AND UPPER(f.type) = 'ST1'
    GROUP BY p.id, p.libelle

    UNION ALL

    SELECT
        p.id AS province_id,
        p.libelle AS province,
        'Eveil' AS type_guide,
        SUM(COALESCE(m.guides_eveil_1ere, 0)) AS "1ere_maternelle",
        SUM(COALESCE(m.guides_eveil_2eme, 0)) AS "2eme_maternelle",
        SUM(COALESCE(m.guides_eveil_3eme, 0)) AS "3eme_maternelle",
        SUM(COALESCE(m.guides_eveil_1ere, 0) + COALESCE(m.guides_eveil_2eme, 0) + COALESCE(m.guides_eveil_3eme, 0)) AS "total_eveil"
    FROM formulaires f
    LEFT JOIN st1_guides_educateurs m ON m.form_st_id = f.id
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE {where_clause} AND UPPER(f.type) = 'ST1'
    GROUP BY p.id, p.libelle

    UNION ALL

    SELECT
        p.id AS province_id,
        p.libelle AS province,
        'Français' AS type_guide,
        SUM(COALESCE(m.guides_francais_1ere, 0)) AS "1ere_maternelle",
        SUM(COALESCE(m.guides_francais_2eme, 0)) AS "2eme_maternelle",
        SUM(COALESCE(m.guides_francais_3eme, 0)) AS "3eme_maternelle",
        SUM(COALESCE(m.guides_francais_1ere, 0) + COALESCE(m.guides_francais_2eme, 0) + COALESCE(m.guides_francais_3eme, 0)) AS "total_francais"
    FROM formulaires f
    LEFT JOIN st1_guides_educateurs m ON m.form_st_id = f.id
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE {where_clause} AND UPPER(f.type) = 'ST1'
    GROUP BY p.id, p.libelle

    UNION ALL

    SELECT
        p.id AS province_id,
        p.libelle AS province,
        'Thèmes Transversaux' AS type_guide,
        SUM(COALESCE(m.guides_themes_transversaux_1ere, 0)) AS "1ere_maternelle",
        SUM(COALESCE(m.guides_themes_transversaux_2eme, 0)) AS "2eme_maternelle",
        SUM(COALESCE(m.guides_themes_transversaux_3eme, 0)) AS "3eme_maternelle",
        SUM(COALESCE(m.guides_themes_transversaux_1ere, 0) + COALESCE(m.guides_themes_transversaux_2eme, 0) + COALESCE(m.guides_themes_transversaux_3eme, 0)) AS "total_themes_transversaux"
    FROM formulaires f
    LEFT JOIN st1_guides_educateurs m ON m.form_st_id = f.id
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE {where_clause} AND UPPER(f.type) = 'ST1'
    GROUP BY p.id, p.libelle

    ORDER BY province_id, type_guide;
    """

def get_manuels_secteur_query(where_clause):
    return f"""
    SELECT
        CASE 
            WHEN UPPER(i.regime_gestion) = 'EPR' THEN 'Privé'
            WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN 'NR'
            ELSE 'Public'
        END AS secteur,
        'Autres' AS "type_manuel",
        SUM(COALESCE(m.manuels_autres_1ere, 0)) AS "1ere_maternelle",
        SUM(COALESCE(m.manuels_autres_2eme, 0)) AS "2eme_maternelle",
        SUM(COALESCE(m.manuels_autres_3eme, 0)) AS "3eme_maternelle",
        SUM(COALESCE(m.manuels_autres_1ere, 0) +
            COALESCE(m.manuels_autres_2eme, 0) +
            COALESCE(m.manuels_autres_3eme, 0)) AS "total_general"
    FROM formulaires f
    LEFT JOIN st1_manuels_enfants m ON m.form_st_id = f.id
    JOIN identifications i ON f.identification_id = i.id
    WHERE {where_clause} AND UPPER(f.type) = 'ST1'
    GROUP BY secteur, "type_manuel"

    UNION ALL

    SELECT
        CASE 
            WHEN UPPER(i.regime_gestion) = 'EPR' THEN 'Privé'
            WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN 'NR'
            ELSE 'Public'
        END AS secteur,
        'Comptage' AS "type_manuel",
        SUM(COALESCE(m.manuels_comptage_1ere, 0)) AS "1ere_maternelle",
        SUM(COALESCE(m.manuels_comptage_2eme, 0)) AS "2eme_maternelle",
        SUM(COALESCE(m.manuels_comptage_3eme, 0)) AS "3eme_maternelle",
        SUM(COALESCE(m.manuels_comptage_1ere, 0) +
            COALESCE(m.manuels_comptage_2eme, 0) +
            COALESCE(m.manuels_comptage_3eme, 0)) AS "total_general"
    FROM formulaires f
    LEFT JOIN st1_manuels_enfants m ON m.form_st_id = f.id
    JOIN identifications i ON f.identification_id = i.id
    WHERE {where_clause} AND UPPER(f.type) = 'ST1'
    GROUP BY secteur, "type_manuel"

    UNION ALL

    SELECT
        CASE 
            WHEN UPPER(i.regime_gestion) = 'EPR' THEN 'Privé'
            WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN 'NR'
            ELSE 'Public'
        END AS secteur,
        'Etude du milieu' AS "type_manuel",
        SUM(COALESCE(m.manuels_etude_du_milieu_1ere, 0)) AS "1ere_maternelle",
        SUM(COALESCE(m.manuels_etude_du_milieu_2eme, 0)) AS "2eme_maternelle",
        SUM(COALESCE(m.manuels_etude_du_milieu_3eme, 0)) AS "3eme_maternelle",
        SUM(COALESCE(m.manuels_etude_du_milieu_1ere, 0) +
            COALESCE(m.manuels_etude_du_milieu_2eme, 0) +
            COALESCE(m.manuels_etude_du_milieu_3eme, 0)) AS "total_general"
    FROM formulaires f
    LEFT JOIN st1_manuels_enfants m ON m.form_st_id = f.id
    JOIN identifications i ON f.identification_id = i.id
    WHERE {where_clause} AND UPPER(f.type) = 'ST1'
    GROUP BY secteur, "type_manuel"

    UNION ALL

    SELECT
        CASE 
            WHEN UPPER(i.regime_gestion) = 'EPR' THEN 'Privé'
            WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN 'NR'
            ELSE 'Public'
        END AS secteur,
        'Eveil' AS "type_manuel",
        SUM(COALESCE(m.manuels_eveil_1ere, 0)) AS "1ere_maternelle",
        SUM(COALESCE(m.manuels_eveil_2eme, 0)) AS "2eme_maternelle",
        SUM(COALESCE(m.manuels_eveil_3eme, 0)) AS "3eme_maternelle",
        SUM(COALESCE(m.manuels_eveil_1ere, 0) +
            COALESCE(m.manuels_eveil_2eme, 0) +
            COALESCE(m.manuels_eveil_3eme, 0)) AS "total_general"
    FROM formulaires f
    LEFT JOIN st1_manuels_enfants m ON m.form_st_id = f.id
    JOIN identifications i ON f.identification_id = i.id
    WHERE {where_clause} AND UPPER(f.type) = 'ST1'
    GROUP BY secteur, "type_manuel"

    UNION ALL

    SELECT
        CASE 
            WHEN UPPER(i.regime_gestion) = 'EPR' THEN 'Privé'
            WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN 'NR'
            ELSE 'Public'
        END AS secteur,
        'Français' AS "type_manuel",
        SUM(COALESCE(m.manuels_francais_1ere, 0)) AS "1ere_maternelle",
        SUM(COALESCE(m.manuels_francais_2eme, 0)) AS "2eme_maternelle",
        SUM(COALESCE(m.manuels_francais_3eme, 0)) AS "3eme_maternelle",
        SUM(COALESCE(m.manuels_francais_1ere, 0) +
            COALESCE(m.manuels_francais_2eme, 0) +
            COALESCE(m.manuels_francais_3eme, 0)) AS "total_general"
    FROM formulaires f
    LEFT JOIN st1_manuels_enfants m ON m.form_st_id = f.id
    JOIN identifications i ON f.identification_id = i.id
    WHERE {where_clause} AND UPPER(f.type) = 'ST1'
    GROUP BY secteur, "type_manuel"

    UNION ALL

    SELECT
        CASE 
            WHEN UPPER(i.regime_gestion) = 'EPR' THEN 'Privé'
            WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN 'NR'
            ELSE 'Public'
        END AS secteur,
        'Thèmes transversaux' AS "type_manuel",
        SUM(COALESCE(m.manuels_themes_transversaux_1ere, 0)) AS "1ere_maternelle",
        SUM(COALESCE(m.manuels_themes_transversaux_2eme, 0)) AS "2eme_maternelle",
        SUM(COALESCE(m.manuels_themes_transversaux_3eme, 0)) AS "3eme_maternelle",
        SUM(COALESCE(m.manuels_themes_transversaux_1ere, 0) +
            COALESCE(m.manuels_themes_transversaux_2eme, 0) +
            COALESCE(m.manuels_themes_transversaux_3eme, 0)) AS "total_general"
    FROM formulaires f
    LEFT JOIN st1_manuels_enfants m ON m.form_st_id = f.id
    JOIN identifications i ON f.identification_id = i.id
    WHERE {where_clause} AND UPPER(f.type) = 'ST1'
    GROUP BY secteur, "type_manuel"

    ORDER BY 
        CASE WHEN secteur = 'Public' THEN 1
             WHEN secteur = 'Privé' THEN 2
             ELSE 3 END,
        CASE WHEN "type_manuel" = 'Autres' THEN 1
             WHEN "type_manuel" = 'Comptage' THEN 2
             WHEN "type_manuel" = 'Etude du milieu' THEN 3
             WHEN "type_manuel" = 'Eveil' THEN 4
             WHEN "type_manuel" = 'Français' THEN 5
             ELSE 6 END;
    """

def get_manuels_province_query(where_clause):
    return f"""
    SELECT
        p.id,
        p.libelle AS province,
        'Autres' AS "type_manuel",
        SUM(COALESCE(m.manuels_autres_1ere, 0)) AS "1ere_maternelle",
        SUM(COALESCE(m.manuels_autres_2eme, 0)) AS "2eme_maternelle",
        SUM(COALESCE(m.manuels_autres_3eme, 0)) AS "3eme_maternelle",
        SUM(COALESCE(m.manuels_autres_1ere, 0) +
            COALESCE(m.manuels_autres_2eme, 0) +
            COALESCE(m.manuels_autres_3eme, 0)) AS "total_general"
    FROM formulaires f
    LEFT JOIN st1_manuels_enfants m ON m.form_st_id = f.id
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE {where_clause} AND UPPER(f.type) = 'ST1'
    GROUP BY p.id, p.libelle, "type_manuel"

    UNION ALL

    SELECT
        p.id,
        p.libelle AS province,
        'Comptage' AS "type_manuel",
        SUM(COALESCE(m.manuels_comptage_1ere, 0)) AS "1ere_maternelle",
        SUM(COALESCE(m.manuels_comptage_2eme, 0)) AS "2eme_maternelle",
        SUM(COALESCE(m.manuels_comptage_3eme, 0)) AS "3eme_maternelle",
        SUM(COALESCE(m.manuels_comptage_1ere, 0) +
            COALESCE(m.manuels_comptage_2eme, 0) +
            COALESCE(m.manuels_comptage_3eme, 0)) AS "total_general"
    FROM formulaires f
    LEFT JOIN st1_manuels_enfants m ON m.form_st_id = f.id
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE {where_clause} AND UPPER(f.type) = 'ST1'
    GROUP BY p.id, p.libelle, "type_manuel"

    UNION ALL

    SELECT
        p.id,
        p.libelle AS province,
        'Etude du milieu' AS "type_manuel",
        SUM(COALESCE(m.manuels_etude_du_milieu_1ere, 0)) AS "1ere_maternelle",
        SUM(COALESCE(m.manuels_etude_du_milieu_2eme, 0)) AS "2eme_maternelle",
        SUM(COALESCE(m.manuels_etude_du_milieu_3eme, 0)) AS "3eme_maternelle",
        SUM(COALESCE(m.manuels_etude_du_milieu_1ere, 0) +
            COALESCE(m.manuels_etude_du_milieu_2eme, 0) +
            COALESCE(m.manuels_etude_du_milieu_3eme, 0)) AS "total_general"
    FROM formulaires f
    LEFT JOIN st1_manuels_enfants m ON m.form_st_id = f.id
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE {where_clause} AND UPPER(f.type) = 'ST1'
    GROUP BY p.id, p.libelle, "type_manuel"

    UNION ALL

    SELECT
        p.id,
        p.libelle AS province,
        'Eveil' AS "type_manuel",
        SUM(COALESCE(m.manuels_eveil_1ere, 0)) AS "1ere_maternelle",
        SUM(COALESCE(m.manuels_eveil_2eme, 0)) AS "2eme_maternelle",
        SUM(COALESCE(m.manuels_eveil_3eme, 0)) AS "3eme_maternelle",
        SUM(COALESCE(m.manuels_eveil_1ere, 0) +
            COALESCE(m.manuels_eveil_2eme, 0) +
            COALESCE(m.manuels_eveil_3eme, 0)) AS "total_general"
    FROM formulaires f
    LEFT JOIN st1_manuels_enfants m ON m.form_st_id = f.id
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE {where_clause} AND UPPER(f.type) = 'ST1'
    GROUP BY p.id, p.libelle, "type_manuel"

    UNION ALL

    SELECT
        p.id,
        p.libelle AS province,
        'Français' AS "type_manuel",
        SUM(COALESCE(m.manuels_francais_1ere, 0)) AS "1ere_maternelle",
        SUM(COALESCE(m.manuels_francais_2eme, 0)) AS "2eme_maternelle",
        SUM(COALESCE(m.manuels_francais_3eme, 0)) AS "3eme_maternelle",
        SUM(COALESCE(m.manuels_francais_1ere, 0) +
            COALESCE(m.manuels_francais_2eme, 0) +
            COALESCE(m.manuels_francais_3eme, 0)) AS "total_general"
    FROM formulaires f
    LEFT JOIN st1_manuels_enfants m ON m.form_st_id = f.id
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE {where_clause} AND UPPER(f.type) = 'ST1'
    GROUP BY p.id, p.libelle, "type_manuel"

    UNION ALL

    SELECT
        p.id,
        p.libelle AS province,
        'Thèmes transversaux' AS "type_manuel",
        SUM(COALESCE(m.manuels_themes_transversaux_1ere, 0)) AS "1ere_maternelle",
        SUM(COALESCE(m.manuels_themes_transversaux_2eme, 0)) AS "2eme_maternelle",
        SUM(COALESCE(m.manuels_themes_transversaux_3eme, 0)) AS "3eme_maternelle",
        SUM(COALESCE(m.manuels_themes_transversaux_1ere, 0) +
            COALESCE(m.manuels_themes_transversaux_2eme, 0) +
            COALESCE(m.manuels_themes_transversaux_3eme, 0)) AS "total_general"
    FROM formulaires f
    LEFT JOIN st1_manuels_enfants m ON m.form_st_id = f.id
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE {where_clause} AND UPPER(f.type) = 'ST1'
    GROUP BY p.id, p.libelle, "type_manuel"

    ORDER BY 
        1,  -- Position de la colonne id
        3;  -- Position de la colonne type manuel
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
def get_guides_secteur_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM formulaires f
        LEFT JOIN st1_guides_educateurs m ON m.form_st_id = f.id
        JOIN identifications i ON f.identification_id = i.id
        WHERE {where_clause} AND UPPER(f.type) = 'ST1'
        GROUP BY 
            CASE
                WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
                ELSE i.secteur_enseignement
            END,
            'Autres'
    ) as subquery
    """

def get_guides_province_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM formulaires f
        LEFT JOIN st1_guides_educateurs m ON m.form_st_id = f.id
        JOIN identifications i ON f.identification_id = i.id
        JOIN provinces p ON i.fk_province_id = p.id
        WHERE {where_clause} AND UPPER(f.type) = 'ST1'
        GROUP BY p.id, p.libelle, 'Autres'
    ) as subquery
    """

def get_manuels_secteur_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM formulaires f
        LEFT JOIN st1_manuels_enfants m ON m.form_st_id = f.id
        JOIN identifications i ON f.identification_id = i.id
        WHERE {where_clause} AND UPPER(f.type) = 'ST1'
        GROUP BY 
            CASE 
                WHEN UPPER(i.regime_gestion) = 'EPR' THEN 'Privé'
                WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' THEN 'NR'
                ELSE 'Public'
            END,
            'Autres'
    ) as subquery
    """

def get_manuels_province_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM formulaires f
        LEFT JOIN st1_manuels_enfants m ON m.form_st_id = f.id
        JOIN identifications i ON f.identification_id = i.id
        JOIN provinces p ON i.fk_province_id = p.id
        WHERE {where_clause} AND UPPER(f.type) = 'ST1'
        GROUP BY p.id, p.libelle, 'Autres'
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
















#LOCAUX
# locaux_views.py
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

def annuaire_locaux(request):
    """Vue principale pour l'annuaire des locaux"""
    context = {
        'annees_scolaires': get_annees_scolaires(),
        'provinces': get_provinces(),
        'types_enseignement': ['ST1'],  # Seulement ST1 pour les locaux
        'milieux': get_milieux(),
    }
    return render(request, 'annuaires/annuaire_locaux.html', context)

@csrf_exempt
def get_locaux_data(request):
    """Endpoint AJAX pour récupérer les données des locaux avec pagination"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rapport_type = data.get('rapport_type', 'locaux_par_province')
            filters = data.get('filters', {})
            page = int(data.get('page', 1))
            page_size = int(data.get('page_size', 10))
            
            # Calculer l'offset pour la pagination
            offset = (page - 1) * page_size
            
            # Construire les conditions WHERE
            where_conditions, params = build_locaux_conditions(filters)
            
            # Sélectionner la requête en fonction du type de rapport
            if rapport_type == 'locaux_par_province':
                query = get_locaux_province_query(where_clause=where_conditions)
                count_query = get_locaux_province_count_query(where_clause=where_conditions)
            elif rapport_type == 'locaux_par_secteur':
                query = get_locaux_secteur_query(where_clause=where_conditions)
                count_query = get_locaux_secteur_count_query(where_clause=where_conditions)
            elif rapport_type == 'locaux_par_milieu':
                query = get_locaux_milieu_query(where_clause=where_conditions)
                count_query = get_locaux_milieu_count_query(where_clause=where_conditions)
            elif rapport_type == 'synthese_province':
                query = get_synthese_province_query(where_clause=where_conditions)
                count_query = get_synthese_province_count_query(where_clause=where_conditions)
            else:
                query = get_locaux_province_query(where_clause=where_conditions)
                count_query = get_locaux_province_count_query(where_clause=where_conditions)
            
            # Exécuter la requête de comptage pour le total
            with connection.cursor() as cursor:
                cursor.execute(count_query, params)
                total_count = cursor.fetchone()[0]
            
            # Ajouter la pagination à la requête principale si nécessaire
            if 'LIMIT' not in query.upper():
                query += f" LIMIT {page_size} OFFSET {offset}"
            
            # Exécuter la requête principale
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

def build_locaux_conditions(filters):
    """Construit les conditions WHERE pour les requêtes des locaux"""
    where_conditions = ["f.responded = 1", "UPPER(f.type) = 'ST1'"]
    params = []
    
    # Filtre année scolaire
    annee = filters.get('annee')
    if annee:
        where_conditions.append("f.idannee = %s")
        params.append(annee)
        
    # Filtre province
    province = filters.get('province')
    if province:
        where_conditions.append("p.id = %s")
        params.append(province)
    
    # Filtre milieu
    milieu = filters.get('milieu')
    if milieu:
        where_conditions.append("UPPER(i.milieu) = UPPER(%s)")
        params.append(milieu)
    
    # Filtre secteur
    secteur = filters.get('secteur')
    if secteur:
        if secteur.upper() == 'PUBLIC':
            where_conditions.append("(i.regime_gestion IS NOT NULL AND UPPER(i.regime_gestion) <> 'EPR')")
        elif secteur.upper() == 'PRIVE':
            where_conditions.append("UPPER(i.regime_gestion) = 'EPR'")
    
    where_clause = " AND ".join(where_conditions)
    return where_clause, params

# REQUÊTES SQL POUR LES DIFFÉRENTS RAPPORTS

def get_locaux_province_query(where_clause):
    return f"""
    WITH locaux_par_type AS (
        -- Bureaux
        SELECT
            f.idannee AS annee,
            p.id AS id_province,
            p.libelle AS province,
            'Bureaux' AS type_locaux,
            SUM(COALESCE(l.bureau_dur_bon, 0) + COALESCE(l.bureau_dur_mauvais, 0)) AS en_dur,
            SUM(COALESCE(l.bureau_semidur_bon, 0) + COALESCE(l.bureau_semidur_mauvais, 0)) AS semi_dur,
            SUM(COALESCE(l.bureau_terre_bon, 0) + COALESCE(l.bureau_terre_mauvais, 0)) AS terre_battu,
            SUM(COALESCE(l.bureau_paille_bon, 0) + COALESCE(l.bureau_paille_mauvais, 0)) AS paille_feuillage
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        JOIN provinces p ON i.fk_province_id = p.id
        LEFT JOIN st1_locaux l ON l.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY f.idannee, p.id, p.libelle

        UNION ALL

        -- Magasins
        SELECT
            f.idannee AS annee,
            p.id AS id_province,
            p.libelle AS province,
            'Magasins' AS type_locaux,
            SUM(COALESCE(l.magasin_dur_bon, 0) + COALESCE(l.magasin_dur_mauvais, 0)) AS en_dur,
            SUM(COALESCE(l.magasin_semidur_bon, 0) + COALESCE(l.magasin_semidur_mauvais, 0)) AS semi_dur,
            SUM(COALESCE(l.magasin_terre_bon, 0) + COALESCE(l.magasin_terre_mauvais, 0)) AS terre_battu,
            SUM(COALESCE(l.magasin_paille_bon, 0) + COALESCE(l.magasin_paille_mauvais, 0)) AS paille_feuillage
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        JOIN provinces p ON i.fk_province_id = p.id
        LEFT JOIN st1_locaux l ON l.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY f.idannee, p.id, p.libelle

        UNION ALL

        -- Salles d'attente
        SELECT
            f.idannee AS annee,
            p.id AS id_province,
            p.libelle AS province,
            'Salles d''attente' AS type_locaux,
            SUM(COALESCE(l.salle_attente_dur_bon, 0) + COALESCE(l.salle_attente_dur_mauvais, 0)) AS en_dur,
            SUM(COALESCE(l.salle_attente_semidur_bon, 0) + COALESCE(l.salle_attente_semidur_mauvais, 0)) AS semi_dur,
            SUM(COALESCE(l.salle_attente_terre_bon, 0) + COALESCE(l.salle_attente_terre_mauvais, 0)) AS terre_battu,
            SUM(COALESCE(l.salle_attente_paille_bon, 0) + COALESCE(l.salle_attente_paille_mauvais, 0)) AS paille_feuillage
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        JOIN provinces p ON i.fk_province_id = p.id
        LEFT JOIN st1_locaux l ON l.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY f.idannee, p.id, p.libelle

        UNION ALL

        -- Salles de jeux/sport
        SELECT
            f.idannee AS annee,
            p.id AS id_province,
            p.libelle AS province,
            'Salles de jeux/sport' AS type_locaux,
            SUM(COALESCE(l.salle_jeux_dur_bon, 0) + COALESCE(l.salle_jeux_dur_mauvais, 0)) AS en_dur,
            SUM(COALESCE(l.salle_jeux_semidur_bon, 0) + COALESCE(l.salle_jeux_semidur_mauvais, 0)) AS semi_dur,
            SUM(COALESCE(l.salle_jeux_terre_bon, 0) + COALESCE(l.salle_jeux_terre_mauvais, 0)) AS terre_battu,
            SUM(COALESCE(l.salle_jeux_paille_bon, 0) + COALESCE(l.salle_jeux_paille_mauvais, 0)) AS paille_feuillage
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        JOIN provinces p ON i.fk_province_id = p.id
        LEFT JOIN st1_locaux l ON l.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY f.idannee, p.id, p.libelle

        UNION ALL

        -- Salles de repos
        SELECT
            f.idannee AS annee,
            p.id AS id_province,
            p.libelle AS province,
            'Salles de repos' AS type_locaux,
            SUM(COALESCE(l.salle_repos_dur_bon, 0) + COALESCE(l.salle_repos_dur_mauvais, 0)) AS en_dur,
            SUM(COALESCE(l.salle_repos_semidur_bon, 0) + COALESCE(l.salle_repos_semidur_mauvais, 0)) AS semi_dur,
            SUM(COALESCE(l.salle_repos_terre_bon, 0) + COALESCE(l.salle_repos_terre_mauvais, 0)) AS terre_battu,
            SUM(COALESCE(l.salle_repos_paille_bon, 0) + COALESCE(l.salle_repos_paille_mauvais, 0)) AS paille_feuillage
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        JOIN provinces p ON i.fk_province_id = p.id
        LEFT JOIN st1_locaux l ON l.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY f.idannee, p.id, p.libelle
    )

    SELECT
        annee AS "Année",
        id_province AS "ID_Province",
        province AS "Province",
        type_locaux AS "Type_de_locaux",
        en_dur AS "En_dur",
        semi_dur AS "Semi_dur",
        terre_battu AS "Terre_battu",
        paille_feuillage AS "Paille_feuillage"
    FROM locaux_par_type
    ORDER BY annee, id_province, type_locaux
    """

def get_locaux_secteur_query(where_clause):
    return f"""
    WITH locaux_par_type AS (
        -- Bureaux
        SELECT
            f.idannee AS annee,
            CASE
                WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
                ELSE i.secteur_enseignement
            END AS secteur_enseignement,
            'Bureaux' AS type_locaux,
            SUM(COALESCE(l.bureau_dur_bon, 0) + COALESCE(l.bureau_dur_mauvais, 0)) AS en_dur,
            SUM(COALESCE(l.bureau_semidur_bon, 0) + COALESCE(l.bureau_semidur_mauvais, 0)) AS semi_dur,
            SUM(COALESCE(l.bureau_terre_bon, 0) + COALESCE(l.bureau_terre_mauvais, 0)) AS terre_battu,
            SUM(COALESCE(l.bureau_paille_bon, 0) + COALESCE(l.bureau_paille_mauvais, 0)) AS paille_feuillage
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        LEFT JOIN st1_locaux l ON l.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY f.idannee, CASE WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR' ELSE i.secteur_enseignement END

        UNION ALL

        -- Magasins
        SELECT
            f.idannee AS annee,
            CASE
                WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
                ELSE i.secteur_enseignement
            END AS secteur_enseignement,
            'Magasins' AS type_locaux,
            SUM(COALESCE(l.magasin_dur_bon, 0) + COALESCE(l.magasin_dur_mauvais, 0)) AS en_dur,
            SUM(COALESCE(l.magasin_semidur_bon, 0) + COALESCE(l.magasin_semidur_mauvais, 0)) AS semi_dur,
            SUM(COALESCE(l.magasin_terre_bon, 0) + COALESCE(l.magasin_terre_mauvais, 0)) AS terre_battu,
            SUM(COALESCE(l.magasin_paille_bon, 0) + COALESCE(l.magasin_paille_mauvais, 0)) AS paille_feuillage
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        LEFT JOIN st1_locaux l ON l.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY f.idannee, CASE WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR' ELSE i.secteur_enseignement END

        UNION ALL

        -- Salles d'attente
        SELECT
            f.idannee AS annee,
            CASE
                WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
                ELSE i.secteur_enseignement
            END AS secteur_enseignement,
            'Salles d''attente' AS type_locaux,
            SUM(COALESCE(l.salle_attente_dur_bon, 0) + COALESCE(l.salle_attente_dur_mauvais, 0)) AS en_dur,
            SUM(COALESCE(l.salle_attente_semidur_bon, 0) + COALESCE(l.salle_attente_semidur_mauvais, 0)) AS semi_dur,
            SUM(COALESCE(l.salle_attente_terre_bon, 0) + COALESCE(l.salle_attente_terre_mauvais, 0)) AS terre_battu,
            SUM(COALESCE(l.salle_attente_paille_bon, 0) + COALESCE(l.salle_attente_paille_mauvais, 0)) AS paille_feuillage
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        LEFT JOIN st1_locaux l ON l.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY f.idannee, CASE WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR' ELSE i.secteur_enseignement END

        UNION ALL

        -- Salles de jeux/sport
        SELECT
            f.idannee AS annee,
            CASE
                WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
                ELSE i.secteur_enseignement
            END AS secteur_enseignement,
            'Salles de jeux/sport' AS type_locaux,
            SUM(COALESCE(l.salle_jeux_dur_bon, 0) + COALESCE(l.salle_jeux_dur_mauvais, 0)) AS en_dur,
            SUM(COALESCE(l.salle_jeux_semidur_bon, 0) + COALESCE(l.salle_jeux_semidur_mauvais, 0)) AS semi_dur,
            SUM(COALESCE(l.salle_jeux_terre_bon, 0) + COALESCE(l.salle_jeux_terre_mauvais, 0)) AS terre_battu,
            SUM(COALESCE(l.salle_jeux_paille_bon, 0) + COALESCE(l.salle_jeux_paille_mauvais, 0)) AS paille_feuillage
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        LEFT JOIN st1_locaux l ON l.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY f.idannee, CASE WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR' ELSE i.secteur_enseignement END

        UNION ALL

        -- Salles de repos
        SELECT
            f.idannee AS annee,
            CASE
                WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
                ELSE i.secteur_enseignement
            END AS secteur_enseignement,
            'Salles de repos' AS type_locaux,
            SUM(COALESCE(l.salle_repos_dur_bon, 0) + COALESCE(l.salle_repos_dur_mauvais, 0)) AS en_dur,
            SUM(COALESCE(l.salle_repos_semidur_bon, 0) + COALESCE(l.salle_repos_semidur_mauvais, 0)) AS semi_dur,
            SUM(COALESCE(l.salle_repos_terre_bon, 0) + COALESCE(l.salle_repos_terre_mauvais, 0)) AS terre_battu,
            SUM(COALESCE(l.salle_repos_paille_bon, 0) + COALESCE(l.salle_repos_paille_mauvais, 0)) AS paille_feuillage
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        LEFT JOIN st1_locaux l ON l.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY f.idannee, CASE WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR' ELSE i.secteur_enseignement END
    )

    SELECT
        annee AS "Année",
        secteur_enseignement AS "Secteur_enseignement",
        type_locaux AS "Type_de_locaux",
        en_dur AS "En_dur",
        semi_dur AS "Semi_dur",
        terre_battu AS "Terre_battu",
        paille_feuillage AS "Paille_feuillage"
    FROM locaux_par_type
    ORDER BY annee, secteur_enseignement, type_locaux
    """

def get_locaux_milieu_query(where_clause):
    return f"""
    SELECT
        f.idannee AS "Année",
        CASE
            WHEN i.milieu IS NULL OR i.milieu = '' OR UPPER(i.milieu) = 'NONE' THEN 'NR'
            ELSE i.milieu
        END AS "Milieu",
        SUM(
            COALESCE(l.bureau_dur_bon, 0) + COALESCE(l.bureau_dur_mauvais, 0) +
            COALESCE(l.magasin_dur_bon, 0) + COALESCE(l.magasin_dur_mauvais, 0) +
            COALESCE(l.salle_activites_dur_bon, 0) + COALESCE(l.salle_activites_dur_mauvais, 0) +
            COALESCE(l.salle_attente_dur_bon, 0) + COALESCE(l.salle_attente_dur_mauvais, 0) +
            COALESCE(l.salle_jeux_dur_bon, 0) + COALESCE(l.salle_jeux_dur_mauvais, 0) +
            COALESCE(l.salle_repos_dur_bon, 0) + COALESCE(l.salle_repos_dur_mauvais, 0)
        ) AS "En_dur",
        SUM(
            COALESCE(l.bureau_semidur_bon, 0) + COALESCE(l.bureau_semidur_mauvais, 0) +
            COALESCE(l.magasin_semidur_bon, 0) + COALESCE(l.magasin_semidur_mauvais, 0) +
            COALESCE(l.salle_activites_semidur_bon, 0) + COALESCE(l.salle_activites_semidur_mauvais, 0) +
            COALESCE(l.salle_attente_semidur_bon, 0) + COALESCE(l.salle_attente_semidur_mauvais, 0) +
            COALESCE(l.salle_jeux_semidur_bon, 0) + COALESCE(l.salle_jeux_semidur_mauvais, 0) +
            COALESCE(l.salle_repos_semidur_bon, 0) + COALESCE(l.salle_repos_semidur_mauvais, 0)
        ) AS "Semi_dur",
        SUM(
            COALESCE(l.bureau_terre_bon, 0) + COALESCE(l.bureau_terre_mauvais, 0) +
            COALESCE(l.magasin_terre_bon, 0) + COALESCE(l.magasin_terre_mauvais, 0) +
            COALESCE(l.salle_activites_terre_bon, 0) + COALESCE(l.salle_activites_terre_mauvais, 0) +
            COALESCE(l.salle_attente_terre_bon, 0) + COALESCE(l.salle_attente_terre_mauvais, 0) +
            COALESCE(l.salle_jeux_terre_bon, 0) + COALESCE(l.salle_jeux_terre_mauvais, 0) +
            COALESCE(l.salle_repos_terre_bon, 0) + COALESCE(l.salle_repos_terre_mauvais, 0)
        ) AS "Terre_battu",
        SUM(
            COALESCE(l.bureau_paille_bon, 0) + COALESCE(l.bureau_paille_mauvais, 0) +
            COALESCE(l.magasin_paille_bon, 0) + COALESCE(l.magasin_paille_mauvais, 0) +
            COALESCE(l.salle_activites_paille_bon, 0) + COALESCE(l.salle_activites_paille_mauvais, 0) +
            COALESCE(l.salle_attente_paille_bon, 0) + COALESCE(l.salle_attente_paille_mauvais, 0) +
            COALESCE(l.salle_jeux_paille_bon, 0) + COALESCE(l.salle_jeux_paille_mauvais, 0) +
            COALESCE(l.salle_repos_paille_bon, 0) + COALESCE(l.salle_repos_paille_mauvais, 0)
        ) AS "Paille_feuillage"
    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    LEFT JOIN st1_locaux l ON l.form_st_id = f.id
    WHERE {where_clause}
    GROUP BY f.idannee, CASE WHEN i.milieu IS NULL OR i.milieu = '' OR UPPER(i.milieu) = 'NONE' THEN 'NR' ELSE i.milieu END
    ORDER BY f.idannee, CASE WHEN i.milieu IS NULL OR i.milieu = '' OR UPPER(i.milieu) = 'NONE' THEN 'NR' ELSE i.milieu END
    """

def get_synthese_province_query(where_clause):
    return f"""
    SELECT
        p.id AS "ID_Province",
        p.libelle AS "Province",
        f.idannee AS "Année",
        CASE
            WHEN SUM(
                COALESCE(l.bureau_dur_bon, 0) + COALESCE(l.bureau_dur_mauvais, 0) +
                COALESCE(l.magasin_dur_bon, 0) + COALESCE(l.magasin_dur_mauvais, 0) +
                COALESCE(l.salle_activites_dur_bon, 0) + COALESCE(l.salle_activites_dur_mauvais, 0) +
                COALESCE(l.salle_attente_dur_bon, 0) + COALESCE(l.salle_attente_dur_mauvais, 0) +
                COALESCE(l.salle_jeux_dur_bon, 0) + COALESCE(l.salle_jeux_dur_mauvais, 0) +
                COALESCE(l.salle_repos_dur_bon, 0) + COALESCE(l.salle_repos_dur_mauvais, 0)
            ) = 0 THEN 'NR'
            ELSE CAST(SUM(
                COALESCE(l.bureau_dur_bon, 0) + COALESCE(l.bureau_dur_mauvais, 0) +
                COALESCE(l.magasin_dur_bon, 0) + COALESCE(l.magasin_dur_mauvais, 0) +
                COALESCE(l.salle_activites_dur_bon, 0) + COALESCE(l.salle_activites_dur_mauvais, 0) +
                COALESCE(l.salle_attente_dur_bon, 0) + COALESCE(l.salle_attente_dur_mauvais, 0) +
                COALESCE(l.salle_jeux_dur_bon, 0) + COALESCE(l.salle_jeux_dur_mauvais, 0) +
                COALESCE(l.salle_repos_dur_bon, 0) + COALESCE(l.salle_repos_dur_mauvais, 0)
            ) AS CHAR)
        END AS "En_dur",
        CASE
            WHEN SUM(
                COALESCE(l.bureau_semidur_bon, 0) + COALESCE(l.bureau_semidur_mauvais, 0) +
                COALESCE(l.magasin_semidur_bon, 0) + COALESCE(l.magasin_semidur_mauvais, 0) +
                COALESCE(l.salle_activites_semidur_bon, 0) + COALESCE(l.salle_activites_semidur_mauvais, 0) +
                COALESCE(l.salle_attente_semidur_bon, 0) + COALESCE(l.salle_attente_semidur_mauvais, 0) +
                COALESCE(l.salle_jeux_semidur_bon, 0) + COALESCE(l.salle_jeux_semidur_mauvais, 0) +
                COALESCE(l.salle_repos_semidur_bon, 0) + COALESCE(l.salle_repos_semidur_mauvais, 0)
            ) = 0 THEN 'NR'
            ELSE CAST(SUM(
                COALESCE(l.bureau_semidur_bon, 0) + COALESCE(l.bureau_semidur_mauvais, 0) +
                COALESCE(l.magasin_semidur_bon, 0) + COALESCE(l.magasin_semidur_mauvais, 0) +
                COALESCE(l.salle_activites_semidur_bon, 0) + COALESCE(l.salle_activites_semidur_mauvais, 0) +
                COALESCE(l.salle_attente_semidur_bon, 0) + COALESCE(l.salle_attente_semidur_mauvais, 0) +
                COALESCE(l.salle_jeux_semidur_bon, 0) + COALESCE(l.salle_jeux_semidur_mauvais, 0) +
                COALESCE(l.salle_repos_semidur_bon, 0) + COALESCE(l.salle_repos_semidur_mauvais, 0)
            ) AS CHAR)
        END AS "Semi_dur",
        CASE
            WHEN SUM(
                COALESCE(l.bureau_terre_bon, 0) + COALESCE(l.bureau_terre_mauvais, 0) +
                COALESCE(l.magasin_terre_bon, 0) + COALESCE(l.magasin_terre_mauvais, 0) +
                COALESCE(l.salle_activites_terre_bon, 0) + COALESCE(l.salle_activites_terre_mauvais, 0) +
                COALESCE(l.salle_attente_terre_bon, 0) + COALESCE(l.salle_attente_terre_mauvais, 0) +
                COALESCE(l.salle_jeux_terre_bon, 0) + COALESCE(l.salle_jeux_terre_mauvais, 0) +
                COALESCE(l.salle_repos_terre_bon, 0) + COALESCE(l.salle_repos_terre_mauvais, 0)
            ) = 0 THEN 'NR'
            ELSE CAST(SUM(
                COALESCE(l.bureau_terre_bon, 0) + COALESCE(l.bureau_terre_mauvais, 0) +
                COALESCE(l.magasin_terre_bon, 0) + COALESCE(l.magasin_terre_mauvais, 0) +
                COALESCE(l.salle_activites_terre_bon, 0) + COALESCE(l.salle_activites_terre_mauvais, 0) +
                COALESCE(l.salle_attente_terre_bon, 0) + COALESCE(l.salle_attente_terre_mauvais, 0) +
                COALESCE(l.salle_jeux_terre_bon, 0) + COALESCE(l.salle_jeux_terre_mauvais, 0) +
                COALESCE(l.salle_repos_terre_bon, 0) + COALESCE(l.salle_repos_terre_mauvais, 0)
            ) AS CHAR)
        END AS "Terre_battu",
        CASE
            WHEN SUM(
                COALESCE(l.bureau_paille_bon, 0) + COALESCE(l.bureau_paille_mauvais, 0) +
                COALESCE(l.magasin_paille_bon, 0) + COALESCE(l.magasin_paille_mauvais, 0) +
                COALESCE(l.salle_activites_paille_bon, 0) + COALESCE(l.salle_activites_paille_mauvais, 0) +
                COALESCE(l.salle_attente_paille_bon, 0) + COALESCE(l.salle_attente_paille_mauvais, 0) +
                COALESCE(l.salle_jeux_paille_bon, 0) + COALESCE(l.salle_jeux_paille_mauvais, 0) +
                COALESCE(l.salle_repos_paille_bon, 0) + COALESCE(l.salle_repos_paille_mauvais, 0)
            ) = 0 THEN 'NR'
            ELSE CAST(SUM(
                COALESCE(l.bureau_paille_bon, 0) + COALESCE(l.bureau_paille_mauvais, 0) +
                COALESCE(l.magasin_paille_bon, 0) + COALESCE(l.magasin_paille_mauvais, 0) +
                COALESCE(l.salle_activites_paille_bon, 0) + COALESCE(l.salle_activites_paille_mauvais, 0) +
                COALESCE(l.salle_attente_paille_bon, 0) + COALESCE(l.salle_attente_paille_mauvais, 0) +
                COALESCE(l.salle_jeux_paille_bon, 0) + COALESCE(l.salle_jeux_paille_mauvais, 0) +
                COALESCE(l.salle_repos_paille_bon, 0) + COALESCE(l.salle_repos_paille_mauvais, 0)
            ) AS CHAR)
        END AS "Paille_feuillage"
    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    LEFT JOIN st1_locaux l ON l.form_st_id = f.id
    WHERE {where_clause}
    GROUP BY p.id, p.libelle, f.idannee
    ORDER BY f.idannee, p.id
    """

# FONCTIONS DE COMPTAGE POUR LA PAGINATION
def get_locaux_province_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        WITH locaux_par_type AS (
            SELECT 1 FROM formulaires f
            JOIN identifications i ON f.identification_id = i.id
            JOIN provinces p ON i.fk_province_id = p.id
            LEFT JOIN st1_locaux l ON l.form_st_id = f.id
            WHERE {where_clause}
            GROUP BY f.idannee, p.id, p.libelle, 'type'
        ) SELECT 1
    ) as subquery
    """

def get_locaux_secteur_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        WITH locaux_par_type AS (
            SELECT 1 FROM formulaires f
            JOIN identifications i ON f.identification_id = i.id
            LEFT JOIN st1_locaux l ON l.form_st_id = f.id
            WHERE {where_clause}
            GROUP BY f.idannee, 
                CASE WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR' ELSE i.secteur_enseignement END,
                'type'
        ) SELECT 1
    ) as subquery
    """

def get_locaux_milieu_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1 FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        LEFT JOIN st1_locaux l ON l.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY f.idannee, CASE WHEN i.milieu IS NULL OR i.milieu = '' OR UPPER(i.milieu) = 'NONE' THEN 'NR' ELSE i.milieu END
    ) as subquery
    """

def get_synthese_province_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1 FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        JOIN provinces p ON i.fk_province_id = p.id
        LEFT JOIN st1_locaux l ON l.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY p.id, p.libelle, f.idannee
    ) as subquery
    """

# FONCTIONS D'EXPORT (similaires à celles de l'annuaire des écoles)
def export_locaux_excel(request):
    """Export Excel des données des locaux"""
    try:
        rapport_type = request.GET.get('rapport_type', 'locaux_par_province')
        filters = {
            'annee': request.GET.get('annee', ''),
            'province': request.GET.get('province', ''),
            'milieu': request.GET.get('milieu', ''),
            'secteur': request.GET.get('secteur', '')
        }
        
        where_clause, params = build_locaux_conditions(filters)
        
        # Sélectionner la requête
        if rapport_type == 'locaux_par_province':
            query = get_locaux_province_query(where_clause)
            title = "Locaux par Province"
        elif rapport_type == 'locaux_par_secteur':
            query = get_locaux_secteur_query(where_clause)
            title = "Locaux par Secteur"
        elif rapport_type == 'locaux_par_milieu':
            query = get_locaux_milieu_query(where_clause)
            title = "Locaux par Milieu"
        elif rapport_type == 'synthese_province':
            query = get_synthese_province_query(where_clause)
            title = "Synthèse par Province"
        else:
            query = get_locaux_province_query(where_clause)
            title = "Locaux par Province"
        
        # Exécuter la requête
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Créer le fichier Excel
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="locaux_{rapport_type}_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.xls"'
        
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Locaux')
        
        # Styles
        header_style = xlwt.easyxf('font: bold on; align: horiz center; pattern: pattern solid, fore_color light_green;')
        normal_style = xlwt.easyxf('align: horiz left;')
        number_style = xlwt.easyxf('align: horiz right;')
        
        # En-tête du document
        row_num = 0
        ws.write(row_num, 0, f"RAPPORT DES LOCAUX - {title}", header_style)
        row_num += 1
        ws.write(row_num, 0, f"Généré le: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
        row_num += 2
        
        # En-têtes des colonnes
        for col_num, column_title in enumerate(columns):
            ws.write(row_num, col_num, column_title.replace('_', ' ').title(), header_style)
            ws.col(col_num).width = 4000
        
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

def export_locaux_pdf(request):
    """Export PDF des données des locaux"""
    # Implémentation similaire à export_pdf de l'annuaire des écoles
    pass

def export_locaux_csv(request):
    """Export CSV des données des locaux"""
    # Implémentation similaire à export_csv de l'annuaire des écoles
    pass

# FONCTIONS UTILITAIRES POUR LES FILTRES
def get_annees_scolaires():
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT idannee FROM formulaires WHERE responded = 1 AND UPPER(type) = 'ST1' ORDER BY idannee DESC")
        return [row[0] for row in cursor.fetchall()]

def get_provinces():
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, libelle FROM provinces ORDER BY libelle")
        return [{'id': row[0], 'libelle': row[1]} for row in cursor.fetchall()]

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

















#Ratios
# views.py
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

def gestion_ratios(request):
    """Vue principale pour la gestion des ratios"""
    context = {
        'annees_scolaires': get_annees_scolaires(),
        'provinces': get_provinces(),
        'types_enseignement': get_types_enseignement(),
        'milieux': get_milieux(),
    }
    return render(request, 'annuaires/gestion_ratios.html', context)

@csrf_exempt
def get_ratios_data(request):
    """Endpoint AJAX pour récupérer les données des ratios"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ratio_type = data.get('ratio_type')
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
                
            # Filtre type d'enseignement
            type_enseignement = filters.get('type_enseignement')
            if type_enseignement:
                where_conditions.append("UPPER(f.type) = UPPER(%s)")
                params.append(type_enseignement)
                
            # Filtre province
            province = filters.get('province')
            if province:
                where_conditions.append("p.id = %s")
                params.append(province)
            
            # Filtre milieu
            milieu = filters.get('milieu')
            if milieu:
                where_conditions.append("UPPER(i.milieu) = UPPER(%s)")
                params.append(milieu)
            
            # Filtre secteur
            secteur = filters.get('secteur')
            if secteur:
                if secteur.upper() == 'PUBLIC':
                    where_conditions.append("(i.regime_gestion IS NOT NULL AND UPPER(i.regime_gestion) <> 'EPR')")
                elif secteur.upper() == 'PRIVE':
                    where_conditions.append("UPPER(i.regime_gestion) = 'EPR'")
            
            where_clause = " AND ".join(where_conditions)
            
            # Sélectionner la requête en fonction du type de ratio
            if ratio_type == 'ratio_national':
                query = get_ratio_national_query(where_clause)
                count_query = get_ratio_national_count_query(where_clause)
            elif ratio_type == 'ratio_provincial':
                query = get_ratio_provincial_query(where_clause)
                count_query = get_ratio_provincial_count_query(where_clause)
            elif ratio_type == 'ratio_milieu':
                query = get_ratio_milieu_query(where_clause)
                count_query = get_ratio_milieu_count_query(where_clause)
            elif ratio_type == 'ratio_secteur':
                query = get_ratio_secteur_query(where_clause)
                count_query = get_ratio_secteur_count_query(where_clause)
            else:
                query = get_ratio_comparatif_query(where_clause, page_size, offset)
                count_query = get_ratio_comparatif_count_query(where_clause)
            
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

# REQUÊTES SPÉCIFIQUES POUR LES RATIOS

def get_ratio_national_query(where_clause):
    return f"""
    WITH stats_nationales AS (
        SELECT
            f.idannee,
            COUNT(DISTINCT f.id) as total_ecoles,
            SUM(COALESCE(e.effectif_total, 0)) as total_eleves,
            SUM(COALESCE(s.nb_salles_total, 0)) as total_classes,
            SUM(COALESCE(ens.total_enseignants, 0)) as total_enseignants
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        LEFT JOIN (
            SELECT form_st_id,
                COALESCE(effectif_filles_3ans_1ere, 0) + COALESCE(effectif_filles_3ans_2eme, 0) + COALESCE(effectif_filles_3ans_3eme, 0) +
                COALESCE(effectif_filles_4ans_1ere, 0) + COALESCE(effectif_filles_4ans_2eme, 0) + COALESCE(effectif_filles_4ans_3eme, 0) +
                COALESCE(effectif_filles_5ans_1ere, 0) + COALESCE(effectif_filles_5ans_2eme, 0) + COALESCE(effectif_filles_5ans_3eme, 0) +
                COALESCE(effectif_filles_moins_3ans_1ere, 0) + COALESCE(effectif_filles_moins_3ans_2eme, 0) + COALESCE(effectif_filles_moins_3ans_3eme, 0) +
                COALESCE(effectif_filles_plus_5ans_1ere, 0) + COALESCE(effectif_filles_plus_5ans_2eme, 0) + COALESCE(effectif_filles_plus_5ans_3eme, 0) +
                COALESCE(effectif_garcons_3ans_1ere, 0) + COALESCE(effectif_garcons_3ans_2eme, 0) + COALESCE(effectif_garcons_3ans_3eme, 0) +
                COALESCE(effectif_garcons_4ans_1ere, 0) + COALESCE(effectif_garcons_4ans_2eme, 0) + COALESCE(effectif_garcons_4ans_3eme, 0) +
                COALESCE(effectif_garcons_5ans_1ere, 0) + COALESCE(effectif_garcons_5ans_2eme, 0) + COALESCE(effectif_garcons_5ans_3eme, 0) +
                COALESCE(effectif_garcons_moins_3ans_1ere, 0) + COALESCE(effectif_garcons_moins_3ans_2eme, 0) + COALESCE(effectif_garcons_moins_3ans_3eme, 0) +
                COALESCE(effectif_garcons_plus_5ans_1ere, 0) + COALESCE(effectif_garcons_plus_5ans_2eme, 0) + COALESCE(effectif_garcons_plus_5ans_3eme, 0) as effectif_total
            FROM st1_effectifs_par_age
        ) e ON e.form_st_id = f.id
        LEFT JOIN (
            SELECT form_st_id,
                COALESCE(nb_salles_autorisees_1ere, 0) + COALESCE(nb_salles_autorisees_2eme, 0) + COALESCE(nb_salles_autorisees_3eme, 0) as nb_salles_total
            FROM st1_infrastructure
        ) s ON s.form_st_id = f.id
        LEFT JOIN (
            SELECT form_st_id,
                COALESCE(enseignants_autres_femmes_1ere, 0) + COALESCE(enseignants_autres_femmes_2eme, 0) + COALESCE(enseignants_autres_femmes_3eme, 0) +
                COALESCE(enseignants_autres_hommes_1ere, 0) + COALESCE(enseignants_autres_hommes_2eme, 0) + COALESCE(enseignants_autres_hommes_3eme, 0) +
                COALESCE(enseignants_d4_femmes_1ere, 0) + COALESCE(enseignants_d4_femmes_2eme, 0) + COALESCE(enseignants_d4_femmes_3eme, 0) +
                COALESCE(enseignants_d4_hommes_1ere, 0) + COALESCE(enseignants_d4_hommes_2eme, 0) + COALESCE(enseignants_d4_hommes_3eme, 0) +
                COALESCE(enseignants_d4p_femmes_1ere, 0) + COALESCE(enseignants_d4p_femmes_2eme, 0) + COALESCE(enseignants_d4p_femmes_3eme, 0) +
                COALESCE(enseignants_d4p_hommes_1ere, 0) + COALESCE(enseignants_d4p_hommes_2eme, 0) + COALESCE(enseignants_d4p_hommes_3eme, 0) +
                COALESCE(enseignants_d6_femmes_1ere, 0) + COALESCE(enseignants_d6_femmes_2eme, 0) + COALESCE(enseignants_d6_femmes_3eme, 0) +
                COALESCE(enseignants_d6_hommes_1ere, 0) + COALESCE(enseignants_d6_hommes_2eme, 0) + COALESCE(enseignants_d6_hommes_3eme, 0) +
                COALESCE(enseignants_em_femmes_1ere, 0) + COALESCE(enseignants_em_femmes_2eme, 0) + COALESCE(enseignants_em_femmes_3eme, 0) +
                COALESCE(enseignants_em_hommes_1ere, 0) + COALESCE(enseignants_em_hommes_2eme, 0) + COALESCE(enseignants_em_hommes_3eme, 0) +
                COALESCE(enseignants_p6_femmes_1ere, 0) + COALESCE(enseignants_p6_femmes_2eme, 0) + COALESCE(enseignants_p6_femmes_3eme, 0) +
                COALESCE(enseignants_p6_hommes_1ere, 0) + COALESCE(enseignants_p6_hommes_2eme, 0) + COALESCE(enseignants_p6_hommes_3eme, 0) as total_enseignants
            FROM st1_enseignant
        ) ens ON ens.form_st_id = f.id
        WHERE {where_clause} AND UPPER(f.type) = 'ST1'
        GROUP BY f.idannee
    )
    SELECT
        idannee as annee,
        total_ecoles,
        total_eleves,
        total_classes,
        total_enseignants,
        CASE 
            WHEN total_classes > 0 THEN ROUND(total_eleves::decimal / total_classes, 2)
            ELSE 0 
        END as ratio_eleves_classe,
        CASE 
            WHEN total_enseignants > 0 THEN ROUND(total_eleves::decimal / total_enseignants, 2)
            ELSE 0 
        END as ratio_eleves_enseignant,
        CASE 
            WHEN total_ecoles > 0 THEN ROUND(total_eleves::decimal / total_ecoles, 2)
            ELSE 0 
        END as ratio_eleves_ecole
    FROM stats_nationales
    ORDER BY idannee DESC;
    """

def get_ratio_provincial_query(where_clause):
    return f"""
    WITH stats_provinciales AS (
        SELECT
            p.id as province_id,
            p.libelle as province,
            COUNT(DISTINCT f.id) as total_ecoles,
            SUM(COALESCE(e.effectif_total, 0)) as total_eleves,
            SUM(COALESCE(s.nb_salles_total, 0)) as total_classes,
            SUM(COALESCE(ens.total_enseignants, 0)) as total_enseignants
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        JOIN provinces p ON i.fk_province_id = p.id
        LEFT JOIN (
            SELECT form_st_id,
                COALESCE(effectif_filles_3ans_1ere, 0) + COALESCE(effectif_filles_3ans_2eme, 0) + COALESCE(effectif_filles_3ans_3eme, 0) +
                COALESCE(effectif_filles_4ans_1ere, 0) + COALESCE(effectif_filles_4ans_2eme, 0) + COALESCE(effectif_filles_4ans_3eme, 0) +
                COALESCE(effectif_filles_5ans_1ere, 0) + COALESCE(effectif_filles_5ans_2eme, 0) + COALESCE(effectif_filles_5ans_3eme, 0) +
                COALESCE(effectif_filles_moins_3ans_1ere, 0) + COALESCE(effectif_filles_moins_3ans_2eme, 0) + COALESCE(effectif_filles_moins_3ans_3eme, 0) +
                COALESCE(effectif_filles_plus_5ans_1ere, 0) + COALESCE(effectif_filles_plus_5ans_2eme, 0) + COALESCE(effectif_filles_plus_5ans_3eme, 0) +
                COALESCE(effectif_garcons_3ans_1ere, 0) + COALESCE(effectif_garcons_3ans_2eme, 0) + COALESCE(effectif_garcons_3ans_3eme, 0) +
                COALESCE(effectif_garcons_4ans_1ere, 0) + COALESCE(effectif_garcons_4ans_2eme, 0) + COALESCE(effectif_garcons_4ans_3eme, 0) +
                COALESCE(effectif_garcons_5ans_1ere, 0) + COALESCE(effectif_garcons_5ans_2eme, 0) + COALESCE(effectif_garcons_5ans_3eme, 0) +
                COALESCE(effectif_garcons_moins_3ans_1ere, 0) + COALESCE(effectif_garcons_moins_3ans_2eme, 0) + COALESCE(effectif_garcons_moins_3ans_3eme, 0) +
                COALESCE(effectif_garcons_plus_5ans_1ere, 0) + COALESCE(effectif_garcons_plus_5ans_2eme, 0) + COALESCE(effectif_garcons_plus_5ans_3eme, 0) as effectif_total
            FROM st1_effectifs_par_age
        ) e ON e.form_st_id = f.id
        LEFT JOIN (
            SELECT form_st_id,
                COALESCE(nb_salles_autorisees_1ere, 0) + COALESCE(nb_salles_autorisees_2eme, 0) + COALESCE(nb_salles_autorisees_3eme, 0) as nb_salles_total
            FROM st1_infrastructure
        ) s ON s.form_st_id = f.id
        LEFT JOIN (
            SELECT form_st_id,
                COALESCE(enseignants_autres_femmes_1ere, 0) + COALESCE(enseignants_autres_femmes_2eme, 0) + COALESCE(enseignants_autres_femmes_3eme, 0) +
                COALESCE(enseignants_autres_hommes_1ere, 0) + COALESCE(enseignants_autres_hommes_2eme, 0) + COALESCE(enseignants_autres_hommes_3eme, 0) +
                COALESCE(enseignants_d4_femmes_1ere, 0) + COALESCE(enseignants_d4_femmes_2eme, 0) + COALESCE(enseignants_d4_femmes_3eme, 0) +
                COALESCE(enseignants_d4_hommes_1ere, 0) + COALESCE(enseignants_d4_hommes_2eme, 0) + COALESCE(enseignants_d4_hommes_3eme, 0) +
                COALESCE(enseignants_d4p_femmes_1ere, 0) + COALESCE(enseignants_d4p_femmes_2eme, 0) + COALESCE(enseignants_d4p_femmes_3eme, 0) +
                COALESCE(enseignants_d4p_hommes_1ere, 0) + COALESCE(enseignants_d4p_hommes_2eme, 0) + COALESCE(enseignants_d4p_hommes_3eme, 0) +
                COALESCE(enseignants_d6_femmes_1ere, 0) + COALESCE(enseignants_d6_femmes_2eme, 0) + COALESCE(enseignants_d6_femmes_3eme, 0) +
                COALESCE(enseignants_d6_hommes_1ere, 0) + COALESCE(enseignants_d6_hommes_2eme, 0) + COALESCE(enseignants_d6_hommes_3eme, 0) +
                COALESCE(enseignants_em_femmes_1ere, 0) + COALESCE(enseignants_em_femmes_2eme, 0) + COALESCE(enseignants_em_femmes_3eme, 0) +
                COALESCE(enseignants_em_hommes_1ere, 0) + COALESCE(enseignants_em_hommes_2eme, 0) + COALESCE(enseignants_em_hommes_3eme, 0) +
                COALESCE(enseignants_p6_femmes_1ere, 0) + COALESCE(enseignants_p6_femmes_2eme, 0) + COALESCE(enseignants_p6_femmes_3eme, 0) +
                COALESCE(enseignants_p6_hommes_1ere, 0) + COALESCE(enseignants_p6_hommes_2eme, 0) + COALESCE(enseignants_p6_hommes_3eme, 0) as total_enseignants
            FROM st1_enseignant
        ) ens ON ens.form_st_id = f.id
        WHERE {where_clause} AND UPPER(f.type) = 'ST1'
        GROUP BY p.id, p.libelle
    )
    SELECT
        province_id,
        province,
        total_ecoles,
        total_eleves,
        total_classes,
        total_enseignants,
        CASE 
            WHEN total_classes > 0 THEN ROUND(total_eleves::decimal / total_classes, 2)
            ELSE 0 
        END as ratio_eleves_classe,
        CASE 
            WHEN total_enseignants > 0 THEN ROUND(total_eleves::decimal / total_enseignants, 2)
            ELSE 0 
        END as ratio_eleves_enseignant,
        CASE 
            WHEN total_ecoles > 0 THEN ROUND(total_eleves::decimal / total_ecoles, 2)
            ELSE 0 
        END as ratio_eleves_ecole
    FROM stats_provinciales
    ORDER BY province;
    """

def get_ratio_milieu_query(where_clause):
    return f"""
    WITH stats_milieu AS (
        SELECT
            CASE 
                WHEN UPPER(i.milieu) = 'URBAIN' THEN 'Urbain'
                WHEN UPPER(i.milieu) = 'RURAL' THEN 'Rural'
                ELSE 'Non renseigné'
            END as milieu,
            COUNT(DISTINCT f.id) as total_ecoles,
            SUM(COALESCE(e.effectif_total, 0)) as total_eleves,
            SUM(COALESCE(s.nb_salles_total, 0)) as total_classes,
            SUM(COALESCE(ens.total_enseignants, 0)) as total_enseignants
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        LEFT JOIN (
            SELECT form_st_id,
                COALESCE(effectif_filles_3ans_1ere, 0) + COALESCE(effectif_filles_3ans_2eme, 0) + COALESCE(effectif_filles_3ans_3eme, 0) +
                COALESCE(effectif_filles_4ans_1ere, 0) + COALESCE(effectif_filles_4ans_2eme, 0) + COALESCE(effectif_filles_4ans_3eme, 0) +
                COALESCE(effectif_filles_5ans_1ere, 0) + COALESCE(effectif_filles_5ans_2eme, 0) + COALESCE(effectif_filles_5ans_3eme, 0) +
                COALESCE(effectif_filles_moins_3ans_1ere, 0) + COALESCE(effectif_filles_moins_3ans_2eme, 0) + COALESCE(effectif_filles_moins_3ans_3eme, 0) +
                COALESCE(effectif_filles_plus_5ans_1ere, 0) + COALESCE(effectif_filles_plus_5ans_2eme, 0) + COALESCE(effectif_filles_plus_5ans_3eme, 0) +
                COALESCE(effectif_garcons_3ans_1ere, 0) + COALESCE(effectif_garcons_3ans_2eme, 0) + COALESCE(effectif_garcons_3ans_3eme, 0) +
                COALESCE(effectif_garcons_4ans_1ere, 0) + COALESCE(effectif_garcons_4ans_2eme, 0) + COALESCE(effectif_garcons_4ans_3eme, 0) +
                COALESCE(effectif_garcons_5ans_1ere, 0) + COALESCE(effectif_garcons_5ans_2eme, 0) + COALESCE(effectif_garcons_5ans_3eme, 0) +
                COALESCE(effectif_garcons_moins_3ans_1ere, 0) + COALESCE(effectif_garcons_moins_3ans_2eme, 0) + COALESCE(effectif_garcons_moins_3ans_3eme, 0) +
                COALESCE(effectif_garcons_plus_5ans_1ere, 0) + COALESCE(effectif_garcons_plus_5ans_2eme, 0) + COALESCE(effectif_garcons_plus_5ans_3eme, 0) as effectif_total
            FROM st1_effectifs_par_age
        ) e ON e.form_st_id = f.id
        LEFT JOIN (
            SELECT form_st_id,
                COALESCE(nb_salles_autorisees_1ere, 0) + COALESCE(nb_salles_autorisees_2eme, 0) + COALESCE(nb_salles_autorisees_3eme, 0) as nb_salles_total
            FROM st1_infrastructure
        ) s ON s.form_st_id = f.id
        LEFT JOIN (
            SELECT form_st_id,
                COALESCE(enseignants_autres_femmes_1ere, 0) + COALESCE(enseignants_autres_femmes_2eme, 0) + COALESCE(enseignants_autres_femmes_3eme, 0) +
                COALESCE(enseignants_autres_hommes_1ere, 0) + COALESCE(enseignants_autres_hommes_2eme, 0) + COALESCE(enseignants_autres_hommes_3eme, 0) +
                COALESCE(enseignants_d4_femmes_1ere, 0) + COALESCE(enseignants_d4_femmes_2eme, 0) + COALESCE(enseignants_d4_femmes_3eme, 0) +
                COALESCE(enseignants_d4_hommes_1ere, 0) + COALESCE(enseignants_d4_hommes_2eme, 0) + COALESCE(enseignants_d4_hommes_3eme, 0) +
                COALESCE(enseignants_d4p_femmes_1ere, 0) + COALESCE(enseignants_d4p_femmes_2eme, 0) + COALESCE(enseignants_d4p_femmes_3eme, 0) +
                COALESCE(enseignants_d4p_hommes_1ere, 0) + COALESCE(enseignants_d4p_hommes_2eme, 0) + COALESCE(enseignants_d4p_hommes_3eme, 0) +
                COALESCE(enseignants_d6_femmes_1ere, 0) + COALESCE(enseignants_d6_femmes_2eme, 0) + COALESCE(enseignants_d6_femmes_3eme, 0) +
                COALESCE(enseignants_d6_hommes_1ere, 0) + COALESCE(enseignants_d6_hommes_2eme, 0) + COALESCE(enseignants_d6_hommes_3eme, 0) +
                COALESCE(enseignants_em_femmes_1ere, 0) + COALESCE(enseignants_em_femmes_2eme, 0) + COALESCE(enseignants_em_femmes_3eme, 0) +
                COALESCE(enseignants_em_hommes_1ere, 0) + COALESCE(enseignants_em_hommes_2eme, 0) + COALESCE(enseignants_em_hommes_3eme, 0) +
                COALESCE(enseignants_p6_femmes_1ere, 0) + COALESCE(enseignants_p6_femmes_2eme, 0) + COALESCE(enseignants_p6_femmes_3eme, 0) +
                COALESCE(enseignants_p6_hommes_1ere, 0) + COALESCE(enseignants_p6_hommes_2eme, 0) + COALESCE(enseignants_p6_hommes_3eme, 0) as total_enseignants
            FROM st1_enseignant
        ) ens ON ens.form_st_id = f.id
        WHERE {where_clause} AND UPPER(f.type) = 'ST1'
        GROUP BY 
            CASE 
                WHEN UPPER(i.milieu) = 'URBAIN' THEN 'Urbain'
                WHEN UPPER(i.milieu) = 'RURAL' THEN 'Rural'
                ELSE 'Non renseigné'
            END
    )
    SELECT
        milieu,
        total_ecoles,
        total_eleves,
        total_classes,
        total_enseignants,
        CASE 
            WHEN total_classes > 0 THEN ROUND(total_eleves::decimal / total_classes, 2)
            ELSE 0 
        END as ratio_eleves_classe,
        CASE 
            WHEN total_enseignants > 0 THEN ROUND(total_eleves::decimal / total_enseignants, 2)
            ELSE 0 
        END as ratio_eleves_enseignant,
        CASE 
            WHEN total_ecoles > 0 THEN ROUND(total_eleves::decimal / total_ecoles, 2)
            ELSE 0 
        END as ratio_eleves_ecole
    FROM stats_milieu
    ORDER BY milieu;
    """

def get_ratio_secteur_query(where_clause):
    return f"""
    WITH stats_secteur AS (
        SELECT
            CASE 
                WHEN UPPER(i.regime_gestion) = 'EPR' THEN 'Privé'
                ELSE 'Public'
            END as secteur,
            COUNT(DISTINCT f.id) as total_ecoles,
            SUM(COALESCE(e.effectif_total, 0)) as total_eleves,
            SUM(COALESCE(s.nb_salles_total, 0)) as total_classes,
            SUM(COALESCE(ens.total_enseignants, 0)) as total_enseignants
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        LEFT JOIN (
            SELECT form_st_id,
                COALESCE(effectif_filles_3ans_1ere, 0) + COALESCE(effectif_filles_3ans_2eme, 0) + COALESCE(effectif_filles_3ans_3eme, 0) +
                COALESCE(effectif_filles_4ans_1ere, 0) + COALESCE(effectif_filles_4ans_2eme, 0) + COALESCE(effectif_filles_4ans_3eme, 0) +
                COALESCE(effectif_filles_5ans_1ere, 0) + COALESCE(effectif_filles_5ans_2eme, 0) + COALESCE(effectif_filles_5ans_3eme, 0) +
                COALESCE(effectif_filles_moins_3ans_1ere, 0) + COALESCE(effectif_filles_moins_3ans_2eme, 0) + COALESCE(effectif_filles_moins_3ans_3eme, 0) +
                COALESCE(effectif_filles_plus_5ans_1ere, 0) + COALESCE(effectif_filles_plus_5ans_2eme, 0) + COALESCE(effectif_filles_plus_5ans_3eme, 0) +
                COALESCE(effectif_garcons_3ans_1ere, 0) + COALESCE(effectif_garcons_3ans_2eme, 0) + COALESCE(effectif_garcons_3ans_3eme, 0) +
                COALESCE(effectif_garcons_4ans_1ere, 0) + COALESCE(effectif_garcons_4ans_2eme, 0) + COALESCE(effectif_garcons_4ans_3eme, 0) +
                COALESCE(effectif_garcons_5ans_1ere, 0) + COALESCE(effectif_garcons_5ans_2eme, 0) + COALESCE(effectif_garcons_5ans_3eme, 0) +
                COALESCE(effectif_garcons_moins_3ans_1ere, 0) + COALESCE(effectif_garcons_moins_3ans_2eme, 0) + COALESCE(effectif_garcons_moins_3ans_3eme, 0) +
                COALESCE(effectif_garcons_plus_5ans_1ere, 0) + COALESCE(effectif_garcons_plus_5ans_2eme, 0) + COALESCE(effectif_garcons_plus_5ans_3eme, 0) as effectif_total
            FROM st1_effectifs_par_age
        ) e ON e.form_st_id = f.id
        LEFT JOIN (
            SELECT form_st_id,
                COALESCE(nb_salles_autorisees_1ere, 0) + COALESCE(nb_salles_autorisees_2eme, 0) + COALESCE(nb_salles_autorisees_3eme, 0) as nb_salles_total
            FROM st1_infrastructure
        ) s ON s.form_st_id = f.id
        LEFT JOIN (
            SELECT form_st_id,
                COALESCE(enseignants_autres_femmes_1ere, 0) + COALESCE(enseignants_autres_femmes_2eme, 0) + COALESCE(enseignants_autres_femmes_3eme, 0) +
                COALESCE(enseignants_autres_hommes_1ere, 0) + COALESCE(enseignants_autres_hommes_2eme, 0) + COALESCE(enseignants_autres_hommes_3eme, 0) +
                COALESCE(enseignants_d4_femmes_1ere, 0) + COALESCE(enseignants_d4_femmes_2eme, 0) + COALESCE(enseignants_d4_femmes_3eme, 0) +
                COALESCE(enseignants_d4_hommes_1ere, 0) + COALESCE(enseignants_d4_hommes_2eme, 0) + COALESCE(enseignants_d4_hommes_3eme, 0) +
                COALESCE(enseignants_d4p_femmes_1ere, 0) + COALESCE(enseignants_d4p_femmes_2eme, 0) + COALESCE(enseignants_d4p_femmes_3eme, 0) +
                COALESCE(enseignants_d4p_hommes_1ere, 0) + COALESCE(enseignants_d4p_hommes_2eme, 0) + COALESCE(enseignants_d4p_hommes_3eme, 0) +
                COALESCE(enseignants_d6_femmes_1ere, 0) + COALESCE(enseignants_d6_femmes_2eme, 0) + COALESCE(enseignants_d6_femmes_3eme, 0) +
                COALESCE(enseignants_d6_hommes_1ere, 0) + COALESCE(enseignants_d6_hommes_2eme, 0) + COALESCE(enseignants_d6_hommes_3eme, 0) +
                COALESCE(enseignants_em_femmes_1ere, 0) + COALESCE(enseignants_em_femmes_2eme, 0) + COALESCE(enseignants_em_femmes_3eme, 0) +
                COALESCE(enseignants_em_hommes_1ere, 0) + COALESCE(enseignants_em_hommes_2eme, 0) + COALESCE(enseignants_em_hommes_3eme, 0) +
                COALESCE(enseignants_p6_femmes_1ere, 0) + COALESCE(enseignants_p6_femmes_2eme, 0) + COALESCE(enseignants_p6_femmes_3eme, 0) +
                COALESCE(enseignants_p6_hommes_1ere, 0) + COALESCE(enseignants_p6_hommes_2eme, 0) + COALESCE(enseignants_p6_hommes_3eme, 0) as total_enseignants
            FROM st1_enseignant
        ) ens ON ens.form_st_id = f.id
        WHERE {where_clause} AND UPPER(f.type) = 'ST1'
        GROUP BY 
            CASE 
                WHEN UPPER(i.regime_gestion) = 'EPR' THEN 'Privé'
                ELSE 'Public'
            END
    )
    SELECT
        secteur,
        total_ecoles,
        total_eleves,
        total_classes,
        total_enseignants,
        CASE 
            WHEN total_classes > 0 THEN ROUND(total_eleves::decimal / total_classes, 2)
            ELSE 0 
        END as ratio_eleves_classe,
        CASE 
            WHEN total_enseignants > 0 THEN ROUND(total_eleves::decimal / total_enseignants, 2)
            ELSE 0 
        END as ratio_eleves_enseignant,
        CASE 
            WHEN total_ecoles > 0 THEN ROUND(total_eleves::decimal / total_ecoles, 2)
            ELSE 0 
        END as ratio_eleves_ecole
    FROM stats_secteur
    ORDER BY secteur;
    """

def get_ratio_comparatif_query(where_clause, page_size=10, offset=0):
    return f"""
    SELECT 
        f.id,
        f.idannee as annee_scolaire,
        f.type as type_enseignement,
        p.libelle as province,
        i.milieu,
        CASE 
            WHEN UPPER(i.regime_gestion) = 'EPR' THEN 'Privé'
            ELSE 'Public'
        END as secteur,
        CONCAT('Établissement ', f.id) as nom_etablissement,
        'Actif' as statut
    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE {where_clause}
    ORDER BY p.libelle, f.idannee
    LIMIT {page_size} OFFSET {offset};
    """

# FONCTIONS DE COMPTAGE
def get_ratio_national_count_query(where_clause):
    return f"""
    SELECT COUNT(DISTINCT f.idannee)
    FROM formulaires f
    WHERE {where_clause} AND UPPER(f.type) = 'ST1'
    """

def get_ratio_provincial_count_query(where_clause):
    return f"""
    SELECT COUNT(DISTINCT p.id)
    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE {where_clause} AND UPPER(f.type) = 'ST1'
    """

def get_ratio_milieu_count_query(where_clause):
    return f"""
    SELECT COUNT(DISTINCT 
        CASE 
            WHEN UPPER(i.milieu) = 'URBAIN' THEN 'Urbain'
            WHEN UPPER(i.milieu) = 'RURAL' THEN 'Rural'
            ELSE 'Non renseigné'
        END
    )
    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    WHERE {where_clause} AND UPPER(f.type) = 'ST1'
    """

def get_ratio_secteur_count_query(where_clause):
    return f"""
    SELECT COUNT(DISTINCT 
        CASE 
            WHEN UPPER(i.regime_gestion) = 'EPR' THEN 'Privé'
            ELSE 'Public'
        END
    )
    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    WHERE {where_clause} AND UPPER(f.type) = 'ST1'
    """

def get_ratio_comparatif_count_query(where_clause):
    return f"""
    SELECT COUNT(*)
    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    WHERE {where_clause}
    """

# FONCTIONS UTILITAIRES (identiques à celles de l'annuaire)
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
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT UPPER(milieu) 
            FROM identifications 
            WHERE milieu IS NOT NULL AND milieu != '' 
            ORDER BY milieu
        """)
        return [row[0] for row in cursor.fetchall()]





























# FONCTIONS POUR LES COMMODITÉS
# views.py - Version complète corrigée pour les commodités
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

def annuaire_commodites(request):
    """Vue principale pour les commodités"""
    context = {
        'annees_scolaires': get_annees_scolaires(),
        'provinces': get_provinces(),
        'types_enseignement': get_types_enseignement(),
        'secteurs_enseignement': get_secteurs_enseignement(),
        'regimes_gestion': get_regimes_gestion(),
    }
    return render(request, 'annuaires/annuaire_commodites.html', context)

@csrf_exempt
def get_commodites_data(request):
    """Endpoint AJAX pour récupérer les données des commodités avec pagination"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rapport_type = data.get('rapport_type', 'par_province')
            filters = data.get('filters', {})
            page = int(data.get('page', 1))
            page_size = int(data.get('page_size', 10))
            
            # Calculer l'offset pour la pagination
            offset = (page - 1) * page_size
            
            # Appliquer les filtres
            where_conditions = ["f.responded = 1"]
            params = {}
            param_count = 0
            
            # Filtre année scolaire
            annee = filters.get('annee')
            if annee:
                param_count += 1
                param_name = f"annee_{param_count}"
                where_conditions.append(f"f.idannee = %({param_name})s")
                params[param_name] = annee
                
            # Filtre type d'enseignement
            type_enseignement = filters.get('type_enseignement')
            if type_enseignement:
                param_count += 1
                param_name = f"type_{param_count}"
                where_conditions.append(f"UPPER(f.type) = UPPER(%({param_name})s)")
                params[param_name] = type_enseignement
                
            # Filtre province
            province = filters.get('province')
            if province:
                param_count += 1
                param_name = f"province_{param_count}"
                where_conditions.append(f"p.id = %({param_name})s")
                params[param_name] = province
            
            # Filtre secteur d'enseignement
            secteur = filters.get('secteur_enseignement')
            if secteur:
                if secteur.upper() == 'NR':
                    where_conditions.append("(i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE')")
                elif secteur.upper() == 'AUTRES':
                    where_conditions.append("UPPER(i.secteur_enseignement) IN ('AC', 'AU/AC')")
                else:
                    param_count += 1
                    param_name = f"secteur_{param_count}"
                    where_conditions.append(f"i.secteur_enseignement = %({param_name})s")
                    params[param_name] = secteur
            
            # Filtre régime de gestion
            regime = filters.get('regime_gestion')
            if regime:
                if regime.upper() == 'NR':
                    where_conditions.append("(i.regime_gestion IS NULL OR i.regime_gestion = '' OR UPPER(i.regime_gestion) = 'NONE')")
                elif regime.upper() == 'AUTRES':
                    where_conditions.append("(i.regime_gestion IS NOT NULL AND i.regime_gestion != '' AND UPPER(i.regime_gestion) NOT IN ('ECC', 'ECF', 'ECI', 'ECK', 'ECP', 'ECS', 'ENC', 'EPR', 'NR'))")
                else:
                    param_count += 1
                    param_name = f"regime_{param_count}"
                    where_conditions.append(f"i.regime_gestion = %({param_name})s")
                    params[param_name] = regime
            
            where_clause = " AND ".join(where_conditions)
            
            # Sélectionner la requête en fonction du type de rapport
            if rapport_type == 'par_secteur_regime':
                query, count_query = get_commodites_secteur_regime_queries(where_clause, page_size, offset)
            else:  # par_province par défaut
                query, count_query = get_commodites_province_queries(where_clause, page_size, offset)
            
            # DEBUG: Afficher les requêtes et paramètres
            print("=== DEBUG COMMODITES ===")
            print("Query:", query)
            print("Count Query:", count_query)
            print("Params:", params)
            print("=============")
            
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
                },
                'columns': columns
            })
            
        except Exception as e:
            import traceback
            print("Erreur détaillée:", traceback.format_exc())
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})

# Fonctions pour générer les requêtes
def get_commodites_province_queries(where_clause, page_size=None, offset=0):
    """Retourne le tuple (query, count_query) pour les commodités par province"""
    base_query = f"""
    SELECT
        f.idannee AS "Annee",
        p.id AS "ID_Province",
        p.libelle AS "Province",
        f.type AS "Type",
        CASE
            WHEN COUNT(f.id) = 0 THEN 0.00
            ELSE ROUND((COUNT(CASE WHEN g.point_eau = 'OUI' THEN 1 END) * 100.0 / COUNT(f.id)), 2)
        END AS "Point_eau_pourcent",
        CASE
            WHEN COUNT(f.id) = 0 THEN 0.00
            ELSE ROUND((COUNT(CASE WHEN g.latrines = 'OUI' THEN 1 END) * 100.0 / COUNT(f.id)), 2)
        END AS "Latrines_pourcent",
        CASE
            WHEN COUNT(f.id) = 0 THEN 0.00
            ELSE ROUND((COUNT(CASE WHEN g.sources_energie = 'OUI' THEN 1 END) * 100.0 / COUNT(f.id)), 2)
        END AS "Electricite_pourcent",
        CASE
            WHEN COUNT(f.id) = 0 THEN 0.00
            ELSE ROUND((COUNT(CASE WHEN g.cloture = 'OUI' THEN 1 END) * 100.0 / COUNT(f.id)), 2)
        END AS "Cloture_pourcent",
        CASE
            WHEN COUNT(f.id) = 0 THEN 0.00
            ELSE ROUND((COUNT(CASE WHEN g.etablissement_pris_en_charge_programme_refugies = 'OUI' THEN 1 END) * 100.0 / COUNT(f.id)), 2)
        END AS "Programme_refugie_pourcent",
        CASE
            WHEN COUNT(f.id) = 0 THEN 0.00
            ELSE ROUND((COUNT(CASE WHEN g.programmes_officiels = 'OUI' THEN 1 END) * 100.0 / COUNT(f.id)), 2)
        END AS "Programme_officiel_pourcent",
        CASE
            WHEN COUNT(f.id) = 0 THEN 0.00
            ELSE ROUND((COUNT(CASE WHEN g.copa = 'OUI' OR g.coges = 'OUI' THEN 1 END) * 100.0 / COUNT(f.id)), 2)
        END AS "COPA_COGES_pourcent",
        CASE
            WHEN COUNT(f.id) = 0 THEN 0.00
            ELSE ROUND((COUNT(CASE WHEN g.terrain_jeux = 'OUI' THEN 1 END) * 100.0 / COUNT(f.id)), 2)
        END AS "Aire_jeux_pourcent"
    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    JOIN provinces p ON i.fk_province_id = p.id
    LEFT JOIN informations_generale g ON g.form_st_id = f.id
    WHERE {where_clause}
    GROUP BY f.idannee, p.id, p.libelle, f.type
    ORDER BY f.idannee, p.id, f.type
    """
    
    count_query = f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        JOIN provinces p ON i.fk_province_id = p.id
        LEFT JOIN informations_generale g ON g.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY f.idannee, p.id, p.libelle, f.type
    ) as subquery
    """
    
    if page_size is not None:
        base_query += f" LIMIT {page_size} OFFSET {offset}"
    
    return base_query, count_query

def get_commodites_secteur_regime_queries(where_clause, page_size=None, offset=0):
    """Retourne le tuple (query, count_query) pour les commodités par secteur et régime"""
    base_query = f"""
    SELECT
        f.idannee AS "Annee",
        f.type AS "Type",
        CASE
            WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
            WHEN UPPER(i.secteur_enseignement) IN ('AC', 'AU/AC') THEN 'AUTRES'
            ELSE i.secteur_enseignement
        END AS "Secteur_enseignement",
        CASE
            WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' OR UPPER(i.regime_gestion) = 'NONE' THEN 'NR'
            WHEN UPPER(i.regime_gestion) IN ('ECC', 'ECF', 'ECI', 'ECK', 'ECP', 'ECS', 'ENC', 'EPR') THEN i.regime_gestion
            ELSE 'AUTRES'
        END AS "Regime_gestion",
        CASE
            WHEN COUNT(f.id) = 0 THEN 0.00
            ELSE ROUND((COUNT(CASE WHEN g.point_eau = 'OUI' THEN 1 END) * 100.0 / COUNT(f.id)), 2)
        END AS "Point_eau_pourcent",
        CASE
            WHEN COUNT(f.id) = 0 THEN 0.00
            ELSE ROUND((COUNT(CASE WHEN g.latrines = 'OUI' THEN 1 END) * 100.0 / COUNT(f.id)), 2)
        END AS "Latrines_pourcent",
        CASE
            WHEN COUNT(f.id) = 0 THEN 0.00
            ELSE ROUND((COUNT(CASE WHEN g.sources_energie = 'OUI' THEN 1 END) * 100.0 / COUNT(f.id)), 2)
        END AS "Electricite_pourcent",
        CASE
            WHEN COUNT(f.id) = 0 THEN 0.00
            ELSE ROUND((COUNT(CASE WHEN g.cloture = 'OUI' THEN 1 END) * 100.0 / COUNT(f.id)), 2)
        END AS "Cloture_pourcent",
        CASE
            WHEN COUNT(f.id) = 0 THEN 0.00
            ELSE ROUND((COUNT(CASE WHEN g.etablissement_pris_en_charge_programme_refugies = 'OUI' THEN 1 END) * 100.0 / COUNT(f.id)), 2)
        END AS "Programme_refugie_pourcent",
        CASE
            WHEN COUNT(f.id) = 0 THEN 0.00
            ELSE ROUND((COUNT(CASE WHEN g.programmes_officiels = 'OUI' THEN 1 END) * 100.0 / COUNT(f.id)), 2)
        END AS "Programme_officiel_pourcent",
        CASE
            WHEN COUNT(f.id) = 0 THEN 0.00
            ELSE ROUND((COUNT(CASE WHEN g.copa = 'OUI' OR g.coges = 'OUI' THEN 1 END) * 100.0 / COUNT(f.id)), 2)
        END AS "COPA_COGES_pourcent",
        CASE
            WHEN COUNT(f.id) = 0 THEN 0.00
            ELSE ROUND((COUNT(CASE WHEN g.terrain_jeux = 'OUI' THEN 1 END) * 100.0 / COUNT(f.id)), 2)
        END AS "Aire_jeux_pourcent"
    FROM formulaires f
    JOIN identifications i ON f.identification_id = i.id
    LEFT JOIN informations_generale g ON g.form_st_id = f.id
    WHERE {where_clause}
    GROUP BY f.idannee, f.type,
        CASE
            WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
            WHEN UPPER(i.secteur_enseignement) IN ('AC', 'AU/AC') THEN 'AUTRES'
            ELSE i.secteur_enseignement
        END,
        CASE
            WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' OR UPPER(i.regime_gestion) = 'NONE' THEN 'NR'
            WHEN UPPER(i.regime_gestion) IN ('ECC', 'ECF', 'ECI', 'ECK', 'ECP', 'ECS', 'ENC', 'EPR') THEN i.regime_gestion
            ELSE 'AUTRES'
        END
    ORDER BY f.idannee, f.type,
        CASE
            WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
            WHEN UPPER(i.secteur_enseignement) IN ('AC', 'AU/AC') THEN 'AUTRES'
            ELSE i.secteur_enseignement
        END,
        CASE
            WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' OR UPPER(i.regime_gestion) = 'NONE' THEN 'NR'
            WHEN UPPER(i.regime_gestion) IN ('ECC', 'ECF', 'ECI', 'ECK', 'ECP', 'ECS', 'ENC', 'EPR') THEN i.regime_gestion
            ELSE 'AUTRES'
        END
    """
    
    count_query = f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        LEFT JOIN informations_generale g ON g.form_st_id = f.id
        WHERE {where_clause}
        GROUP BY f.idannee, f.type,
            CASE
                WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
                WHEN UPPER(i.secteur_enseignement) IN ('AC', 'AU/AC') THEN 'AUTRES'
                ELSE i.secteur_enseignement
            END,
            CASE
                WHEN i.regime_gestion IS NULL OR i.regime_gestion = '' OR UPPER(i.regime_gestion) = 'NONE' THEN 'NR'
                WHEN UPPER(i.regime_gestion) IN ('ECC', 'ECF', 'ECI', 'ECK', 'ECP', 'ECS', 'ENC', 'EPR') THEN i.regime_gestion
                ELSE 'AUTRES'
            END
    ) as subquery
    """
    
    if page_size is not None:
        base_query += f" LIMIT {page_size} OFFSET {offset}"
    
    return base_query, count_query

# Fonctions pour les exports
def get_commodites_province_query(where_clause):
    query, _ = get_commodites_province_queries(where_clause)
    return query

def get_commodites_secteur_regime_query(where_clause):
    query, _ = get_commodites_secteur_regime_queries(where_clause)
    return query

def export_commodites_excel(request):
    """Export Excel des données de commodités"""
    try:
        rapport_type = request.GET.get('rapport_type', 'par_province')
        filters = {
            'annee': request.GET.get('annee', ''),
            'type_enseignement': request.GET.get('type_enseignement', ''),
            'province': request.GET.get('province', ''),
            'secteur_enseignement': request.GET.get('secteur_enseignement', ''),
            'regime_gestion': request.GET.get('regime_gestion', '')
        }
        
        # Récupérer les données
        where_conditions = ["f.responded = 1"]
        params = {}
        param_count = 0
        
        # Appliquer les filtres
        annee = filters.get('annee')
        if annee:
            param_count += 1
            param_name = f"annee_{param_count}"
            where_conditions.append(f"f.idannee = %({param_name})s")
            params[param_name] = annee
            
        type_enseignement = filters.get('type_enseignement')
        if type_enseignement:
            param_count += 1
            param_name = f"type_{param_count}"
            where_conditions.append(f"UPPER(f.type) = UPPER(%({param_name})s)")
            params[param_name] = type_enseignement
            
        province = filters.get('province')
        if province:
            param_count += 1
            param_name = f"province_{param_count}"
            where_conditions.append(f"p.id = %({param_name})s")
            params[param_name] = province
        
        secteur = filters.get('secteur_enseignement')
        if secteur:
            if secteur.upper() == 'NR':
                where_conditions.append("(i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE')")
            elif secteur.upper() == 'AUTRES':
                where_conditions.append("UPPER(i.secteur_enseignement) IN ('AC', 'AU/AC')")
            else:
                param_count += 1
                param_name = f"secteur_{param_count}"
                where_conditions.append(f"i.secteur_enseignement = %({param_name})s")
                params[param_name] = secteur
        
        regime = filters.get('regime_gestion')
        if regime:
            if regime.upper() == 'NR':
                where_conditions.append("(i.regime_gestion IS NULL OR i.regime_gestion = '' OR UPPER(i.regime_gestion) = 'NONE')")
            elif regime.upper() == 'AUTRES':
                where_conditions.append("(i.regime_gestion IS NOT NULL AND i.regime_gestion != '' AND UPPER(i.regime_gestion) NOT IN ('ECC', 'ECF', 'ECI', 'ECK', 'ECP', 'ECS', 'ENC', 'EPR', 'NR'))")
            else:
                param_count += 1
                param_name = f"regime_{param_count}"
                where_conditions.append(f"i.regime_gestion = %({param_name})s")
                params[param_name] = regime
        
        where_clause = " AND ".join(where_conditions)
        
        # Sélectionner la requête
        if rapport_type == 'par_secteur_regime':
            query = get_commodites_secteur_regime_query(where_clause)
            title = "Commodités par Secteur et Régime"
        else:
            query = get_commodites_province_query(where_clause)
            title = "Commodités par Province"
        
        # Exécuter la requête
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Créer le fichier Excel
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="commodites_{rapport_type}_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.xls"'
        
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Commodités')
        
        # Styles
        header_style = xlwt.easyxf('font: bold on; align: horiz center; pattern: pattern solid, fore_color light_blue;')
        normal_style = xlwt.easyxf('align: horiz left;')
        number_style = xlwt.easyxf('align: horiz right;')
        percent_style = xlwt.easyxf('align: horiz right;', num_format_str='0.00%')
        
        # En-tête du document
        row_num = 0
        ws.write(row_num, 0, f"RAPPORT DES COMMODITÉS - {title}", header_style)
        row_num += 1
        ws.write(row_num, 0, f"Généré le: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
        row_num += 2
        
        # En-têtes des colonnes avec noms plus lisibles
        display_columns = []
        for col in columns:
            if col.endswith('_pourcent'):
                display_columns.append(col.replace('_pourcent', ' (%)').replace('_', ' ').title())
            else:
                display_columns.append(col.replace('_', ' ').title())
        
        for col_num, column_title in enumerate(display_columns):
            ws.write(row_num, col_num, column_title, header_style)
            ws.col(col_num).width = 4000
        
        row_num += 1
        
        # Données
        for row in results:
            for col_num, column_title in enumerate(columns):
                value = row.get(column_title, '')
                if isinstance(value, (int, float)) and '_pourcent' in column_title:
                    ws.write(row_num, col_num, value/100.0, percent_style)
                elif isinstance(value, (int, float)):
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

def export_commodites_pdf(request):
    """Export PDF des données de commodités"""
    try:
        rapport_type = request.GET.get('rapport_type', 'par_province')
        filters = {
            'annee': request.GET.get('annee', ''),
            'type_enseignement': request.GET.get('type_enseignement', ''),
            'province': request.GET.get('province', ''),
            'secteur_enseignement': request.GET.get('secteur_enseignement', ''),
            'regime_gestion': request.GET.get('regime_gestion', '')
        }
        
        # Récupérer les données
        where_conditions = ["f.responded = 1"]
        params = {}
        param_count = 0
        
        # Appliquer les filtres
        annee = filters.get('annee')
        if annee:
            param_count += 1
            param_name = f"annee_{param_count}"
            where_conditions.append(f"f.idannee = %({param_name})s")
            params[param_name] = annee
            
        type_enseignement = filters.get('type_enseignement')
        if type_enseignement:
            param_count += 1
            param_name = f"type_{param_count}"
            where_conditions.append(f"UPPER(f.type) = UPPER(%({param_name})s)")
            params[param_name] = type_enseignement
            
        province = filters.get('province')
        if province:
            param_count += 1
            param_name = f"province_{param_count}"
            where_conditions.append(f"p.id = %({param_name})s")
            params[param_name] = province
        
        secteur = filters.get('secteur_enseignement')
        if secteur:
            if secteur.upper() == 'NR':
                where_conditions.append("(i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE')")
            elif secteur.upper() == 'AUTRES':
                where_conditions.append("UPPER(i.secteur_enseignement) IN ('AC', 'AU/AC')")
            else:
                param_count += 1
                param_name = f"secteur_{param_count}"
                where_conditions.append(f"i.secteur_enseignement = %({param_name})s")
                params[param_name] = secteur
        
        regime = filters.get('regime_gestion')
        if regime:
            if regime.upper() == 'NR':
                where_conditions.append("(i.regime_gestion IS NULL OR i.regime_gestion = '' OR UPPER(i.regime_gestion) = 'NONE')")
            elif regime.upper() == 'AUTRES':
                where_conditions.append("(i.regime_gestion IS NOT NULL AND i.regime_gestion != '' AND UPPER(i.regime_gestion) NOT IN ('ECC', 'ECF', 'ECI', 'ECK', 'ECP', 'ECS', 'ENC', 'EPR', 'NR'))")
            else:
                param_count += 1
                param_name = f"regime_{param_count}"
                where_conditions.append(f"i.regime_gestion = %({param_name})s")
                params[param_name] = regime
        
        where_clause = " AND ".join(where_conditions)
        
        # Sélectionner la requête
        if rapport_type == 'par_secteur_regime':
            query = get_commodites_secteur_regime_query(where_clause)
            title = "Commodités par Secteur et Régime"
        else:
            query = get_commodites_province_query(where_clause)
            title = "Commodités par Province"
        
        # Exécuter la requête
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Créer le PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="commodites_{rapport_type}_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.pdf"'
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        elements = []
        
        styles = getSampleStyleSheet()
        
        # Titre
        title_text = f"RAPPORT DES COMMODITÉS - {title}"
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
        if filters['secteur_enseignement']:
            filters_list.append(f"Secteur: {filters['secteur_enseignement']}")
        if filters['regime_gestion']:
            filters_list.append(f"Régime: {filters['regime_gestion']}")
        
        if filters_list:
            filters_text += " | ".join(filters_list)
            elements.append(Paragraph(filters_text, styles['Normal']))
        
        elements.append(Paragraph(" ", styles['Normal']))  # Espace
        
        # Préparer les données pour le tableau
        if results:
            # En-têtes avec noms plus lisibles
            display_columns = []
            for col in columns:
                if col.endswith('_pourcent'):
                    display_columns.append(col.replace('_pourcent', ' (%)').replace('_', ' ').title())
                else:
                    display_columns.append(col.replace('_', ' ').title())
            
            table_data = [display_columns]
            
            # Données
            for row in results:
                table_row = []
                for col in columns:
                    value = row.get(col, '')
                    if isinstance(value, float) and '_pourcent' in col:
                        table_row.append(f"{value:.2f}%")
                    else:
                        table_row.append(str(value))
                table_data.append(table_row)
            
            # Créer le tableau
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4b6cb7')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 7),
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

# Fonctions utilitaires
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

def get_secteurs_enseignement():
    """Récupère tous les secteurs d'enseignement disponibles"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT 
                CASE
                    WHEN secteur_enseignement IS NULL OR secteur_enseignement = '' OR UPPER(secteur_enseignement) = 'NONE' THEN 'NR'
                    WHEN UPPER(secteur_enseignement) IN ('AC', 'AU/AC') THEN 'AUTRES'
                    ELSE secteur_enseignement
                END AS secteur
            FROM identifications 
            WHERE secteur_enseignement IS NOT NULL 
            ORDER BY secteur
        """)
        return [row[0] for row in cursor.fetchall()]

def get_regimes_gestion():
    """Récupère tous les régimes de gestion disponibles"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT 
                CASE
                    WHEN regime_gestion IS NULL OR regime_gestion = '' OR UPPER(regime_gestion) = 'NONE' THEN 'NR'
                    WHEN UPPER(regime_gestion) IN ('ECC', 'ECF', 'ECI', 'ECK', 'ECP', 'ECS', 'ENC', 'EPR') THEN regime_gestion
                    ELSE 'AUTRES'
                END AS regime
            FROM identifications 
            WHERE regime_gestion IS NOT NULL 
            ORDER BY regime
        """)
        return [row[0] for row in cursor.fetchall()]






# TRANSVERSAUX
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

def themes_transversaux(request):
    """Vue principale pour les thèmes transversaux"""
    context = {
        'annees_scolaires': get_annees_scolaires(),
        'provinces': get_provinces(),
        'types_enseignement': get_types_enseignement(),
        'secteurs_enseignement': get_secteurs_enseignement(),
    }
    return render(request, 'annuaires/themes_transversaux.html', context)

@csrf_exempt
def get_themes_data(request):
    """Endpoint AJAX pour récupérer les données des thèmes transversaux avec pagination"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rapport_type = data.get('rapport_type', 'par_province')
            filters = data.get('filters', {})
            page = int(data.get('page', 1))
            page_size = int(data.get('page_size', 10))
            
            # Calculer l'offset pour la pagination
            offset = (page - 1) * page_size
            
            # Construire les conditions WHERE et les paramètres
            where_conditions = ["f.responded = 1"]
            params = []
            param_count = 0
            
            # Appliquer les filtres
            annee = filters.get('annee')
            if annee:
                where_conditions.append(f"f.idannee = %s")
                params.append(annee)
                param_count += 1
                
            type_enseignement = filters.get('type_enseignement')
            if type_enseignement:
                where_conditions.append(f"UPPER(f.type) = UPPER(%s)")
                params.append(type_enseignement)
                param_count += 1
                
            province = filters.get('province')
            if province:
                where_conditions.append(f"p.id = %s")
                params.append(province)
                param_count += 1
            
            secteur = filters.get('secteur')
            if secteur:
                if secteur.upper() == 'NR':
                    where_conditions.append("(i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE')")
                else:
                    where_conditions.append(f"UPPER(i.secteur_enseignement) = UPPER(%s)")
                    params.append(secteur)
                    param_count += 1
            
            where_clause = " AND ".join(where_conditions)
            
            # DEBUG
            print("=== DEBUG ===")
            print("Where clause:", where_clause)
            print("Params:", params)
            print("Param count:", param_count)
            print("Rapport type:", rapport_type)
            
            # Sélectionner la requête en fonction du type de rapport
            if rapport_type == 'par_secteur':
                query = get_themes_par_secteur_query(where_clause, page_size, offset)
                count_query = get_themes_par_secteur_count_query(where_clause)
            else:  # par_province par défaut
                query = get_themes_par_province_query(where_clause, page_size, offset)
                count_query = get_themes_par_province_count_query(where_clause)
            
            print("Query:", query)
            print("Count query:", count_query)
            
            # Exécuter la requête de comptage pour le total
            with connection.cursor() as cursor:
                cursor.execute(count_query, params)
                total_count = cursor.fetchone()[0]
            
            print("Total count:", total_count)
            
            # Exécuter la requête principale avec pagination
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                columns = [col[0] for col in cursor.description]
                results = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
            
            print("Results count:", len(results))
            
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
            import traceback
            print("=== ERREUR ===")
            print("Error:", str(e))
            print("Traceback:", traceback.format_exc())
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})

def export_themes_excel(request):
    """Export Excel des thèmes transversaux"""
    try:
        rapport_type = request.GET.get('rapport_type', 'par_province')
        filters = {
            'annee': request.GET.get('annee', ''),
            'type_enseignement': request.GET.get('type_enseignement', ''),
            'province': request.GET.get('province', ''),
            'secteur': request.GET.get('secteur', '')
        }
        
        # Construire les conditions WHERE
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
        
        secteur = filters.get('secteur')
        if secteur:
            if secteur.upper() == 'NR':
                where_conditions.append("(i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE')")
            else:
                where_conditions.append("UPPER(i.secteur_enseignement) = UPPER(%s)")
                params.append(secteur)
        
        where_clause = " AND ".join(where_conditions)
        
        # Sélectionner la requête
        if rapport_type == 'par_secteur':
            query = get_themes_par_secteur_query(where_clause)
            title = "Thèmes Transversaux par Secteur d'Enseignement"
        else:
            query = get_themes_par_province_query(where_clause)
            title = "Thèmes Transversaux par Province"
        
        # Exécuter la requête
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Créer le fichier Excel
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="themes_transversaux_{rapport_type}_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.xls"'
        
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Thèmes Transversaux')
        
        # Styles
        header_style = xlwt.easyxf('font: bold on; align: horiz center; pattern: pattern solid, fore_color light_blue;')
        theme_style = xlwt.easyxf('font: bold on; pattern: pattern solid, fore_color light_green;')
        normal_style = xlwt.easyxf('align: horiz left;')
        number_style = xlwt.easyxf('align: horiz right;')
        
        # En-tête du document
        row_num = 0
        ws.write(row_num, 0, title, header_style)
        row_num += 1
        ws.write(row_num, 0, f"Généré le: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
        row_num += 2
        
        # En-têtes des colonnes
        for col_num, column_title in enumerate(columns):
            ws.write(row_num, col_num, column_title, header_style)
            ws.col(col_num).width = 4000
        
        row_num += 1
        
        # Données
        current_theme = None
        for row in results:
            # Style différent pour les nouveaux thèmes
            if current_theme != row.get('Thèmes transversaux'):
                current_theme = row.get('Thèmes transversaux')
                style = theme_style
            else:
                style = normal_style
            
            for col_num, column_title in enumerate(columns):
                value = row.get(column_title, '')
                if isinstance(value, (int, float)):
                    ws.write(row_num, col_num, value, number_style)
                else:
                    ws.write(row_num, col_num, str(value), style)
            row_num += 1
        
        # Pied de page
        row_num += 1
        ws.write(row_num, 0, f"Total: {len(results)} enregistrements")
        
        wb.save(response)
        return response
        
    except Exception as e:
        return HttpResponse(f"Erreur lors de l'export Excel: {str(e)}")

def export_themes_pdf(request):
    """Export PDF des thèmes transversaux"""
    try:
        rapport_type = request.GET.get('rapport_type', 'par_province')
        filters = {
            'annee': request.GET.get('annee', ''),
            'type_enseignement': request.GET.get('type_enseignement', ''),
            'province': request.GET.get('province', ''),
            'secteur': request.GET.get('secteur', '')
        }
        
        # Construire les conditions WHERE
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
        
        secteur = filters.get('secteur')
        if secteur:
            if secteur.upper() == 'NR':
                where_conditions.append("(i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE')")
            else:
                where_conditions.append("UPPER(i.secteur_enseignement) = UPPER(%s)")
                params.append(secteur)
        
        where_clause = " AND ".join(where_conditions)
        
        # Sélectionner la requête
        if rapport_type == 'par_secteur':
            query = get_themes_par_secteur_query(where_clause)
            title = "Thèmes Transversaux par Secteur d'Enseignement"
        else:
            query = get_themes_par_province_query(where_clause)
            title = "Thèmes Transversaux par Province"
        
        # Exécuter la requête
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Créer le PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="themes_transversaux_{rapport_type}_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.pdf"'
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        elements = []
        
        styles = getSampleStyleSheet()
        
        # Titre
        title_text = f"RAPPORT - {title}"
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
        if filters['secteur']:
            filters_list.append(f"Secteur: {filters['secteur']}")
        
        if filters_list:
            filters_text += " | ".join(filters_list)
            elements.append(Paragraph(filters_text, styles['Normal']))
        
        elements.append(Paragraph(" ", styles['Normal']))  # Espace
        
        # Préparer les données pour le tableau
        if results:
            # En-têtes
            table_data = [columns]
            
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
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
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

def export_themes_csv(request):
    """Export CSV des thèmes transversaux"""
    try:
        rapport_type = request.GET.get('rapport_type', 'par_province')
        filters = {
            'annee': request.GET.get('annee', ''),
            'type_enseignement': request.GET.get('type_enseignement', ''),
            'province': request.GET.get('province', ''),
            'secteur': request.GET.get('secteur', '')
        }
        
        # Construire les conditions WHERE
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
        
        secteur = filters.get('secteur')
        if secteur:
            if secteur.upper() == 'NR':
                where_conditions.append("(i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE')")
            else:
                where_conditions.append("UPPER(i.secteur_enseignement) = UPPER(%s)")
                params.append(secteur)
        
        where_clause = " AND ".join(where_conditions)
        
        # Sélectionner la requête
        if rapport_type == 'par_secteur':
            query = get_themes_par_secteur_query(where_clause)
            title = "Thèmes Transversaux par Secteur d'Enseignement"
        else:
            query = get_themes_par_province_query(where_clause)
            title = "Thèmes Transversaux par Province"
        
        # Exécuter la requête
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Créer le CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="themes_transversaux_{rapport_type}_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.csv"'
        
        response.write(u'\ufeff'.encode('utf8'))  # BOM pour Excel
        writer = csv.writer(response)
        
        # En-tête
        writer.writerow([title])
        writer.writerow([f"Généré le: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}"])
        writer.writerow([])
        
        # En-têtes des colonnes
        writer.writerow(columns)
        
        # Données
        for row in results:
            writer.writerow([str(row.get(col, '')) for col in columns])
        
        writer.writerow([])
        writer.writerow([f"Total: {len(results)} enregistrements"])
        
        return response
        
    except Exception as e:
        return HttpResponse(f"Erreur lors de l'export CSV: {str(e)}")

# Fonctions pour les requêtes principales - CORRIGÉES
def get_themes_par_province_query(where_clause, page_size=None, offset=0):
    # Utiliser des f-strings pour éviter les problèmes de formatage
    limit_clause = ""
    if page_size is not None:
        limit_clause = f" LIMIT {page_size} OFFSET {offset}"
    
    return f"""
    WITH themes_par_annee_type_province AS (
        SELECT
            f.idannee,
            f.type,
            p.id AS province_id,
            p.libelle AS province,
            'le VIH/SIDA' AS theme_transversal,
            SUM(COALESCE(s.sante_reproductive_enseigne, 0)) AS nombre_programme_officiel,
            0 AS nombre_discipline,
            0 AS nombre_parascolaire
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        JOIN provinces p ON i.fk_province_id = p.id
        LEFT JOIN sante_sexuelle_reproductive s ON f.id = s.form_st_id
        WHERE {where_clause}
        GROUP BY f.idannee, f.type, p.id, p.libelle

        UNION ALL

        SELECT
            f.idannee,
            f.type,
            p.id AS province_id,
            p.libelle AS province,
            'La santé sexuelle et reproductive' AS theme_transversal,
            SUM(COALESCE(s.sante_reproductive_programme, 0)) AS nombre_programme_officiel,
            0 AS nombre_discipline,
            0 AS nombre_parascolaire
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        JOIN provinces p ON i.fk_province_id = p.id
        LEFT JOIN sante_sexuelle_reproductive s ON f.id = s.form_st_id
        WHERE {where_clause}
        GROUP BY f.idannee, f.type, p.id, p.libelle

        UNION ALL

        SELECT
            f.idannee,
            f.type,
            p.id AS province_id,
            p.libelle AS province,
            'La sensibilisation contre les abus et les violences' AS theme_transversal,
            0 AS nombre_programme_officiel,
            SUM(COALESCE(s.sante_reproductive_discipline, 0)) AS nombre_discipline,
            0 AS nombre_parascolaire
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        JOIN provinces p ON i.fk_province_id = p.id
        LEFT JOIN sante_sexuelle_reproductive s ON f.id = s.form_st_id
        WHERE {where_clause}
        GROUP BY f.idannee, f.type, p.id, p.libelle

        UNION ALL

        SELECT
            f.idannee,
            f.type,
            p.id AS province_id,
            p.libelle AS province,
            'l''éducation environnementale' AS theme_transversal,
            0 AS nombre_programme_officiel,
            0 AS nombre_discipline,
            SUM(COALESCE(s.sante_reproductive_parascolaire, 0)) AS nombre_parascolaire
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        JOIN provinces p ON i.fk_province_id = p.id
        LEFT JOIN sante_sexuelle_reproductive s ON f.id = s.form_st_id
        WHERE {where_clause}
        GROUP BY f.idannee, f.type, p.id, p.libelle
    )

    SELECT
        t.idannee AS `Année`,
        t.type AS `Type`,
        t.province_id AS `ID Province`,
        t.province AS `Province`,
        t.theme_transversal AS `Thèmes transversaux`,
        t.nombre_programme_officiel AS `Dont : Programme officiel`,
        t.nombre_discipline AS `Dont : Discipline à part`,
        t.nombre_parascolaire AS `Dont : Activités parascolaires`
    FROM themes_par_annee_type_province t
    ORDER BY t.idannee, t.type, t.province_id, t.theme_transversal
    {limit_clause}
    """

def get_themes_par_secteur_query(where_clause, page_size=None, offset=0):
    # Utiliser des f-strings pour éviter les problèmes de formatage
    limit_clause = ""
    if page_size is not None:
        limit_clause = f" LIMIT {page_size} OFFSET {offset}"
    
    return f"""
    WITH themes_par_annee_type_secteur AS (
        SELECT
            f.idannee,
            f.type,
            CASE
                WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
                ELSE i.secteur_enseignement
            END AS secteur_enseignement,
            'le VIH/SIDA' AS theme_transversal,
            SUM(COALESCE(s.sante_reproductive_enseigne, 0)) AS nombre_programme_officiel,
            0 AS nombre_discipline,
            0 AS nombre_parascolaire
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        LEFT JOIN sante_sexuelle_reproductive s ON f.id = s.form_st_id
        WHERE {where_clause}
        GROUP BY f.idannee, f.type, 
            CASE
                WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
                ELSE i.secteur_enseignement
            END

        UNION ALL

        SELECT
            f.idannee,
            f.type,
            CASE
                WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
                ELSE i.secteur_enseignement
            END AS secteur_enseignement,
            'La santé sexuelle et reproductive' AS theme_transversal,
            SUM(COALESCE(s.sante_reproductive_programme, 0)) AS nombre_programme_officiel,
            0 AS nombre_discipline,
            0 AS nombre_parascolaire
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        LEFT JOIN sante_sexuelle_reproductive s ON f.id = s.form_st_id
        WHERE {where_clause}
        GROUP BY f.idannee, f.type, 
            CASE
                WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
                ELSE i.secteur_enseignement
            END

        UNION ALL

        SELECT
            f.idannee,
            f.type,
            CASE
                WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
                ELSE i.secteur_enseignement
            END AS secteur_enseignement,
            'La sensibilisation contre les abus et les violences' AS theme_transversal,
            0 AS nombre_programme_officiel,
            SUM(COALESCE(s.sante_reproductive_discipline, 0)) AS nombre_discipline,
            0 AS nombre_parascolaire
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        LEFT JOIN sante_sexuelle_reproductive s ON f.id = s.form_st_id
        WHERE {where_clause}
        GROUP BY f.idannee, f.type, 
            CASE
                WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
                ELSE i.secteur_enseignement
            END

        UNION ALL

        SELECT
            f.idannee,
            f.type,
            CASE
                WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
                ELSE i.secteur_enseignement
            END AS secteur_enseignement,
            'l''éducation environnementale' AS theme_transversal,
            0 AS nombre_programme_officiel,
            0 AS nombre_discipline,
            SUM(COALESCE(s.sante_reproductive_parascolaire, 0)) AS nombre_parascolaire
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        LEFT JOIN sante_sexuelle_reproductive s ON f.id = s.form_st_id
        WHERE {where_clause}
        GROUP BY f.idannee, f.type, 
            CASE
                WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
                ELSE i.secteur_enseignement
            END
    )

    SELECT
        t.idannee AS `Année`,
        t.type AS `Type`,
        t.secteur_enseignement AS `Secteur d'enseignement`,
        t.theme_transversal AS `Thèmes transversaux`,
        t.nombre_programme_officiel AS `Dont : Programme officiel`,
        t.nombre_discipline AS `Dont : Discipline à part`,
        t.nombre_parascolaire AS `Dont : Activités parascolaires`
    FROM themes_par_annee_type_secteur t
    ORDER BY t.idannee, t.type, 
        CASE WHEN t.secteur_enseignement = 'NR' THEN 1 ELSE 0 END,
        t.secteur_enseignement, t.theme_transversal
    {limit_clause}
    """

# Fonctions de comptage SIMPLIFIÉES
def get_themes_par_province_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        JOIN provinces p ON i.fk_province_id = p.id
        LEFT JOIN sante_sexuelle_reproductive s ON f.id = s.form_st_id
        WHERE {where_clause}
        AND (
            COALESCE(s.sante_reproductive_enseigne, 0) > 0 OR
            COALESCE(s.sante_reproductive_programme, 0) > 0 OR
            COALESCE(s.sante_reproductive_discipline, 0) > 0 OR
            COALESCE(s.sante_reproductive_parascolaire, 0) > 0
        )
        GROUP BY f.idannee, f.type, p.id, p.libelle
    ) AS subquery
    """

def get_themes_par_secteur_count_query(where_clause):
    return f"""
    SELECT COUNT(*) FROM (
        SELECT 1
        FROM formulaires f
        JOIN identifications i ON f.identification_id = i.id
        LEFT JOIN sante_sexuelle_reproductive s ON f.id = s.form_st_id
        WHERE {where_clause}
        AND (
            COALESCE(s.sante_reproductive_enseigne, 0) > 0 OR
            COALESCE(s.sante_reproductive_programme, 0) > 0 OR
            COALESCE(s.sante_reproductive_discipline, 0) > 0 OR
            COALESCE(s.sante_reproductive_parascolaire, 0) > 0
        )
        GROUP BY f.idannee, f.type, 
            CASE
                WHEN i.secteur_enseignement IS NULL OR i.secteur_enseignement = '' OR UPPER(i.secteur_enseignement) = 'NONE' THEN 'NR'
                ELSE i.secteur_enseignement
            END
    ) AS subquery
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

def get_secteurs_enseignement():
    """Récupère tous les secteurs d'enseignement disponibles"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT 
                CASE 
                    WHEN secteur_enseignement IS NULL OR secteur_enseignement = '' OR UPPER(secteur_enseignement) = 'NONE' THEN 'NR'
                    ELSE UPPER(secteur_enseignement)
                END AS secteur
            FROM identifications 
            WHERE secteur_enseignement IS NOT NULL 
            ORDER BY 
                CASE 
                    WHEN secteur_enseignement IS NULL OR secteur_enseignement = '' OR UPPER(secteur_enseignement) = 'NONE' THEN 1
                    ELSE 0
                END,
                secteur_enseignement
        """)
        return [row[0] for row in cursor.fetchall()]


