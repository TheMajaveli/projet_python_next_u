"""
Routes pour les fonctionnalités de mobilité
"""

from flask import Blueprint, render_template, request, jsonify
import logging
import pandas as pd
from app.utils.data_loader import DataLoader
from app.utils.cache import get_cached_stats
from script import main

logger = logging.getLogger(__name__)

# Créer un Blueprint pour les routes mobilité
bp = Blueprint('mobilite', __name__, url_prefix='/mobilite')

# Initialiser le chargeur de données
data_loader = DataLoader()


@bp.route('/communes')
def communes():
    """
    Page affichant les indicateurs par commune avec filtres et pagination
    Charge seulement les options de filtres, les données sont chargées via API
    """
    try:
        # Charger les options de filtres
        regions_list = data_loader.get_regions_list()
        age_ranges_list = data_loader.get_age_ranges_from_data()
        
        # Récupérer les filtres actuels depuis l'URL
        region_filter = request.args.get('region', '')
        department_filter = request.args.get('department', '')
        age_filter = request.args.get('age', '')
        
        # Charger les départements seulement si une région est sélectionnée
        departments_list = []
        if region_filter:
            departments_list = data_loader.get_departments_by_region(region_filter)
        
        return render_template('mobilite/communes.html', 
                             regions_list=regions_list,
                             departments_list=departments_list,
                             age_ranges_list=age_ranges_list,
                             region_filter=region_filter,
                             department_filter=department_filter,
                             age_filter=age_filter)
    except Exception as e:
        logger.error(f"Erreur lors du chargement de la page communes: {e}", exc_info=True)
        return render_template('mobilite/communes.html', 
                             regions_list=[],
                             departments_list=[],
                             age_ranges_list=[],
                             transport_types_list=[],
                             error=str(e))


@bp.route('/api/communes')
def api_communes():
    """
    API endpoint pour charger les communes avec pagination et filtres
    Calcule les pourcentages réels par type de transport pour chaque commune
    """
    try:
        import re
        import pandas as pd
        
        # Récupérer les paramètres
        region_filter = request.args.get('region', '')
        department_filter = request.args.get('department', '')
        age_filter = request.args.get('age', '')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Charger les statistiques globales pour les indicateurs généraux (avec cache)
        stats = get_cached_stats(main)
        
        # Charger les communes
        communes_df = data_loader.load_communes_data()
        
        if communes_df.empty:
            return jsonify({
                'communes': [],
                'total_count': 0,
                'total_pages': 0,
                'page': page,
                'per_page': per_page
            })
        
        # Appliquer les filtres géographiques AVANT de calculer les indicateurs
        if region_filter and 'REG' in communes_df.columns:
            communes_df = communes_df[communes_df['REG'].astype(str) == str(region_filter)]
        
        if department_filter and 'DEP' in communes_df.columns:
            communes_df = communes_df[communes_df['DEP'].astype(str) == str(department_filter)]
        
        # Obtenir les codes communes filtrés
        commune_codes = set()
        if 'COM' in communes_df.columns:
            commune_codes.update(communes_df['COM'].astype(str).str.zfill(5).tolist())
        if 'CODCOM' in communes_df.columns:
            commune_codes.update(communes_df['CODCOM'].astype(str).str.zfill(5).tolist())
        
        # Charger les données de mobilité
        mobility_df = data_loader.load_mobility_data()
        
        if mobility_df.empty:
            # Si pas de données de mobilité, retourner avec valeurs par défaut
            return jsonify({
                'communes': [],
                'total_count': 0,
                'total_pages': 0,
                'page': page,
                'per_page': per_page
            })
        
        # Extraire le code commune depuis la colonne COMMUNE (format: "Nom (CODE)")
        mobility_df['COMMUNE_CODE'] = mobility_df['COMMUNE'].astype(str).str.extract(r'\((\d+)\)', expand=False)
        mobility_df['COMMUNE_CODE'] = mobility_df['COMMUNE_CODE'].astype(str).str.zfill(5)
        
        # Filtrer par codes communes
        if commune_codes:
            mobility_df = mobility_df[mobility_df['COMMUNE_CODE'].isin(commune_codes)]
        
        # Filtrer par tranche d'âge si spécifié
        if age_filter:
            age_values = data_loader.map_age_filter_to_agerevq_values(age_filter)
            if age_values:
                mobility_df = mobility_df[mobility_df['AGEREVQ'].isin(age_values)]
        
        # Calculer les pourcentages par type de transport pour chaque commune
        if len(mobility_df) > 0:
            # Définir les catégories de transport
            transport_categories = {
                'velo': ['Vélo (y compris à assistance électrique)'],
                'voiture': ['Voiture, camion, fourgonnette'],
                'transport_commun': ['Transports en commun'],
                'marche': ['Marche à pied (ou rollers, patinette)'],
                'deux_roues': ['Deux-roues motorisé'],
                'pas_transport': ['Pas de transport']
            }
            
            # Calculer la population totale par commune
            commune_pop = mobility_df.groupby('COMMUNE_CODE')['IPONDI'].sum().reset_index()
            commune_pop.columns = ['COMMUNE_CODE', 'total_pop']
            
            # Calculer les pourcentages pour chaque type de transport
            transport_stats = []
            for transport_type, transport_values in transport_categories.items():
                transport_df = mobility_df[mobility_df['TRANS'].isin(transport_values)]
                if len(transport_df) > 0:
                    transport_pop = transport_df.groupby('COMMUNE_CODE')['IPONDI'].sum().reset_index()
                    transport_pop.columns = ['COMMUNE_CODE', f'{transport_type}_pop']
                    transport_stats.append(transport_pop)
            
            # Fusionner toutes les statistiques
            result_df = commune_pop.copy()
            for stat_df in transport_stats:
                result_df = result_df.merge(stat_df, on='COMMUNE_CODE', how='left')
            
            # Calculer les pourcentages
            for transport_type in transport_categories.keys():
                pop_col = f'{transport_type}_pop'
                if pop_col in result_df.columns:
                    result_df[f'{transport_type}_percentage'] = (result_df[pop_col] / result_df['total_pop'] * 100).fillna(0).round(1)
                else:
                    result_df[f'{transport_type}_percentage'] = 0.0
            
            # Joindre avec les données des communes
            communes_df = communes_df.copy()
            communes_df['COMMUNE_CODE'] = communes_df.get('COM', communes_df.get('CODCOM', '')).astype(str).str.zfill(5)
            communes_df = communes_df.merge(result_df[['COMMUNE_CODE'] + [f'{t}_percentage' for t in transport_categories.keys()]], 
                                            on='COMMUNE_CODE', how='left')
            
            # Remplir les valeurs manquantes par 0
            for transport_type in transport_categories.keys():
                col = f'{transport_type}_percentage'
                if col not in communes_df.columns:
                    communes_df[col] = 0.0
                communes_df[col] = communes_df[col].fillna(0.0)
        
        # Calculer les indicateurs généraux (green_mobility_index, avg_commute_time)
        # basés sur les pourcentages réels calculés
        if len(communes_df) > 0:
            communes_df = communes_df.copy()
            
            # Ajuster la population selon la tranche d'âge sélectionnée
            population_adjustment_factor = 1.0
            if age_filter:
                if age_filter in ['0-18', '19-35']:
                    population_adjustment_factor = 0.28
                elif age_filter == '36-50':
                    population_adjustment_factor = 0.32
                elif age_filter in ['51-65', '65+']:
                    population_adjustment_factor = 0.22
            
            if 'PTOT' in communes_df.columns:
                communes_df['PTOT'] = (communes_df['PTOT'] * population_adjustment_factor).round(0).astype(int)
            
            # Calculer l'indice de mobilité verte basé sur les pourcentages réels
            # (vélo + transports en commun * 0.8)
            velo_pct = communes_df['velo_percentage'] if 'velo_percentage' in communes_df.columns else pd.Series([0.0] * len(communes_df), index=communes_df.index)
            tc_pct = communes_df['transport_commun_percentage'] if 'transport_commun_percentage' in communes_df.columns else pd.Series([0.0] * len(communes_df), index=communes_df.index)
            communes_df['green_mobility_index'] = (velo_pct + tc_pct * 0.8).round(1)
            
            # Calculer le temps de trajet moyen (basé sur les stats globales avec variation par population)
            base_avg_commute = stats.get('pourcentage_temps_moyen', 30)
            population_max = communes_df['PTOT'].max() if 'PTOT' in communes_df.columns else 1
            population_factor = (communes_df['PTOT'] / population_max) if population_max > 0 else 0
            communes_df['avg_commute_time'] = (base_avg_commute + (population_factor * 5)).round(1)
        
        # S'assurer que toutes les colonnes de transport sont présentes (avec 0.0 par défaut)
        transport_cols = ['velo_percentage', 'voiture_percentage', 'transport_commun_percentage', 
                          'marche_percentage', 'deux_roues_percentage', 'pas_transport_percentage']
        for col in transport_cols:
            if col not in communes_df.columns:
                communes_df[col] = 0.0
        
        # Sélectionner les colonnes nécessaires
        base_cols = ['Commune', 'COM', 'CODCOM', 'PTOT', 'green_mobility_index', 'avg_commute_time']
        display_cols = base_cols + transport_cols
        available_cols = [col for col in display_cols if col in communes_df.columns]
        communes_df = communes_df[available_cols].copy()
        communes_df = communes_df.rename(columns={'Commune': 'LIBGEO'})
        
        
        # Pagination APRÈS filtrage
        total_count = len(communes_df)
        start = (page - 1) * per_page
        end = start + per_page
        communes_list = communes_df.iloc[start:end].to_dict('records')
        
        total_pages = (total_count + per_page - 1) // per_page if total_count > 0 else 1
        
        return jsonify({
            'communes': communes_list,
            'total_count': total_count,
            'total_pages': total_pages,
            'page': page,
            'per_page': per_page
        })
    except Exception as e:
        logger.error(f"Erreur API communes: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@bp.route('/api/communes/<code>')
def api_commune_detail(code):
    """
    API endpoint pour charger les détails d'une commune spécifique avec filtres
    """
    try:
        import re
        import pandas as pd
        
        # Récupérer les paramètres de filtres
        region_filter = request.args.get('region', '')
        department_filter = request.args.get('department', '')
        age_filter = request.args.get('age', '')
        
        # Charger les statistiques globales (avec cache)
        stats = get_cached_stats(main)
        
        # Charger les communes
        communes_df = data_loader.load_communes_data()
        
        if communes_df.empty:
            return jsonify({'error': 'Aucune donnée de commune disponible'}), 404
        
        # Appliquer les filtres géographiques
        if region_filter and 'REG' in communes_df.columns:
            communes_df = communes_df[communes_df['REG'].astype(str) == str(region_filter)]
        
        if department_filter and 'DEP' in communes_df.columns:
            communes_df = communes_df[communes_df['DEP'].astype(str) == str(department_filter)]
        
        # Trouver la commune par code
        commune_data = None
        code_str = str(code).zfill(5)
        
        if 'COM' in communes_df.columns:
            commune_match = communes_df[communes_df['COM'].astype(str).str.zfill(5) == code_str]
            if not commune_match.empty:
                commune_data = commune_match.iloc[0].to_dict()
        
        if commune_data is None and 'CODCOM' in communes_df.columns:
            commune_match = communes_df[communes_df['CODCOM'].astype(str).str.zfill(5) == code_str]
            if not commune_match.empty:
                commune_data = commune_match.iloc[0].to_dict()
        
        if commune_data is None:
            return jsonify({'error': f'Commune avec le code {code} non trouvée'}), 404
        
        # Obtenir le code commune pour filtrer les données de mobilité
        commune_code = str(commune_data.get('COM', commune_data.get('CODCOM', ''))).zfill(5)
        
        # Charger les données de mobilité
        mobility_df = data_loader.load_mobility_data()
        
        if mobility_df.empty:
            return jsonify({'error': 'Aucune donnée de mobilité disponible'}), 404
        
        # Extraire le code commune depuis la colonne COMMUNE
        mobility_df['COMMUNE_CODE'] = mobility_df['COMMUNE'].astype(str).str.extract(r'\((\d+)\)', expand=False)
        mobility_df['COMMUNE_CODE'] = mobility_df['COMMUNE_CODE'].astype(str).str.zfill(5)
        
        # Filtrer par code commune
        mobility_df = mobility_df[mobility_df['COMMUNE_CODE'] == commune_code]
        
        # Filtrer par tranche d'âge si spécifié
        if age_filter:
            age_values = data_loader.map_age_filter_to_agerevq_values(age_filter)
            if age_values:
                mobility_df = mobility_df[mobility_df['AGEREVQ'].isin(age_values)]
        
        # Calculer les pourcentages par type de transport
        transport_categories = {
            'velo': ['Vélo (y compris à assistance électrique)'],
            'voiture': ['Voiture, camion, fourgonnette'],
            'transport_commun': ['Transports en commun'],
            'marche': ['Marche à pied (ou rollers, patinette)'],
            'deux_roues': ['Deux-roues motorisé'],
            'pas_transport': ['Pas de transport']
        }
        
        # Calculer la population totale
        total_pop = mobility_df['IPONDI'].sum() if len(mobility_df) > 0 else 0
        
        # Calculer les pourcentages pour chaque type de transport
        transport_percentages = {}
        for transport_type, transport_values in transport_categories.items():
            transport_pop = mobility_df[mobility_df['TRANS'].isin(transport_values)]['IPONDI'].sum()
            transport_percentages[f'{transport_type}_percentage'] = (transport_pop / total_pop * 100).round(1) if total_pop > 0 else 0.0
        
        # Ajuster la population selon la tranche d'âge sélectionnée
        population_adjustment_factor = 1.0
        if age_filter:
            if age_filter in ['0-18', '19-35']:
                population_adjustment_factor = 0.28
            elif age_filter == '36-50':
                population_adjustment_factor = 0.32
            elif age_filter in ['51-65', '65+']:
                population_adjustment_factor = 0.22
        
        adjusted_population = int(commune_data.get('PTOT', 0) * population_adjustment_factor)
        
        # Calculer l'indice de mobilité verte
        velo_pct = transport_percentages.get('velo_percentage', 0.0)
        tc_pct = transport_percentages.get('transport_commun_percentage', 0.0)
        green_mobility_index = round(velo_pct + tc_pct * 0.8, 1)
        
        # Calculer le temps de trajet moyen
        base_avg_commute = stats.get('pourcentage_temps_moyen', 30)
        population_max = communes_df['PTOT'].max() if 'PTOT' in communes_df.columns and not communes_df.empty else 1
        population_factor = (adjusted_population / population_max) if population_max > 0 else 0
        avg_commute_time = round(base_avg_commute + (population_factor * 5), 1)
        
        # Construire la réponse
        result = {
            'commune': {
                'LIBGEO': commune_data.get('Commune', commune_data.get('LIBGEO', 'N/A')),
                'COM': commune_data.get('COM', commune_data.get('CODCOM', 'N/A')),
                'CODCOM': commune_data.get('CODCOM', commune_data.get('COM', 'N/A')),
                'PTOT': adjusted_population,
                'green_mobility_index': green_mobility_index,
                'avg_commute_time': avg_commute_time,
                **transport_percentages
            }
        }
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Erreur API détail commune: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@bp.route('/api/departments')
def api_departments():
    """
    API endpoint pour charger les départements d'une région
    """
    try:
        region_code = request.args.get('region', '')
        
        if not region_code:
            return jsonify({'departments': []})
        
        departments_list = data_loader.get_departments_by_region(region_code)
        
        return jsonify({'departments': departments_list})
    except Exception as e:
        logger.error(f"Erreur API départements: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@bp.route('/regions')
def regions():
    """
    Page affichant les indicateurs par région avec filtres et pagination
    Charge seulement les options de filtres, les données sont chargées via API
    """
    try:
        # Charger les options de filtres
        age_ranges_list = data_loader.get_age_ranges_from_data()
        
        # Récupérer les filtres actuels depuis l'URL
        age_filter = request.args.get('age', '')
        
        return render_template('mobilite/regions.html', 
                             age_ranges_list=age_ranges_list,
                             age_filter=age_filter)
    except Exception as e:
        logger.error(f"Erreur lors du chargement de la page regions: {e}", exc_info=True)
        return render_template('mobilite/regions.html', 
                             age_ranges_list=[],
                             age_filter='',
                             error=str(e))


@bp.route('/api/regions')
def api_regions():
    """
    API endpoint pour charger les régions avec pagination et filtres
    Calcule les pourcentages réels par type de transport pour chaque région
    """
    try:
        import pandas as pd
        
        # Récupérer les paramètres
        age_filter = request.args.get('age', '')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Charger les statistiques globales
        stats = get_cached_stats(main)
        
        # Charger les régions
        regions_df = data_loader.load_regions_data()
        
        if regions_df.empty:
            return jsonify({
                'regions': [],
                'total_count': 0,
                'total_pages': 0,
                'page': page,
                'per_page': per_page
            })
        
        # Charger les communes pour obtenir les codes communes par région
        communes_df = data_loader.load_communes_data()
        
        # Charger les données de mobilité
        mobility_df = data_loader.load_mobility_data()
        
        if mobility_df.empty:
            return jsonify({
                'regions': [],
                'total_count': 0,
                'total_pages': 0,
                'page': page,
                'per_page': per_page
            })
        
        # Extraire le code commune depuis la colonne COMMUNE
        mobility_df['COMMUNE_CODE'] = mobility_df['COMMUNE'].astype(str).str.extract(r'\((\d+)\)', expand=False)
        mobility_df['COMMUNE_CODE'] = mobility_df['COMMUNE_CODE'].astype(str).str.zfill(5)
        
        # Filtrer par tranche d'âge si spécifié
        if age_filter:
            age_values = data_loader.map_age_filter_to_agerevq_values(age_filter)
            if age_values:
                mobility_df = mobility_df[mobility_df['AGEREVQ'].isin(age_values)]
        
        # Créer un mapping région -> codes communes
        region_commune_map = {}
        if 'REG' in communes_df.columns:
            # Convertir REG en string pour le groupby
            communes_df = communes_df.copy()
            communes_df['REG_STR'] = communes_df['REG'].astype(str)
            
            # Obtenir les codes communes (COM ou CODCOM)
            if 'COM' in communes_df.columns:
                communes_df['COMMUNE_CODE'] = communes_df['COM'].astype(str).str.zfill(5)
            elif 'CODCOM' in communes_df.columns:
                communes_df['COMMUNE_CODE'] = communes_df['CODCOM'].astype(str).str.zfill(5)
            else:
                logger.warning("Aucune colonne COM ou CODCOM trouvée dans communes_df")
            
            if 'COMMUNE_CODE' in communes_df.columns:
                # Créer le mapping avec REG en string
                region_commune_map = communes_df.groupby('REG_STR')['COMMUNE_CODE'].apply(set).to_dict()
                logger.info(f"Mapping région->communes créé: {len(region_commune_map)} régions trouvées")
        
        # Définir les catégories de transport
        transport_categories = {
            'velo': ['Vélo (y compris à assistance électrique)'],
            'voiture': ['Voiture, camion, fourgonnette'],
            'transport_commun': ['Transports en commun'],
            'marche': ['Marche à pied (ou rollers, patinette)'],
            'deux_roues': ['Deux-roues motorisé'],
            'pas_transport': ['Pas de transport']
        }
        
        # Calculer les pourcentages par région
        regions_list = []
        for _, region_row in regions_df.iterrows():
            region_code = str(region_row.get('REG', ''))
            region_name = region_row.get('Région', 'N/A')
            
            # Obtenir les codes communes de cette région
            commune_codes = region_commune_map.get(region_code, set())
            
            if not commune_codes:
                # Logger pour déboguer
                logger.warning(f"Aucune commune trouvée pour la région {region_code} ({region_name}). Mapping disponible: {list(region_commune_map.keys())[:5] if region_commune_map else 'vide'}")
                # Si pas de communes, utiliser des valeurs par défaut
                transport_percentages = {f'{t}_percentage': 0.0 for t in transport_categories.keys()}
                total_pop = 0
            else:
                # Filtrer les données de mobilité pour cette région
                # Convertir commune_codes en liste pour éviter les problèmes de type
                commune_codes_list = list(commune_codes) if isinstance(commune_codes, set) else commune_codes
                region_mobility = mobility_df[mobility_df['COMMUNE_CODE'].isin(commune_codes_list)]
                
                # Logger pour déboguer
                if len(region_mobility) == 0 and len(commune_codes_list) > 0:
                    # Vérifier si les codes correspondent
                    sample_commune_codes = list(commune_codes_list)[:5]
                    sample_mobility_codes = mobility_df['COMMUNE_CODE'].unique()[:5].tolist() if len(mobility_df) > 0 else []
                    logger.warning(f"Région {region_code} ({region_name}): {len(commune_codes_list)} communes dans le mapping, mais 0 lignes trouvées dans mobility_df. Exemples codes communes: {sample_commune_codes}, Exemples codes mobility: {sample_mobility_codes}")
                
                # Calculer la population totale
                total_pop = region_mobility['IPONDI'].sum() if len(region_mobility) > 0 else 0
                
                # Calculer les pourcentages pour chaque type de transport
                transport_percentages = {}
                for transport_type, transport_values in transport_categories.items():
                    transport_pop = region_mobility[region_mobility['TRANS'].isin(transport_values)]['IPONDI'].sum()
                    transport_percentages[f'{transport_type}_percentage'] = (transport_pop / total_pop * 100).round(1) if total_pop > 0 else 0.0
            
            # Ajuster la population selon la tranche d'âge
            population_adjustment_factor = 1.0
            if age_filter:
                if age_filter in ['0-18', '19-35']:
                    population_adjustment_factor = 0.28
                elif age_filter == '36-50':
                    population_adjustment_factor = 0.32
                elif age_filter in ['51-65', '65+']:
                    population_adjustment_factor = 0.22
            
            adjusted_population = int(region_row.get('PTOT', 0) * population_adjustment_factor)
            
            # Calculer l'indice de mobilité verte
            velo_pct = transport_percentages.get('velo_percentage', 0.0)
            tc_pct = transport_percentages.get('transport_commun_percentage', 0.0)
            green_mobility_index = round(velo_pct + tc_pct * 0.8, 1)
            
            # Calculer le temps de trajet moyen
            base_avg_commute = stats.get('pourcentage_temps_moyen', 30)
            population_max = regions_df['PTOT'].max() if 'PTOT' in regions_df.columns and not regions_df.empty else 1
            population_factor = (adjusted_population / population_max) if population_max > 0 else 0
            avg_commute_time = round(base_avg_commute + (population_factor * 5), 1)
            
            regions_list.append({
                'REGION': region_name,
                'REG': region_code,
                'total_communes': int(region_row.get('NBCOM', 0)),
                'PTOT': adjusted_population,
                'green_mobility_index': green_mobility_index,
                'avg_commute_time': avg_commute_time,
                **transport_percentages
            })
        
        # Convertir en DataFrame pour la pagination
        regions_result_df = pd.DataFrame(regions_list)
        
        # Pagination
        total_count = len(regions_result_df)
        start = (page - 1) * per_page
        end = start + per_page
        regions_list_paginated = regions_result_df.iloc[start:end].to_dict('records')
        
        total_pages = (total_count + per_page - 1) // per_page if total_count > 0 else 1
        
        return jsonify({
            'regions': regions_list_paginated,
            'total_count': total_count,
            'total_pages': total_pages,
            'page': page,
            'per_page': per_page
        })
    except Exception as e:
        logger.error(f"Erreur API régions: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@bp.route('/api/regions/<code>')
def api_region_detail(code):
    """
    API endpoint pour charger les détails d'une région spécifique avec filtres
    """
    try:
        import pandas as pd
        
        # Récupérer les paramètres de filtres
        age_filter = request.args.get('age', '')
        
        # Charger les statistiques globales
        stats = get_cached_stats(main)
        
        # Charger les régions
        regions_df = data_loader.load_regions_data()
        
        if regions_df.empty:
            return jsonify({'error': 'Aucune donnée de région disponible'}), 404
        
        # Trouver la région par code
        region_data = None
        if 'REG' in regions_df.columns:
            region_match = regions_df[regions_df['REG'].astype(str) == str(code)]
            if not region_match.empty:
                region_data = region_match.iloc[0].to_dict()
        
        if region_data is None:
            return jsonify({'error': f'Région avec le code {code} non trouvée'}), 404
        
        # Charger les communes pour obtenir les codes communes de cette région
        communes_df = data_loader.load_communes_data()
        
        # Obtenir les codes communes de cette région
        region_code = str(region_data.get('REG', ''))
        commune_codes = set()
        if 'REG' in communes_df.columns and 'COM' in communes_df.columns:
            region_communes = communes_df[communes_df['REG'].astype(str) == region_code]
            commune_codes.update(region_communes['COM'].astype(str).str.zfill(5).tolist())
        
        # Charger les données de mobilité
        mobility_df = data_loader.load_mobility_data()
        
        if mobility_df.empty:
            return jsonify({'error': 'Aucune donnée de mobilité disponible'}), 404
        
        # Extraire le code commune depuis la colonne COMMUNE
        mobility_df['COMMUNE_CODE'] = mobility_df['COMMUNE'].astype(str).str.extract(r'\((\d+)\)', expand=False)
        mobility_df['COMMUNE_CODE'] = mobility_df['COMMUNE_CODE'].astype(str).str.zfill(5)
        
        # Filtrer par codes communes de la région
        if commune_codes:
            mobility_df = mobility_df[mobility_df['COMMUNE_CODE'].isin(commune_codes)]
        
        # Filtrer par tranche d'âge si spécifié
        if age_filter:
            age_values = data_loader.map_age_filter_to_agerevq_values(age_filter)
            if age_values:
                mobility_df = mobility_df[mobility_df['AGEREVQ'].isin(age_values)]
        
        # Calculer les pourcentages par type de transport
        transport_categories = {
            'velo': ['Vélo (y compris à assistance électrique)'],
            'voiture': ['Voiture, camion, fourgonnette'],
            'transport_commun': ['Transports en commun'],
            'marche': ['Marche à pied (ou rollers, patinette)'],
            'deux_roues': ['Deux-roues motorisé'],
            'pas_transport': ['Pas de transport']
        }
        
        # Calculer la population totale
        total_pop = mobility_df['IPONDI'].sum() if len(mobility_df) > 0 else 0
        
        # Calculer les pourcentages pour chaque type de transport
        transport_percentages = {}
        for transport_type, transport_values in transport_categories.items():
            transport_pop = mobility_df[mobility_df['TRANS'].isin(transport_values)]['IPONDI'].sum()
            transport_percentages[f'{transport_type}_percentage'] = (transport_pop / total_pop * 100).round(1) if total_pop > 0 else 0.0
        
        # Ajuster la population selon la tranche d'âge
        population_adjustment_factor = 1.0
        if age_filter:
            if age_filter in ['0-18', '19-35']:
                population_adjustment_factor = 0.28
            elif age_filter == '36-50':
                population_adjustment_factor = 0.32
            elif age_filter in ['51-65', '65+']:
                population_adjustment_factor = 0.22
        
        adjusted_population = int(region_data.get('PTOT', 0) * population_adjustment_factor)
        
        # Calculer l'indice de mobilité verte
        velo_pct = transport_percentages.get('velo_percentage', 0.0)
        tc_pct = transport_percentages.get('transport_commun_percentage', 0.0)
        green_mobility_index = round(velo_pct + tc_pct * 0.8, 1)
        
        # Calculer le temps de trajet moyen
        base_avg_commute = stats.get('pourcentage_temps_moyen', 30)
        population_max = regions_df['PTOT'].max() if 'PTOT' in regions_df.columns and not regions_df.empty else 1
        population_factor = (adjusted_population / population_max) if population_max > 0 else 0
        avg_commute_time = round(base_avg_commute + (population_factor * 5), 1)
        
        # Construire la réponse
        result = {
            'region': {
                'REGION': region_data.get('Région', 'N/A'),
                'REG': region_data.get('REG', 'N/A'),
                'total_communes': int(region_data.get('NBCOM', 0)),
                'PTOT': adjusted_population,
                'green_mobility_index': green_mobility_index,
                'avg_commute_time': avg_commute_time,
                **transport_percentages
            }
        }
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Erreur API détail région: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500



