from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from apps.core.models import Etablissement
from django.shortcuts import render
from django.core.paginator import Paginator
import csv
import chardet
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from io import TextIOWrapper, StringIO
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from apps.core.models import Etablissement, Annee_scolaire, Provinces, Proveds, Sous_proved
import tempfile
import os
import csv
import chardet
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from io import TextIOWrapper, StringIO

def tablissement_table(request):
    # Récupérer tous les établissements non supprimés avec les relations
    etablissements_list = Etablissement.objects.filter(isDeleted=False)\
        .select_related(
            'anneeId', 
            'provinceId', 
            'provedId', 
            'sousProvedId'
        )\
        .order_by('-createdAt')
    
    # Pagination
    paginator = Paginator(etablissements_list, 10)
    page_number = request.GET.get('page')
    etablissements = paginator.get_page(page_number)
    
    context = {
        'etablissements': etablissements,
    }
    
    return render(request, 'etablissement/etablissement_table.html', context)

def detail_etablissement(request, etablissement_id):
    try:
        etablissement = Etablissement.objects.select_related(
            'anneeId', 'provinceId', 'provedId', 'sousProvedId',
            'informations_generale_id', 'localisation_administrative_id',
            'localisation_scolaire_id', 'territoireId', 
            'reference_juridique_id', 'identification_id'
        ).get(id=etablissement_id, isDeleted=False)
        
        context = {
            'etablissement': etablissement
        }
        
        return render(request, 'etablissement/detail.html', context)
    except Etablissement.DoesNotExist:
        return HttpResponse("Établissement introuvable.", status=404)
    except Exception as e:
        return HttpResponse(f"Erreur lors de la récupération: {str(e)}", status=500)

def etablissement_form(request):
    if request.method == 'POST':
        # Récupération des données du formulaire
        anneeId_id = request.POST.get('anneeId')
        nomEtablissement = request.POST.get('nomEtablissement')
        type_enseignement = request.POST.get('type_enseignement')
        NomChefEtablissement = request.POST.get('NomChefEtablissement')
        adresseEtablissement = request.POST.get('adresseEtablissement')
        TelephoneEtablissement = request.POST.get('TelephoneEtablissement')
        provinceId_id = request.POST.get('provinceId')
        provedId_id = request.POST.get('provedId')
        sousProvedId_id = request.POST.get('sousProvedId')
        informations_generale_id_id = request.POST.get('informations_generale_id')
        localisation_administrative_id_id = request.POST.get('localisation_administrative_id')
        localisation_scolaire_id_id = request.POST.get('localisation_scolaire_id')
        territoireId_id = request.POST.get('territoireId')
        reference_juridique_id_id = request.POST.get('reference_juridique_id')
        identification_id_id = request.POST.get('identification_id')
        nom_norm = request.POST.get('nom_norm')

        try:
            # Création de l'établissement
            etablissement = Etablissement.objects.create(
                anneeId_id=anneeId_id,
                nomEtablissement=nomEtablissement,
                type_enseignement=type_enseignement,
                NomChefEtablissement=NomChefEtablissement,
                adresseEtablissement=adresseEtablissement,
                TelephoneEtablissement=TelephoneEtablissement,
                provinceId_id=provinceId_id,
                provedId_id=provedId_id,
                sousProvedId_id=sousProvedId_id,
                informations_generale_id_id=informations_generale_id_id,
                localisation_administrative_id_id=localisation_administrative_id_id,
                localisation_scolaire_id_id=localisation_scolaire_id_id,
                territoireId_id=territoireId_id,
                reference_juridique_id_id=reference_juridique_id_id,
                identification_id_id=identification_id_id,
                nom_norm=nom_norm
            )
            
            return HttpResponse(f"Établissement {etablissement.nomEtablissement} créé avec succès!")
            
        except Exception as e:
            return HttpResponse(f"Erreur lors de la création: {str(e)}")

    # Si méthode GET, afficher le formulaire
    return render(request, 'etablissement/etablissement_forms.html', locals())

def import_etablissements(request):
    context = {
        'annees': Annee_scolaire.objects.all(),
        'provinces': Provinces.objects.all(),
        'proveds': Proveds.objects.all(),
        'sous_proveds': Sous_proved.objects.all(),
    }
    return render(request, 'etablissement/import.html', context)

def import_excel(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        
        # Vérifier l'extension du fichier
        if not excel_file.name.endswith(('.xlsx', '.xls')):
            messages.error(request, "Le fichier doit être au format Excel (.xlsx ou .xls)")
            return redirect('etablissement')
        
        try:
            # Sauvegarder le fichier temporairement
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                for chunk in excel_file.chunks():
                    tmp_file.write(chunk)
                tmp_path = tmp_file.name
            
            # Lire le fichier Excel
            df = pd.read_excel(tmp_path)
            
            # Nettoyer le fichier temporaire
            os.unlink(tmp_path)
            
            # Vérifier les colonnes requises
            required_columns = ['nomEtablissement', 'anneeId', 'provinceId']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                messages.error(request, f"Colonnes manquantes dans le fichier Excel: {', '.join(missing_columns)}")
                return redirect('etablissement')
            
            # Traiter chaque ligne
            success_count = 0
            error_count = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    # Vérifier les clés étrangères
                    try:
                        annee = Annee_scolaire.objects.get(id=row['anneeId'])
                    except Annee_scolaire.DoesNotExist:
                        errors.append(f"Ligne {index + 2}: Année scolaire ID {row['anneeId']} non trouvé")
                        error_count += 1
                        continue
                    
                    try:
                        province = Provinces.objects.get(id=row['provinceId'])
                    except Provinces.DoesNotExist:
                        errors.append(f"Ligne {index + 2}: Province ID {row['provinceId']} non trouvé")
                        error_count += 1
                        continue
                    
                    # Vérifier les autres ForeignKeys si présentes
                    proved = None
                    if 'provedId' in df.columns and pd.notna(row['provedId']):
                        try:
                            proved = Proveds.objects.get(id=row['provedId'])
                        except Proveds.DoesNotExist:
                            errors.append(f"Ligne {index + 2}: Proved ID {row['provedId']} non trouvé")
                            error_count += 1
                            continue
                    
                    sous_proved = None
                    if 'sousProvedId' in df.columns and pd.notna(row['sousProvedId']):
                        try:
                            sous_proved = Sous_proved.objects.get(id=row['sousProvedId'])
                        except Sous_proved.DoesNotExist:
                            errors.append(f"Ligne {index + 2}: Sous-proved ID {row['sousProvedId']} non trouvé")
                            error_count += 1
                            continue
                    
                    # Créer l'établissement
                    etablissement = Etablissement(
                        nomEtablissement=row['nomEtablissement'],
                        anneeId=annee,
                        provinceId=province,
                        type_enseignement=row.get('type_enseignement'),
                        NomChefEtablissement=row.get('NomChefEtablissement'),
                        adresseEtablissement=row.get('adresseEtablissement'),
                        TelephoneEtablissement=row.get('TelephoneEtablissement'),
                        provedId=proved,
                        sousProvedId=sous_proved,
                        nom_norm=row.get('nom_norm'),
                        isActive=row.get('isActive', True)
                    )
                    
                    etablissement.save()
                    success_count += 1
                    
                except Exception as e:
                    errors.append(f"Ligne {index + 2}: {str(e)}")
                    error_count += 1
            
            # Messages de résultat
            if success_count > 0:
                messages.success(request, f"{success_count} établissement(s) importé(s) avec succès!")
            
            if error_count > 0:
                messages.warning(request, f"{error_count} erreur(s) lors de l'importation")
                # Stocker les erreurs détaillées dans la session
                request.session['import_errors'] = errors[:10]  # Limiter à 10 erreurs
            
        except Exception as e:
            messages.error(request, f"Erreur lors de la lecture du fichier Excel: {str(e)}")
        
        return redirect('etablissement')
    
    return redirect('etablissement')

def import_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        # Vérifier l'extension du fichier
        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Le fichier doit être au format CSV")
            return redirect('etablissement')
        
        try:
            # Détecter l'encodage du fichier
            raw_data = csv_file.read()
            encoding = chardet.detect(raw_data)['encoding']
            
            # Réinitialiser le fichier
            csv_file.seek(0)
            
            # Lire le fichier CSV
            csv_text = TextIOWrapper(csv_file, encoding=encoding)
            reader = csv.DictReader(csv_text, delimiter=';')
            
            # Vérifier les colonnes requises
            required_columns = ['nomEtablissement', 'anneeId', 'provinceId']
            missing_columns = [col for col in required_columns if col not in reader.fieldnames]
            
            if missing_columns:
                messages.error(request, f"Colonnes manquantes dans le fichier CSV: {', '.join(missing_columns)}")
                return redirect('etablissement')
            
            # Traiter chaque ligne
            success_count = 0
            error_count = 0
            errors = []
            line_number = 1
            
            for row in reader:
                line_number += 1
                try:
                    # Nettoyer les valeurs
                    cleaned_row = {k: (v.strip() if v else None) for k, v in row.items()}
                    
                    # Vérifier les clés étrangères
                    try:
                        annee = Annee_scolaire.objects.get(id=cleaned_row['anneeId'])
                    except (Annee_scolaire.DoesNotExist, ValueError):
                        errors.append(f"Ligne {line_number}: Année scolaire ID {cleaned_row['anneeId']} non trouvé")
                        error_count += 1
                        continue
                    
                    try:
                        province = Provinces.objects.get(id=cleaned_row['provinceId'])
                    except (Provinces.DoesNotExist, ValueError):
                        errors.append(f"Ligne {line_number}: Province ID {cleaned_row['provinceId']} non trouvé")
                        error_count += 1
                        continue
                    
                    # Vérifier les autres ForeignKeys si présentes
                    proved = None
                    if 'provedId' in cleaned_row and cleaned_row['provedId']:
                        try:
                            proved = Proveds.objects.get(id=cleaned_row['provedId'])
                        except (Proveds.DoesNotExist, ValueError):
                            errors.append(f"Ligne {line_number}: Proved ID {cleaned_row['provedId']} non trouvé")
                            error_count += 1
                            continue
                    
                    sous_proved = None
                    if 'sousProvedId' in cleaned_row and cleaned_row['sousProvedId']:
                        try:
                            sous_proved = Sous_proved.objects.get(id=cleaned_row['sousProvedId'])
                        except (Sous_proved.DoesNotExist, ValueError):
                            errors.append(f"Ligne {line_number}: Sous-proved ID {cleaned_row['sousProvedId']} non trouvé")
                            error_count += 1
                            continue
                    
                    # Gérer les valeurs booléennes
                    is_active = True
                    if 'isActive' in cleaned_row:
                        is_active = cleaned_row['isActive'].lower() in ['true', '1', 'yes', 'oui']
                    
                    # Créer l'établissement
                    etablissement = Etablissement(
                        nomEtablissement=cleaned_row['nomEtablissement'],
                        anneeId=annee,
                        provinceId=province,
                        type_enseignement=cleaned_row.get('type_enseignement'),
                        NomChefEtablissement=cleaned_row.get('NomChefEtablissement'),
                        adresseEtablissement=cleaned_row.get('adresseEtablissement'),
                        TelephoneEtablissement=cleaned_row.get('TelephoneEtablissement'),
                        provedId=proved,
                        sousProvedId=sous_proved,
                        nom_norm=cleaned_row.get('nom_norm'),
                        isActive=is_active
                    )
                    
                    etablissement.save()
                    success_count += 1
                    
                except Exception as e:
                    errors.append(f"Ligne {line_number}: {str(e)}")
                    error_count += 1
            
            # Messages de résultat
            if success_count > 0:
                messages.success(request, f"{success_count} établissement(s) importé(s) avec succès!")
            
            if error_count > 0:
                messages.warning(request, f"{error_count} erreur(s) lors de l'importation")
                request.session['import_errors'] = errors[:10]
            
        except Exception as e:
            messages.error(request, f"Erreur lors de la lecture du fichier CSV: {str(e)}")
        
        return redirect('etablissement')
    
    return redirect('etablissement')

