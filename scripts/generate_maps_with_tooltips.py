"""
Script pour régénérer les cartes statiques avec tooltips
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire racine au path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

import pandas as pd
import folium
from app.utils.data_loader import DataLoader
from app.visualizations.maps import get_commune_coordinates, create_communes_map

def generate_map_communes():
    """Génère la carte des communes avec tooltips"""
    print("Génération de la carte des communes...")
    
    data_loader = DataLoader()
    communes_df = data_loader.load_communes_data()
    
    if communes_df.empty:
        print("Aucune donnée de commune disponible")
        return
    
    # Créer COMMUNE_CODE si nécessaire
    if 'COMMUNE_CODE' not in communes_df.columns:
        if 'COM' in communes_df.columns:
            communes_df['COMMUNE_CODE'] = communes_df['COM'].astype(str).str.zfill(5)
        elif 'CODCOM' in communes_df.columns:
            communes_df['COMMUNE_CODE'] = communes_df['CODCOM'].astype(str).str.zfill(5)
    
    # Limiter le nombre de communes pour la performance (échantillon)
    max_communes = 200
    if len(communes_df) > max_communes:
        communes_df = communes_df.sample(n=max_communes)
        print(f"Échantillonnage: {max_communes} communes sur {len(data_loader.load_communes_data())}")
    
    # Créer la carte
    m = folium.Map(
        location=[46.2276, 2.2137],
        zoom_start=6,
        tiles='OpenStreetMap'
    )
    
    # Identifier les colonnes
    commune_col = 'COMMUNE_CODE' if 'COMMUNE_CODE' in communes_df.columns else None
    if not commune_col:
        for col in ['COM', 'CODCOM']:
            if col in communes_df.columns:
                commune_col = col
                break
    
    name_col = None
    for col in ['Commune', 'LIBGEO']:
        if col in communes_df.columns:
            name_col = col
            break
    
    if not commune_col:
        print("Colonne commune non trouvée")
        return
    
    # Ajouter les marqueurs avec tooltips
    added = 0
    for idx, row in communes_df.iterrows():
        try:
            commune_code = str(row[commune_col]).zfill(5) if pd.notna(row.get(commune_col)) else None
            if not commune_code or commune_code == '00000':
                continue
            
            commune_name = str(row[name_col]) if name_col and pd.notna(row.get(name_col)) else commune_code
            
            lat, lon = get_commune_coordinates(commune_code, commune_name)
            
            if lat and lon:
                # Créer le tooltip
                tooltip_text = f"<b>{commune_name}</b>"
                if 'PTOT' in row and pd.notna(row.get('PTOT')):
                    tooltip_text += f"<br>Population: {int(row['PTOT']):,}"
                
                # Créer le popup avec plus d'infos
                popup_html = f"""
                <div style="min-width: 200px;">
                    <h6 style="margin: 0 0 10px 0; font-weight: bold;">{commune_name}</h6>
                    <p style="margin: 5px 0;"><strong>Code:</strong> {commune_code}</p>
                """
                if 'PTOT' in row and pd.notna(row.get('PTOT')):
                    popup_html += f'<p style="margin: 5px 0;"><strong>Population:</strong> {int(row["PTOT"]):,}</p>'
                popup_html += '</div>'
                
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=6,
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=folium.Tooltip(tooltip_text, permanent=False),
                    color='blue',
                    fill=True,
                    fillColor='blue',
                    fillOpacity=0.7,
                    weight=2
                ).add_to(m)
                added += 1
        except Exception as e:
            print(f"Erreur pour la ligne {idx}: {e}")
            continue
    
    # Sauvegarder
    output_path = root_dir / 'static' / 'map_communes.html'
    m.save(str(output_path))
    print(f"Carte des communes générée: {added} marqueurs -> {output_path}")


def generate_map_zones_mal_desservies():
    """Génère la carte des zones mal desservies avec tooltips"""
    print("Génération de la carte des zones mal desservies...")
    
    data_loader = DataLoader()
    communes_df = data_loader.load_communes_data()
    
    if communes_df.empty:
        print("Aucune donnée de commune disponible")
        return
    
    # Créer COMMUNE_CODE si nécessaire
    if 'COMMUNE_CODE' not in communes_df.columns:
        if 'COM' in communes_df.columns:
            communes_df['COMMUNE_CODE'] = communes_df['COM'].astype(str).str.zfill(5)
        elif 'CODCOM' in communes_df.columns:
            communes_df['COMMUNE_CODE'] = communes_df['CODCOM'].astype(str).str.zfill(5)
    
    # Simuler des zones mal desservies (exemple: communes avec population < 1000)
    if 'PTOT' in communes_df.columns:
        communes_df['is_underserved'] = communes_df['PTOT'] < 1000
    else:
        communes_df['is_underserved'] = False
    
    # Limiter le nombre
    underserved = communes_df[communes_df['is_underserved'] == True]
    if len(underserved) > 100:
        underserved = underserved.sample(n=100)
    
    # Créer la carte
    m = folium.Map(
        location=[46.2276, 2.2137],
        zoom_start=6,
        tiles='OpenStreetMap'
    )
    
    # Identifier les colonnes
    commune_col = 'COMMUNE_CODE' if 'COMMUNE_CODE' in communes_df.columns else None
    if not commune_col:
        for col in ['COM', 'CODCOM']:
            if col in communes_df.columns:
                commune_col = col
                break
    
    name_col = None
    for col in ['Commune', 'LIBGEO']:
        if col in communes_df.columns:
            name_col = col
            break
    
    # Ajouter les marqueurs
    added = 0
    for idx, row in underserved.iterrows():
        try:
            commune_code = str(row[commune_col]).zfill(5) if pd.notna(row.get(commune_col)) else None
            if not commune_code or commune_code == '00000':
                continue
            
            commune_name = str(row[name_col]) if name_col and pd.notna(row.get(name_col)) else commune_code
            lat, lon = get_commune_coordinates(commune_code, commune_name)
            
            if lat and lon:
                tooltip_text = f"<b>{commune_name}</b><br>Zone mal desservie"
                if 'PTOT' in row and pd.notna(row.get('PTOT')):
                    tooltip_text += f"<br>Population: {int(row['PTOT']):,}"
                
                popup_html = f"<b>{commune_name}</b><br>Zone mal desservie"
                if 'PTOT' in row and pd.notna(row.get('PTOT')):
                    popup_html += f"<br>Population: {int(row['PTOT']):,}"
                
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=10,
                    popup=folium.Popup(popup_html, max_width=200),
                    tooltip=folium.Tooltip(tooltip_text, permanent=False),
                    color='red',
                    fill=True,
                    fillColor='red',
                    fillOpacity=0.5,
                    weight=3
                ).addTo(m)
                added += 1
        except Exception as e:
            print(f"Erreur pour la ligne {idx}: {e}")
            continue
    
    # Sauvegarder
    output_path = root_dir / 'static' / 'map_zones_mal_desservies.html'
    m.save(str(output_path))
    print(f"Carte des zones mal desservies générée: {added} marqueurs -> {output_path}")


def generate_map_mobilite_verte():
    """Génère la carte de mobilité verte avec tooltips"""
    print("Génération de la carte de mobilité verte...")
    
    data_loader = DataLoader()
    communes_df = data_loader.load_communes_data()
    
    if communes_df.empty:
        print("Aucune donnée de commune disponible")
        return
    
    # Créer COMMUNE_CODE si nécessaire
    if 'COMMUNE_CODE' not in communes_df.columns:
        if 'COM' in communes_df.columns:
            communes_df['COMMUNE_CODE'] = communes_df['COM'].astype(str).str.zfill(5)
        elif 'CODCOM' in communes_df.columns:
            communes_df['COMMUNE_CODE'] = communes_df['CODCOM'].astype(str).str.zfill(5)
    
    # Simuler un indice de mobilité verte (exemple basé sur la population)
    if 'PTOT' in communes_df.columns:
        max_pop = communes_df['PTOT'].max()
        communes_df['green_mobility_index'] = (communes_df['PTOT'] / max_pop * 100).round(1)
    else:
        communes_df['green_mobility_index'] = 50.0
    
    # Limiter le nombre
    max_communes = 200
    if len(communes_df) > max_communes:
        communes_df = communes_df.sample(n=max_communes)
    
    # Créer la carte
    m = folium.Map(
        location=[46.2276, 2.2137],
        zoom_start=6,
        tiles='OpenStreetMap'
    )
    
    # Identifier les colonnes
    commune_col = 'COMMUNE_CODE' if 'COMMUNE_CODE' in communes_df.columns else None
    if not commune_col:
        for col in ['COM', 'CODCOM']:
            if col in communes_df.columns:
                commune_col = col
                break
    
    name_col = None
    for col in ['Commune', 'LIBGEO']:
        if col in communes_df.columns:
            name_col = col
            break
    
    # Calculer min/max pour les couleurs
    green_values = communes_df['green_mobility_index'].dropna()
    if len(green_values) > 0:
        min_green = float(green_values.min())
        max_green = float(green_values.max())
    else:
        min_green, max_green = 0, 100
    
    def get_color(value):
        if pd.isna(value):
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
    added = 0
    for idx, row in communes_df.iterrows():
        try:
            commune_code = str(row[commune_col]).zfill(5) if pd.notna(row.get(commune_col)) else None
            if not commune_code or commune_code == '00000':
                continue
            
            commune_name = str(row[name_col]) if name_col and pd.notna(row.get(name_col)) else commune_code
            lat, lon = get_commune_coordinates(commune_code, commune_name)
            
            if lat and lon:
                green_index = row.get('green_mobility_index', 0)
                color = get_color(green_index)
                
                tooltip_text = f"<b>{commune_name}</b>"
                if pd.notna(green_index):
                    tooltip_text += f"<br>Mobilité Verte: {green_index:.1f}%"
                
                popup_html = f"""
                <div style="min-width: 200px;">
                    <h6 style="margin: 0 0 10px 0; font-weight: bold;">{commune_name}</h6>
                    <p style="margin: 5px 0;"><strong>Code:</strong> {commune_code}</p>
                """
                if 'PTOT' in row and pd.notna(row.get('PTOT')):
                    popup_html += f'<p style="margin: 5px 0;"><strong>Population:</strong> {int(row["PTOT"]):,}</p>'
                if pd.notna(green_index):
                    popup_html += f'<p style="margin: 5px 0;"><strong>Mobilité Verte:</strong> {green_index:.1f}%</p>'
                popup_html += '</div>'
                
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=6,
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=folium.Tooltip(tooltip_text, permanent=False),
                    color=color,
                    fill=True,
                    fillColor=color,
                    fillOpacity=0.7,
                    weight=2
                ).add_to(m)
                added += 1
        except Exception as e:
            print(f"Erreur pour la ligne {idx}: {e}")
            continue
    
    # Ajouter une légende
    legend_html = f'''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 220px; height: 140px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.3);">
    <p style="margin: 0 0 10px 0; font-weight: bold; font-size: 16px;">Légende</p>
    <p style="margin: 5px 0;"><span style="color:green; font-size: 20px;">●</span> Mobilité Verte Élevée ({max_green:.1f}%)</p>
    <p style="margin: 5px 0;"><span style="color:orange; font-size: 20px;">●</span> Mobilité Verte Moyenne</p>
    <p style="margin: 5px 0;"><span style="color:red; font-size: 20px;">●</span> Mobilité Verte Faible ({min_green:.1f}%)</p>
    <p style="margin: 10px 0 0 0; font-size: 12px; color: #666;">Survolez un marqueur pour plus d'infos</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Sauvegarder
    output_path = root_dir / 'static' / 'map_mobilite_verte.html'
    m.save(str(output_path))
    print(f"Carte de mobilité verte générée: {added} marqueurs -> {output_path}")


if __name__ == '__main__':
    print("Génération des cartes avec tooltips...")
    print("=" * 50)
    
    try:
        generate_map_communes()
        print()
        generate_map_zones_mal_desservies()
        print()
        generate_map_mobilite_verte()
        print()
        print("=" * 50)
        print("✅ Toutes les cartes ont été générées avec succès!")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()





