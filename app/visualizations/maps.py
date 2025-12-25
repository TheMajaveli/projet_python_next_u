"""
Module de création de cartes interactives avec Folium
"""

import folium
import pandas as pd
import numpy as np
import logging
from typing import Optional, Dict, Any
from pathlib import Path
import requests
import json

logger = logging.getLogger(__name__)


def get_commune_coordinates(commune_code: str, commune_name: str = None) -> tuple:
    """
    Récupère les coordonnées GPS d'une commune.
    Utilise l'API GéoAPI de l'INSEE ou un cache local.
    
    Args:
        commune_code: Code INSEE de la commune (5 chiffres)
        commune_name: Nom de la commune (optionnel, pour améliorer la recherche)
    
    Returns:
        Tuple (latitude, longitude) ou (None, None) si non trouvé
    """
    try:
        # Essayer d'abord avec l'API GéoAPI de l'INSEE
        # Format: https://geo.api.gouv.fr/communes/{code}
        url = f"https://geo.api.gouv.fr/communes/{commune_code}"
        params = {
            'fields': 'nom,code,codesPostaux,centre',
            'format': 'json',
            'geometry': 'centre'
        }
        
        try:
            response = requests.get(url, params=params, timeout=2)
            if response.status_code == 200:
                data = response.json()
                if 'centre' in data and 'coordinates' in data['centre']:
                    # L'API retourne [longitude, latitude]
                    lon, lat = data['centre']['coordinates']
                    return (float(lat), float(lon))
        except Exception as e:
            logger.debug(f"Erreur API GéoAPI pour {commune_code}: {e}")
        
        # Si l'API échoue, utiliser une position par défaut basée sur le département
        # Extraire le département du code commune (2 premiers chiffres)
        if len(commune_code) >= 2:
            dept_code = commune_code[:2]
            # Coordonnées approximatives par département (centres régionaux)
            dept_coords = {
                '01': (46.2043, 5.2265),  # Ain
                '02': (49.4431, 3.4110),  # Aisne
                '03': (46.3448, 3.4285),  # Allier
                '04': (44.0925, 6.2350),  # Alpes-de-Haute-Provence
                '05': (44.5586, 6.0794),  # Hautes-Alpes
                '06': (43.7102, 7.2620),  # Alpes-Maritimes
                '07': (44.9333, 4.3833),  # Ardèche
                '08': (49.7733, 4.7194),  # Ardennes
                '09': (42.9389, 1.6072),  # Ariège
                '10': (48.2978, 4.0783),  # Aube
                '11': (43.2131, 2.3517),  # Aude
                '12': (44.3500, 2.5667),  # Aveyron
                '13': (43.2965, 5.3698),  # Bouches-du-Rhône
                '14': (49.1829, -0.3707), # Calvados
                '15': (45.0469, 2.4406),  # Cantal
                '16': (45.6500, 0.1500),  # Charente
                '17': (45.6333, -0.6333), # Charente-Maritime
                '18': (47.0833, 2.4000),  # Cher
                '19': (45.2667, 1.7667),  # Corrèze
                '21': (47.3220, 5.0415),  # Côte-d'Or
                '22': (48.4500, -2.7500), # Côtes-d'Armor
                '23': (46.1667, 1.8667),  # Creuse
                '24': (45.1833, 0.7167),  # Dordogne
                '25': (47.2378, 6.0244),  # Doubs
                '26': (44.9333, 4.8833),  # Drôme
                '27': (49.0833, 1.1500),  # Eure
                '28': (48.4333, 1.4833),  # Eure-et-Loir
                '29': (48.3833, -4.4833), # Finistère
                '30': (44.1333, 4.0833),  # Gard
                '31': (43.6047, 1.4442),  # Haute-Garonne
                '32': (43.6500, 0.5833),  # Gers
                '33': (44.8378, -0.5792), # Gironde
                '34': (43.6109, 3.8767),  # Hérault
                '35': (48.1147, -1.6794), # Ille-et-Vilaine
                '36': (46.8167, 1.6833),  # Indre
                '37': (47.3833, 0.6833),  # Indre-et-Loire
                '38': (45.1885, 5.7245),  # Isère
                '39': (46.6667, 5.5500),  # Jura
                '40': (43.8833, -1.3833), # Landes
                '41': (47.5833, 1.3333),  # Loir-et-Cher
                '42': (45.4333, 4.3833),  # Loire
                '43': (45.0333, 3.8833),  # Haute-Loire
                '44': (47.2167, -1.5500), # Loire-Atlantique
                '45': (47.9000, 1.9000),  # Loiret
                '46': (44.4500, 1.4333),  # Lot
                '47': (44.2000, 0.6167),  # Lot-et-Garonne
                '48': (44.5167, 3.5000),  # Lozère
                '49': (47.4667, -0.5500), # Maine-et-Loire
                '50': (49.1167, -1.0833), # Manche
                '51': (49.2500, 4.0333),  # Marne
                '52': (48.1167, 5.1333),  # Haute-Marne
                '53': (48.0667, -0.7667), # Mayenne
                '54': (48.6833, 6.1833),  # Meurthe-et-Moselle
                '55': (49.1167, 5.3833),  # Meuse
                '56': (47.7500, -3.3667), # Morbihan
                '57': (49.1167, 6.1833),  # Moselle
                '58': (47.0000, 3.1500),  # Nièvre
                '59': (50.6333, 3.0667),  # Nord
                '60': (49.4333, 2.0833),  # Oise
                '61': (48.4333, 0.0833),  # Orne
                '62': (50.2833, 2.7833),  # Pas-de-Calais
                '63': (45.7833, 3.0833),  # Puy-de-Dôme
                '64': (43.3000, -0.3667), # Pyrénées-Atlantiques
                '65': (43.2333, 0.0667),  # Hautes-Pyrénées
                '66': (42.7000, 2.8833),  # Pyrénées-Orientales
                '67': (48.5833, 7.7500),  # Bas-Rhin
                '68': (47.7500, 7.3333),  # Haut-Rhin
                '69': (45.7500, 4.8500),  # Rhône
                '70': (47.6167, 6.1667),  # Haute-Saône
                '71': (46.7833, 4.8500),  # Saône-et-Loire
                '72': (48.0000, 0.2000),  # Sarthe
                '73': (45.5667, 5.9167),  # Savoie
                '74': (46.2000, 6.1667),  # Haute-Savoie
                '75': (48.8566, 2.3522),  # Paris
                '76': (49.4333, 1.0833),  # Seine-Maritime
                '77': (48.5667, 2.6667),  # Seine-et-Marne
                '78': (48.8000, 2.1333),  # Yvelines
                '79': (46.3167, -0.4667), # Deux-Sèvres
                '80': (49.9000, 2.3000),  # Somme
                '81': (43.6000, 2.2333),  # Tarn
                '82': (44.0167, 1.3500),  # Tarn-et-Garonne
                '83': (43.1167, 6.0833),  # Var
                '84': (44.0500, 5.0500),  # Vaucluse
                '85': (46.6667, -1.4333), # Vendée
                '86': (46.5833, 0.3333),  # Vienne
                '87': (45.8333, 1.2500),  # Haute-Vienne
                '88': (48.1667, 6.4500),  # Vosges
                '89': (47.8000, 3.5667),  # Yonne
                '90': (47.6333, 6.8667),  # Territoire de Belfort
                '91': (48.6333, 2.3333),  # Essonne
                '92': (48.9000, 2.2500),  # Hauts-de-Seine
                '93': (48.9333, 2.3833),  # Seine-Saint-Denis
                '94': (48.7833, 2.4667),  # Val-de-Marne
                '95': (49.0833, 2.2500),  # Val-d'Oise
                '971': (16.2530, -61.5348), # Guadeloupe
                '972': (14.6415, -61.0242), # Martinique
                '973': (3.9339, -53.1258),  # Guyane
                '974': (-21.1151, 55.5364), # La Réunion
                '976': (-12.8275, 45.1662), # Mayotte
            }
            
            if dept_code in dept_coords:
                return dept_coords[dept_code]
        
        # Position par défaut (centre de la France)
        logger.warning(f"Coordonnées non trouvées pour commune {commune_code}, utilisation position par défaut")
        return (46.2276, 2.2137)  # Centre approximatif de la France
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des coordonnées pour {commune_code}: {e}")
        return (46.2276, 2.2137)


def create_communes_map(
    communes_df: pd.DataFrame,
    output_path: Optional[str] = None,
    center_lat: float = 46.2276,
    center_lon: float = 2.2137,
    zoom_start: int = 6,
    show_legend: bool = True
) -> folium.Map:
    """
    Crée une carte Folium affichant la localisation des communes avec leurs indicateurs.
    
    Args:
        communes_df: DataFrame avec les données des communes (doit contenir COM/CODCOM, Commune/LIBGEO, PTOT, green_mobility_index, etc.)
        output_path: Chemin pour sauvegarder la carte HTML (optionnel)
        center_lat: Latitude du centre de la carte
        center_lon: Longitude du centre de la carte
        zoom_start: Niveau de zoom initial
        show_legend: Afficher la légende
    
    Returns:
        Objet folium.Map
    """
    # Créer la carte
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom_start,
        tiles='OpenStreetMap'
    )
    
    if communes_df.empty:
        logger.warning("DataFrame vide, création d'une carte vide")
        return m
    
    # Identifier les colonnes nécessaires
    commune_col = None
    name_col = None
    
    # Chercher d'abord COMMUNE_CODE (créé par prepare_communes_data)
    if 'COMMUNE_CODE' in communes_df.columns:
        commune_col = 'COMMUNE_CODE'
    else:
        # Sinon chercher les autres colonnes possibles
        for col in ['COM', 'CODCOM', 'CODGEO']:
            if col in communes_df.columns:
                commune_col = col
                break
    
    # Chercher la colonne de nom
    for col in ['Commune', 'LIBGEO', 'COM_NOM']:
        if col in communes_df.columns:
            name_col = col
            break
    
    if commune_col is None:
        logger.warning(f"Colonne commune non trouvée. Colonnes disponibles: {list(communes_df.columns)}")
        return m
    
    # Limiter le nombre de marqueurs pour la performance
    max_markers = 500
    if len(communes_df) > max_markers:
        df_sample = communes_df.sample(n=max_markers)
        logger.info(f"Échantillonnage: {max_markers} communes sur {len(communes_df)}")
    else:
        df_sample = communes_df
    
    # Calculer les valeurs min/max pour la couleur
    has_green_mobility = 'green_mobility_index' in df_sample.columns
    min_green = 0
    max_green = 100
    if has_green_mobility:
        green_values = df_sample['green_mobility_index'].dropna()
        if len(green_values) > 0:
            min_green = float(green_values.min())
            max_green = float(green_values.max())
        else:
            has_green_mobility = False
    
    # Fonction pour obtenir la couleur selon la mobilité verte
    def get_color(value):
        if not has_green_mobility or pd.isna(value):
            return 'blue'
        if max_green == min_green:
            return 'green'
        normalized = (value - min_green) / (max_green - min_green)
        if normalized < 0.33:
            return 'red'
        elif normalized < 0.66:
            return 'orange'
        else:
            return 'green'
    
    # Ajouter les marqueurs
    added_count = 0
    for idx, row in df_sample.iterrows():
        try:
            # Récupérer le code commune
            commune_code_raw = row.get(commune_col)
            if pd.isna(commune_code_raw) or commune_code_raw == '':
                logger.debug(f"Code commune vide pour la ligne {idx}")
                continue
            
            commune_code = str(commune_code_raw).strip().zfill(5)
            if commune_code == '00000' or len(commune_code) != 5:
                logger.debug(f"Code commune invalide: {commune_code}")
                continue
            
            commune_name = str(row[name_col]) if name_col and pd.notna(row.get(name_col)) else commune_code
            
            # Obtenir les coordonnées
            lat, lon = get_commune_coordinates(commune_code, commune_name)
            
            if lat and lon:
                # Créer le popup avec tooltip
                popup_html = f"""
                <div style="min-width: 200px;">
                    <h6 style="margin: 0 0 10px 0; font-weight: bold;">{commune_name}</h6>
                    <p style="margin: 5px 0;"><strong>Code:</strong> {commune_code}</p>
                """
                
                if 'PTOT' in row and pd.notna(row.get('PTOT')):
                    popup_html += f'<p style="margin: 5px 0;"><strong>Population:</strong> {int(row["PTOT"]):,}</p>'
                
                if has_green_mobility and pd.notna(row.get('green_mobility_index')):
                    popup_html += f'<p style="margin: 5px 0;"><strong>Mobilité Verte:</strong> {row["green_mobility_index"]:.1f}%</p>'
                
                if 'avg_commute_time' in row and pd.notna(row.get('avg_commute_time')):
                    popup_html += f'<p style="margin: 5px 0;"><strong>Temps Trajet:</strong> {row["avg_commute_time"]:.1f} min</p>'
                
                # Ajouter les pourcentages de transport
                transport_cols = ['velo_percentage', 'voiture_percentage', 'transport_commun_percentage', 
                                'marche_percentage', 'deux_roues_percentage', 'pas_transport_percentage']
                transport_labels = {
                    'velo_percentage': 'Vélo',
                    'voiture_percentage': 'Voiture',
                    'transport_commun_percentage': 'TC',
                    'marche_percentage': 'Marche',
                    'deux_roues_percentage': '2-roues',
                    'pas_transport_percentage': 'Sans transport'
                }
                
                popup_html += '<hr style="margin: 10px 0;"><p style="margin: 5px 0; font-weight: bold;">Transport:</p>'
                for col in transport_cols:
                    if col in row and pd.notna(row.get(col)):
                        popup_html += f'<p style="margin: 3px 0;">{transport_labels.get(col, col)}: {row[col]:.1f}%</p>'
                
                popup_html += '</div>'
                
                # Obtenir la couleur
                color = get_color(row.get('green_mobility_index') if has_green_mobility else None)
                
                # Créer le marqueur avec tooltip
                tooltip_text = f"{commune_name}"
                if has_green_mobility and pd.notna(row.get('green_mobility_index')):
                    tooltip_text += f" - Mobilité: {row['green_mobility_index']:.1f}%"
                
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=6,
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=tooltip_text,
                    color=color,
                    fill=True,
                    fillColor=color,
                    fillOpacity=0.7,
                    weight=2
                ).add_to(m)
                added_count += 1
        except Exception as e:
            logger.debug(f"Erreur lors de l'ajout du marqueur pour la ligne {idx}: {e}")
            continue
    
    logger.info(f"Carte créée avec {added_count} marqueurs sur {len(df_sample)} lignes")
    
    # Ajouter une légende si demandé
    if show_legend and has_green_mobility:
        legend_html = f'''
        <div style="position: fixed; 
                    bottom: 50px; left: 50px; width: 220px; height: 140px; 
                    background-color: white; border:2px solid grey; z-index:9999; 
                    font-size:14px; padding: 10px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.3);">
        <p style="margin: 0 0 10px 0; font-weight: bold; font-size: 16px;">Légende</p>
        <p style="margin: 5px 0;"><span style="color:green; font-size: 20px;">●</span> Mobilité Verte Élevée ({max_green:.1f}%)</p>
        <p style="margin: 5px 0;"><span style="color:orange; font-size: 20px;">●</span> Mobilité Verte Moyenne</p>
        <p style="margin: 5px 0;"><span style="color:red; font-size: 20px;">●</span> Mobilité Verte Faible ({min_green:.1f}%)</p>
        <p style="margin: 10px 0 0 0; font-size: 12px; color: #666;">Cliquez sur un marqueur pour plus d'infos</p>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))
    
    # Sauvegarder si demandé
    if output_path:
        m.save(output_path)
        logger.info(f"Carte sauvegardée: {output_path}")
    
    return m


def create_green_mobility_map(
    communes_df: pd.DataFrame,
    output_path: Optional[str] = None,
    center_lat: float = 46.2276,
    center_lon: float = 2.2137,
    zoom_start: int = 6
) -> folium.Map:
    """
    Crée une carte colorée selon l'indicateur de mobilité verte.
    """
    return create_communes_map(
        communes_df,
        output_path=output_path,
        center_lat=center_lat,
        center_lon=center_lon,
        zoom_start=zoom_start,
        show_legend=True
    )

