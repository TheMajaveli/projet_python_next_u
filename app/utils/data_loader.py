"""
Chargeur de données pour les comparaisons
"""

import pandas as pd
import os
import logging
from pathlib import Path
from functools import lru_cache
import hashlib

logger = logging.getLogger(__name__)

# Cache global pour les données
_data_cache = {}
_cache_timestamps = {}


class DataLoader:
    """Charge les données depuis les fichiers CSV"""
    
    def __init__(self, base_path: str = None):
        if base_path is None:
            # Trouver le répertoire racine du projet
            current_file = os.path.abspath(__file__)
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
        self.base_path = Path(base_path)
    
    def load_communes_data(self, use_cache=True) -> pd.DataFrame:
        """Charge les données des communes avec cache"""
        cache_key = 'communes_data'
        
        # Vérifier le cache
        if use_cache and cache_key in _data_cache:
            cached_data, cached_timestamp = _data_cache[cache_key], _cache_timestamps.get(cache_key, 0)
            # Vérifier si le fichier a été modifié
            paths = [
                self.base_path / 'ensemble' / 'donnees_communes.csv',
                self.base_path / 'data' / 'raw' / 'demographic' / 'donnees_communes.csv',
            ]
            
            file_modified = False
            for path in paths:
                if path.exists():
                    file_mtime = path.stat().st_mtime
                    if file_mtime > cached_timestamp:
                        file_modified = True
                        break
            
            if not file_modified:
                logger.debug(f"Utilisation du cache pour les données communes ({len(cached_data)} lignes)")
                return cached_data.copy()
        
        try:
            # Essayer plusieurs chemins possibles
            paths = [
                self.base_path / 'ensemble' / 'donnees_communes.csv',
                self.base_path / 'data' / 'raw' / 'demographic' / 'donnees_communes.csv',
            ]
            
            for path in paths:
                if path.exists():
                    # Les fichiers CSV utilisent des points-virgules comme séparateurs
                    df = pd.read_csv(path, sep=';', encoding='utf-8')
                    logger.info(f"Données communes chargées depuis {path}: {len(df)} lignes, colonnes: {list(df.columns)}")
                    
                    # Mettre en cache
                    if use_cache:
                        _data_cache[cache_key] = df.copy()
                        _cache_timestamps[cache_key] = path.stat().st_mtime
                    
                    return df
            
            logger.warning("Aucun fichier de données communes trouvé")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Erreur lors du chargement des données communes: {e}")
            return pd.DataFrame()
    
    def load_regions_data(self) -> pd.DataFrame:
        """Charge les données des régions"""
        try:
            paths = [
                self.base_path / 'ensemble' / 'donnees_regions.csv',
                self.base_path / 'data' / 'raw' / 'demographic' / 'donnees_regions.csv',
            ]
            
            for path in paths:
                if path.exists():
                    # Les fichiers CSV utilisent des points-virgules comme séparateurs
                    df = pd.read_csv(path, sep=';', encoding='utf-8')
                    logger.info(f"Données régions chargées depuis {path}: {len(df)} lignes, colonnes: {list(df.columns)}")
                    return df
            
            logger.warning("Aucun fichier de données régions trouvé")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Erreur lors du chargement des données régions: {e}")
            return pd.DataFrame()
    
    def get_top_communes(self, n: int = 10, sort_by: str = 'green_mobility_index') -> pd.DataFrame:
        """
        Retourne les top N communes selon un indicateur
        
        Args:
            n: Nombre de communes à retourner
            sort_by: Colonne pour trier (par défaut: green_mobility_index)
        """
        df = self.load_communes_data()
        if df.empty:
            return pd.DataFrame()
        
        # Si la colonne de tri n'existe pas, utiliser une colonne par défaut
        if sort_by not in df.columns:
            # Essayer d'autres colonnes possibles
            possible_cols = ['PTOT', 'population', 'avg_commute_time', 'bike_usage_rate']
            for col in possible_cols:
                if col in df.columns:
                    sort_by = col
                    break
            else:
                # Si aucune colonne trouvée, retourner les premières lignes
                return df.head(n)
        
        # Trier et retourner les top N
        return df.nlargest(n, sort_by)
    
    def get_top_regions(self, n: int = 5, sort_by: str = 'green_mobility_index') -> pd.DataFrame:
        """
        Retourne les top N régions selon un indicateur
        
        Args:
            n: Nombre de régions à retourner
            sort_by: Colonne pour trier (par défaut: green_mobility_index)
        """
        df = self.load_regions_data()
        if df.empty:
            return pd.DataFrame()
        
        # Si la colonne de tri n'existe pas, utiliser une colonne par défaut
        if sort_by not in df.columns:
            possible_cols = ['total_communes', 'population', 'avg_commute_time', 'bike_usage_rate']
            for col in possible_cols:
                if col in df.columns:
                    sort_by = col
                    break
            else:
                return df.head(n)
        
        # Trier et retourner les top N
        return df.nlargest(n, sort_by)
    
    def get_regions_list(self) -> list:
        """Retourne la liste des régions pour les filtres"""
        try:
            df = self.load_regions_data()
            if df.empty:
                return []
            
            # Extraire les régions uniques avec code et nom
            if 'REG' in df.columns and 'Région' in df.columns:
                regions = df[['REG', 'Région']].drop_duplicates().sort_values('Région')
                return regions.to_dict('records')
            elif 'REG' in df.columns and 'REGION' in df.columns:
                regions = df[['REG', 'REGION']].drop_duplicates().sort_values('REGION')
                return [{'REG': r['REG'], 'Région': r['REGION']} for r in regions.to_dict('records')]
            return []
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des régions: {e}")
            return []
    
    def load_departments_data(self) -> pd.DataFrame:
        """Charge les données des départements"""
        try:
            paths = [
                self.base_path / 'ensemble' / 'donnees_departements.csv',
                self.base_path / 'data' / 'raw' / 'demographic' / 'donnees_departements.csv',
            ]
            
            for path in paths:
                if path.exists():
                    df = pd.read_csv(path, sep=';', encoding='utf-8')
                    logger.info(f"Données départements chargées depuis {path}: {len(df)} lignes, colonnes: {list(df.columns)}")
                    return df
            
            logger.warning("Aucun fichier de données départements trouvé")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Erreur lors du chargement des données départements: {e}")
            return pd.DataFrame()
    
    def get_departments_by_region(self, region_code: str = None) -> list:
        """Retourne la liste des départements pour une région spécifique"""
        try:
            dept_df = self.load_departments_data()
            
            if dept_df.empty:
                return []
            
            # Filtrer par région si spécifiée
            if region_code and 'REG' in dept_df.columns:
                dept_df = dept_df[dept_df['REG'].astype(str) == str(region_code)]
            
            if 'DEP' in dept_df.columns and 'Département' in dept_df.columns:
                depts = dept_df[['DEP', 'Département']].drop_duplicates().sort_values('DEP')
                result = []
                for d in depts.to_dict('records'):
                    dep_code = str(d['DEP']).strip()
                    if len(dep_code) == 1:
                        dep_code = dep_code.zfill(2)
                    elif dep_code == '2A' or dep_code == '2B':
                        dep_code = dep_code
                    result.append({
                        'DEP': dep_code,
                        'Nom': str(d['Département']).strip()
                    })
                return result
            
            return []
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des départements par région: {e}")
            return []
    
    def get_departments_list(self) -> list:
        """Retourne la liste des départements pour les filtres avec noms"""
        try:
            # Charger depuis le fichier dédié
            dept_df = self.load_departments_data()
            
            if not dept_df.empty:
                # Le fichier a les colonnes DEP et Département
                if 'DEP' in dept_df.columns and 'Département' in dept_df.columns:
                    depts = dept_df[['DEP', 'Département']].drop_duplicates().sort_values('DEP')
                    result = []
                    for d in depts.to_dict('records'):
                        dep_code = str(d['DEP']).strip()
                        # Formater le code : 01, 02, etc. (sauf pour 2A, 2B, 971, 972, etc.)
                        if len(dep_code) == 1:
                            dep_code = dep_code.zfill(2)
                        elif dep_code == '2A' or dep_code == '2B':
                            dep_code = dep_code  # Garder tel quel pour la Corse
                        result.append({
                            'DEP': dep_code,
                            'Nom': str(d['Département']).strip()
                        })
                    return result
            
            # Fallback: utiliser les données communes et créer un mapping manuel
            communes_df = self.load_communes_data()
            if communes_df.empty:
                return []
            
            # Mapping des codes départements vers noms (France métropolitaine + DOM)
            dept_names = {
                '01': 'Ain', '02': 'Aisne', '03': 'Allier', '04': 'Alpes-de-Haute-Provence',
                '05': 'Hautes-Alpes', '06': 'Alpes-Maritimes', '07': 'Ardèche', '08': 'Ardennes',
                '09': 'Ariège', '10': 'Aube', '11': 'Aude', '12': 'Aveyron',
                '13': 'Bouches-du-Rhône', '14': 'Calvados', '15': 'Cantal', '16': 'Charente',
                '17': 'Charente-Maritime', '18': 'Cher', '19': 'Corrèze', '21': "Côte-d'Or",
                '22': "Côtes-d'Armor", '23': 'Creuse', '24': 'Dordogne', '25': 'Doubs',
                '26': 'Drôme', '27': 'Eure', '28': 'Eure-et-Loir', '29': 'Finistère',
                '2A': 'Corse-du-Sud', '2B': 'Haute-Corse', '30': 'Gard', '31': 'Haute-Garonne',
                '32': 'Gers', '33': 'Gironde', '34': 'Hérault', '35': 'Ille-et-Vilaine',
                '36': 'Indre', '37': 'Indre-et-Loire', '38': 'Isère', '39': 'Jura',
                '40': 'Landes', '41': 'Loir-et-Cher', '42': 'Loire', '43': 'Haute-Loire',
                '44': 'Loire-Atlantique', '45': 'Loiret', '46': 'Lot', '47': 'Lot-et-Garonne',
                '48': 'Lozère', '49': 'Maine-et-Loire', '50': 'Manche', '51': 'Marne',
                '52': 'Haute-Marne', '53': 'Mayenne', '54': 'Meurthe-et-Moselle', '55': 'Meuse',
                '56': 'Morbihan', '57': 'Moselle', '58': 'Nièvre', '59': 'Nord',
                '60': 'Oise', '61': 'Orne', '62': 'Pas-de-Calais', '63': 'Puy-de-Dôme',
                '64': 'Pyrénées-Atlantiques', '65': 'Hautes-Pyrénées', '66': 'Pyrénées-Orientales',
                '67': 'Bas-Rhin', '68': 'Haut-Rhin', '69': 'Rhône', '70': 'Haute-Saône',
                '71': 'Saône-et-Loire', '72': 'Sarthe', '73': 'Savoie', '74': 'Haute-Savoie',
                '75': 'Paris', '76': 'Seine-Maritime', '77': 'Seine-et-Marne', '78': 'Yvelines',
                '79': 'Deux-Sèvres', '80': 'Somme', '81': 'Tarn', '82': 'Tarn-et-Garonne',
                '83': 'Var', '84': 'Vaucluse', '85': 'Vendée', '86': 'Vienne',
                '87': 'Haute-Vienne', '88': 'Vosges', '89': 'Yonne', '90': 'Territoire de Belfort',
                '91': 'Essonne', '92': 'Hauts-de-Seine', '93': 'Seine-Saint-Denis', '94': 'Val-de-Marne',
                '95': "Val-d'Oise", '971': 'Guadeloupe', '972': 'Martinique', '973': 'Guyane',
                '974': 'La Réunion', '976': 'Mayotte'
            }
            
            if 'DEP' in communes_df.columns:
                depts = communes_df[['DEP']].drop_duplicates().sort_values('DEP')
                result = []
                for d in depts.to_dict('records'):
                    dep_code = str(d['DEP']).zfill(2) if len(str(d['DEP'])) < 3 else str(d['DEP'])
                    dep_name = dept_names.get(dep_code, dep_code)
                    result.append({'DEP': dep_code, 'Nom': dep_name})
                return result
            
            return []
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des départements: {e}")
            return []
    
    def get_age_ranges_from_data(self) -> list:
        """
        Extrait les tranches d'âge réelles du fichier de mobilité
        et les mappe vers les catégories du dropdown
        """
        try:
            # Charger seulement la colonne AGEREVQ pour économiser la mémoire
            paths = [
                self.base_path / 'data' / 'RP2021_mobpro' / 'Commune_1001-13101_2.csv',
                self.base_path / 'data' / 'RP2021_mobpro' / 'Commune_1001-13101.csv',
            ]
            
            for path in paths:
                if path.exists():
                    # Charger seulement AGEREVQ pour économiser la mémoire
                    df = pd.read_csv(path, usecols=['AGEREVQ'], nrows=10000)  # Échantillon pour identifier les valeurs
                    
                    # Extraire les valeurs uniques
                    age_ranges = df['AGEREVQ'].dropna().unique()
                    
                    # Mapper vers les catégories du dropdown
                    age_mapping = {
                        '0-18': [],
                        '19-35': [],
                        '36-50': [],
                        '51-65': [],
                        '65+': []
                    }
                    
                    import re
                    for age_range in age_ranges:
                        age_str = str(age_range).strip()
                        # Extraire les nombres (ex: "25 à 29 ans" -> [25, 29])
                        numbers = re.findall(r'\d+', age_str)
                        
                        if numbers:
                            min_age = int(numbers[0])
                            
                            # Mapper vers les catégories
                            if min_age < 19:
                                age_mapping['0-18'].append(age_str)
                            elif min_age < 36:
                                age_mapping['19-35'].append(age_str)
                            elif min_age < 51:
                                age_mapping['36-50'].append(age_str)
                            elif min_age < 66:
                                age_mapping['51-65'].append(age_str)
                            else:
                                age_mapping['65+'].append(age_str)
                    
                    # Retourner la liste des catégories avec leurs valeurs réelles
                    result = []
                    for category, values in age_mapping.items():
                        if values:
                            # Trier les valeurs par âge
                            sorted_values = sorted(set(values), key=lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else 0)
                            result.append({
                                'code': category,
                                'name': f"{category} ans",
                                'values': sorted_values  # Valeurs réelles dans les données
                            })
                    
                    return result
            
            # Si pas de fichier trouvé, retourner les catégories par défaut
            return [
                {'code': '0-18', 'name': '0-18 ans', 'values': []},
                {'code': '19-35', 'name': '19-35 ans', 'values': []},
                {'code': '36-50', 'name': '36-50 ans', 'values': []},
                {'code': '51-65', 'name': '51-65 ans', 'values': []},
                {'code': '65+', 'name': '65+ ans', 'values': []},
            ]
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction des tranches d'âge: {e}")
            return []
    
    def map_age_filter_to_agerevq_values(self, age_filter: str) -> list:
        """
        Mappe un filtre d'âge (ex: '19-35') vers les valeurs AGEREVQ réelles
        dans les données (ex: ['19 à 24 ans', '25 à 29 ans', '30 à 34 ans'])
        """
        if not age_filter:
            return []
        
        try:
            # Charger un échantillon pour identifier les valeurs
            paths = [
                self.base_path / 'data' / 'RP2021_mobpro' / 'Commune_1001-13101_2.csv',
                self.base_path / 'data' / 'RP2021_mobpro' / 'Commune_1001-13101.csv',
            ]
            
            for path in paths:
                if path.exists():
                    df = pd.read_csv(path, usecols=['AGEREVQ'], nrows=50000)  # Échantillon plus large
                    age_ranges = df['AGEREVQ'].dropna().unique()
                    
                    import re
                    result = []
                    
                    for age_range in age_ranges:
                        age_str = str(age_range).strip()
                        numbers = re.findall(r'\d+', age_str)
                        
                        if numbers:
                            min_age = int(numbers[0])
                            
                            # Vérifier si cette tranche correspond au filtre
                            if age_filter == '0-18' and min_age < 19:
                                result.append(age_str)
                            elif age_filter == '19-35' and 19 <= min_age < 36:
                                result.append(age_str)
                            elif age_filter == '36-50' and 36 <= min_age < 51:
                                result.append(age_str)
                            elif age_filter == '51-65' and 51 <= min_age < 66:
                                result.append(age_str)
                            elif age_filter == '65+' and min_age >= 65:
                                result.append(age_str)
                    
                    return sorted(set(result), key=lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else 0)
            
            return []
        except Exception as e:
            logger.error(f"Erreur lors du mapping des tranches d'âge: {e}")
            return []
    
    def get_transport_types_from_data(self) -> list:
        """
        Extrait les types de transport réels du fichier CSV
        et les mappe vers les catégories du dropdown
        """
        try:
            # Charger seulement la colonne TRANS pour économiser la mémoire
            paths = [
                self.base_path / 'data' / 'RP2021_mobpro' / 'Commune_1001-13101_2.csv',
                self.base_path / 'data' / 'RP2021_mobpro' / 'Commune_1001-13101.csv',
            ]
            
            for path in paths:
                if path.exists():
                    # Charger seulement TRANS pour économiser la mémoire
                    df = pd.read_csv(path, usecols=['TRANS'], nrows=10000)  # Échantillon
                    
                    # Extraire les valeurs uniques
                    transport_types = df['TRANS'].dropna().unique()
                    
                    # Mapper vers les catégories du dropdown
                    transport_mapping = {
                        'velo': [],
                        'voiture': [],
                        'transport_commun': [],
                        'marche': [],
                        'deux_roues': [],
                        'pas_transport': []
                    }
                    
                    for transport in transport_types:
                        transport_str = str(transport).strip()
                        
                        # Mapper vers les catégories
                        if 'Vélo' in transport_str or 'vélo' in transport_str:
                            transport_mapping['velo'].append(transport_str)
                        elif 'Voiture' in transport_str or 'camion' in transport_str or 'fourgonnette' in transport_str:
                            transport_mapping['voiture'].append(transport_str)
                        elif 'Transports en commun' in transport_str or 'transport' in transport_str.lower():
                            transport_mapping['transport_commun'].append(transport_str)
                        elif 'Marche' in transport_str or 'marche' in transport_str or 'rollers' in transport_str or 'patinette' in transport_str:
                            transport_mapping['marche'].append(transport_str)
                        elif 'Deux-roues' in transport_str or 'deux-roues' in transport_str:
                            transport_mapping['deux_roues'].append(transport_str)
                        elif 'Pas de transport' in transport_str or 'pas de transport' in transport_str:
                            transport_mapping['pas_transport'].append(transport_str)
                    
                    # Retourner la liste des catégories avec leurs valeurs réelles
                    result = []
                    category_names = {
                        'velo': 'Vélo',
                        'voiture': 'Voiture',
                        'transport_commun': 'Transports en commun',
                        'marche': 'Marche à pied',
                        'deux_roues': 'Deux-roues motorisé',
                        'pas_transport': 'Pas de transport'
                    }
                    
                    for category, values in transport_mapping.items():
                        if values:
                            result.append({
                                'code': category,
                                'name': category_names.get(category, category),
                                'values': sorted(set(values))  # Valeurs réelles dans les données
                            })
                    
                    return result
            
            # Si pas de fichier trouvé, retourner les catégories par défaut
            return [
                {'code': 'velo', 'name': 'Vélo', 'values': []},
                {'code': 'voiture', 'name': 'Voiture', 'values': []},
                {'code': 'transport_commun', 'name': 'Transports en commun', 'values': []},
                {'code': 'marche', 'name': 'Marche à pied', 'values': []},
                {'code': 'deux_roues', 'name': 'Deux-roues motorisé', 'values': []},
            ]
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction des types de transport: {e}")
            return []
    
    def map_transport_filter_to_trans_values(self, transport_filter: str) -> list:
        """
        Mappe un filtre de transport (ex: 'velo', 'transport_commun') vers les valeurs TRANS réelles
        dans les données (ex: ['Vélo (y compris à assistance électrique)'])
        """
        if not transport_filter:
            return []
        
        try:
            # Charger un échantillon pour identifier les valeurs
            paths = [
                self.base_path / 'data' / 'RP2021_mobpro' / 'Commune_1001-13101_2.csv',
                self.base_path / 'data' / 'RP2021_mobpro' / 'Commune_1001-13101.csv',
            ]
            
            for path in paths:
                if path.exists():
                    df = pd.read_csv(path, usecols=['TRANS'], nrows=50000)  # Échantillon plus large
                    transport_types = df['TRANS'].dropna().unique()
                    
                    result = []
                    
                    for transport in transport_types:
                        transport_str = str(transport).strip()
                        
                        # Vérifier si ce transport correspond au filtre
                        if transport_filter == 'velo':
                            if 'Vélo' in transport_str or 'vélo' in transport_str:
                                result.append(transport_str)
                        elif transport_filter == 'voiture':
                            if 'Voiture' in transport_str or 'camion' in transport_str or 'fourgonnette' in transport_str:
                                result.append(transport_str)
                        elif transport_filter in ['transport_commun', 'bus', 'train', 'metro', 'tram']:
                            # Tous les transports en commun
                            if 'Transports en commun' in transport_str or 'transport' in transport_str.lower():
                                result.append(transport_str)
                        elif transport_filter == 'marche':
                            if 'Marche' in transport_str or 'marche' in transport_str or 'rollers' in transport_str or 'patinette' in transport_str:
                                result.append(transport_str)
                        elif transport_filter == 'deux_roues':
                            if 'Deux-roues' in transport_str or 'deux-roues' in transport_str:
                                result.append(transport_str)
                        elif transport_filter == 'pas_transport':
                            if 'Pas de transport' in transport_str or 'pas de transport' in transport_str:
                                result.append(transport_str)
                    
                    return sorted(set(result))
            
            return []
        except Exception as e:
            logger.error(f"Erreur lors du mapping des types de transport: {e}")
            return []
    
    def load_mobility_data(self, use_cache=True) -> pd.DataFrame:
        """
        Charge les données de mobilité depuis le fichier CSV avec cache
        Retourne un DataFrame avec les colonnes: COMMUNE, TRANS, AGEREVQ, IPONDI, etc.
        """
        cache_key = 'mobility_data'
        
        # Vérifier le cache
        if use_cache and cache_key in _data_cache:
            cached_data, cached_timestamp = _data_cache[cache_key], _cache_timestamps.get(cache_key, 0)
            # Vérifier si le fichier a été modifié
            paths = [
                self.base_path / 'data' / 'RP2021_mobpro' / 'Commune_1001-13101_2.csv',
                self.base_path / 'data' / 'RP2021_mobpro' / 'Commune_1001-13101.csv',
            ]
            
            file_modified = False
            for path in paths:
                if path.exists():
                    file_mtime = path.stat().st_mtime
                    if file_mtime > cached_timestamp:
                        file_modified = True
                        break
            
            if not file_modified:
                logger.debug(f"Utilisation du cache pour les données de mobilité ({len(cached_data)} lignes)")
                return cached_data.copy()
        
        try:
            paths = [
                self.base_path / 'data' / 'RP2021_mobpro' / 'Commune_1001-13101_2.csv',
                self.base_path / 'data' / 'RP2021_mobpro' / 'Commune_1001-13101.csv',
            ]
            
            for path in paths:
                if path.exists():
                    logger.info(f"Chargement des données de mobilité depuis {path}")
                    # Charger seulement les colonnes nécessaires pour économiser la mémoire
                    df = pd.read_csv(path, usecols=['COMMUNE', 'TRANS', 'AGEREVQ', 'IPONDI'])
                    logger.info(f"Données de mobilité chargées: {len(df)} lignes")
                    
                    # Mettre en cache
                    if use_cache:
                        _data_cache[cache_key] = df.copy()
                        _cache_timestamps[cache_key] = path.stat().st_mtime
                        logger.info(f"Données de mobilité mises en cache")
                    
                    return df
            
            logger.warning("Aucun fichier de données de mobilité trouvé")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Erreur lors du chargement des données de mobilité: {e}", exc_info=True)
            return pd.DataFrame()

