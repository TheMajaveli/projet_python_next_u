"""
Routes pour les visualisations (cartes, graphiques)
"""

from flask import Blueprint, render_template_string, Response, request
import logging
import base64
from app.utils.data_loader import DataLoader
from app.visualizations.maps import (
    create_communes_map,
    create_green_mobility_map
)
from app.visualizations.charts import (
    create_histogram,
    create_bar_chart
)
from script import main

logger = logging.getLogger(__name__)

bp = Blueprint('visualizations', __name__, url_prefix='/visualizations')
data_loader = DataLoader()


@bp.route('/map/communes')
def map_communes():
    """
    Génère une carte Folium des communes et retourne le HTML
    Supporte les filtres: region, department, age
    """
    try:
        from app.routes.export import prepare_communes_data
        
        # Récupérer les filtres
        region_filter = request.args.get('region', '')
        department_filter = request.args.get('department', '')
        age_filter = request.args.get('age', '')
        
        # Préparer les données avec les mêmes calculs que l'export
        communes_df = prepare_communes_data(region_filter, department_filter, age_filter)
        
        if communes_df.empty:
            return "<p>Aucune donnée disponible</p>", 404
        
        # Créer la carte
        m = create_communes_map(communes_df, show_legend=True)
        
        # Retourner le HTML de la carte
        return m._repr_html_()
    except Exception as e:
        logger.error(f"Erreur lors de la génération de la carte: {e}", exc_info=True)
        return f"<p>Erreur: {str(e)}</p>", 500


@bp.route('/map/zones-mal-desservies')
def map_underserved():
    """
    Génère une carte avec les zones mal desservies
    """
    try:
        from app.routes.export import prepare_communes_data
        
        # Récupérer les filtres
        region_filter = request.args.get('region', '')
        department_filter = request.args.get('department', '')
        age_filter = request.args.get('age', '')
        
        communes_df = prepare_communes_data(region_filter, department_filter, age_filter)
        
        if communes_df.empty:
            return "<p>Aucune donnée disponible</p>", 404
        
        # Identifier les zones mal desservies (mobilité verte faible et pas de transport élevé)
        if 'green_mobility_index' in communes_df.columns and 'pas_transport_percentage' in communes_df.columns:
            # Seuil: mobilité verte < 20% OU pas de transport > 15%
            communes_df['is_underserved'] = (
                (communes_df['green_mobility_index'] < 20) | 
                (communes_df['pas_transport_percentage'] > 15)
            )
        else:
            communes_df['is_underserved'] = False
        
        # Créer la carte
        m = create_communes_map(communes_df, show_legend=True)
        
        # Ajouter des marqueurs spéciaux pour les zones mal desservies
        if 'is_underserved' in communes_df.columns:
            import folium
            from app.visualizations.maps import get_commune_coordinates
            
            underserved = communes_df[communes_df['is_underserved'] == True]
            
            # Identifier les colonnes
            commune_col = None
            name_col = None
            for col in ['COM', 'CODCOM']:
                if col in communes_df.columns:
                    commune_col = col
                    break
            for col in ['Commune', 'LIBGEO']:
                if col in communes_df.columns:
                    name_col = col
                    break
            
            for idx, row in underserved.iterrows():
                commune_code = str(row.get(commune_col, '')).zfill(5) if commune_col else ''
                commune_name = str(row.get(name_col, '')) if name_col else commune_code
                lat, lon = get_commune_coordinates(commune_code, commune_name)
                
                if lat and lon:
                    folium.CircleMarker(
                        location=[lat, lon],
                        radius=10,
                        popup=folium.Popup(f"<b>{commune_name}</b><br>Zone mal desservie", max_width=200),
                        tooltip=f"{commune_name} - Zone mal desservie",
                        color='red',
                        fill=True,
                        fillColor='red',
                        fillOpacity=0.5,
                        weight=3
                    ).add_to(m)
        
        return m._repr_html_()
    except Exception as e:
        logger.error(f"Erreur lors de la génération de la carte: {e}", exc_info=True)
        return f"<p>Erreur: {str(e)}</p>", 500


@bp.route('/map/green-mobility')
def map_green_mobility():
    """
    Génère une carte de mobilité verte
    """
    try:
        from app.routes.export import prepare_communes_data
        
        # Récupérer les filtres
        region_filter = request.args.get('region', '')
        department_filter = request.args.get('department', '')
        age_filter = request.args.get('age', '')
        
        communes_df = prepare_communes_data(region_filter, department_filter, age_filter)
        
        if communes_df.empty:
            return "<p>Aucune donnée disponible</p>", 404
        
        # Créer la carte
        m = create_green_mobility_map(communes_df)
        
        return m._repr_html_()
    except Exception as e:
        logger.error(f"Erreur lors de la génération de la carte: {e}", exc_info=True)
        return f"<p>Erreur: {str(e)}</p>", 500


@bp.route('/chart/histogram/travel-time')
def chart_histogram_travel_time():
    """
    Génère un histogramme de la distribution du temps de trajet
    Les données proviennent de Commune_1001-13101_2.csv via load_mobility_data()
    """
    try:
        from app.routes.export import prepare_communes_data
        
        # Récupérer les filtres
        region_filter = request.args.get('region', '')
        department_filter = request.args.get('department', '')
        age_filter = request.args.get('age', '')
        
        # prepare_communes_data() utilise load_mobility_data() qui charge Commune_1001-13101_2.csv
        communes_df = prepare_communes_data(region_filter, department_filter, age_filter)
        
        if communes_df.empty or 'avg_commute_time' not in communes_df.columns:
            return "<p>Données non disponibles</p>", 404
        
        # Générer l'histogramme en base64
        img_base64 = create_histogram(
            communes_df, 
            'avg_commute_time',
            title="Distribution du Temps de Trajet Domicile-Travail",
            xlabel="Temps (minutes)",
            ylabel="Nombre de communes",
            bins=30,
            return_base64=True
        )
        
        if img_base64:
            html = f'<img src="data:image/png;base64,{img_base64}" alt="Histogramme Temps de Trajet" style="width: 100%;" />'
            return html
        else:
            return "<p>Erreur lors de la génération du graphique</p>", 500
    except Exception as e:
        logger.error(f"Erreur lors de la génération de l'histogramme: {e}", exc_info=True)
        return f"<p>Erreur: {str(e)}</p>", 500


@bp.route('/chart/histogram/bike-usage')
def chart_histogram_bike_usage():
    """
    Génère un histogramme de la distribution du taux d'utilisation du vélo
    Les données proviennent de Commune_1001-13101_2.csv via load_mobility_data()
    """
    try:
        from app.routes.export import prepare_communes_data
        
        # Récupérer les filtres
        region_filter = request.args.get('region', '')
        department_filter = request.args.get('department', '')
        age_filter = request.args.get('age', '')
        
        communes_df = prepare_communes_data(region_filter, department_filter, age_filter)
        
        if communes_df.empty or 'velo_percentage' not in communes_df.columns:
            return "<p>Données non disponibles</p>", 404
        
        # Générer l'histogramme en base64
        img_base64 = create_histogram(
            communes_df, 
            'velo_percentage',
            title="Distribution du Taux d'Utilisation du Vélo",
            xlabel="Taux (%)",
            ylabel="Nombre de communes",
            bins=30,
            return_base64=True
        )
        
        if img_base64:
            html = f'<img src="data:image/png;base64,{img_base64}" alt="Histogramme Taux Vélo" style="width: 100%;" />'
            return html
        else:
            return "<p>Erreur lors de la génération du graphique</p>", 500
    except Exception as e:
        logger.error(f"Erreur lors de la génération de l'histogramme: {e}", exc_info=True)
        return f"<p>Erreur: {str(e)}</p>", 500


@bp.route('/chart/histogram/public-transport')
def chart_histogram_public_transport():
    """
    Génère un histogramme de la distribution du taux d'utilisation des transports en commun
    Les données proviennent de Commune_1001-13101_2.csv via load_mobility_data()
    """
    try:
        from app.routes.export import prepare_communes_data
        
        # Récupérer les filtres
        region_filter = request.args.get('region', '')
        department_filter = request.args.get('department', '')
        age_filter = request.args.get('age', '')
        
        communes_df = prepare_communes_data(region_filter, department_filter, age_filter)
        
        if communes_df.empty or 'transport_commun_percentage' not in communes_df.columns:
            return "<p>Données non disponibles</p>", 404
        
        # Générer l'histogramme en base64
        img_base64 = create_histogram(
            communes_df, 
            'transport_commun_percentage',
            title="Distribution du Taux d'Utilisation des Transports en Commun",
            xlabel="Taux (%)",
            ylabel="Nombre de communes",
            bins=30,
            return_base64=True
        )
        
        if img_base64:
            html = f'<img src="data:image/png;base64,{img_base64}" alt="Histogramme TC" style="width: 100%;" />'
            return html
        else:
            return "<p>Erreur lors de la génération du graphique</p>", 500
    except Exception as e:
        logger.error(f"Erreur lors de la génération de l'histogramme: {e}", exc_info=True)
        return f"<p>Erreur: {str(e)}</p>", 500


@bp.route('/chart/bar/green-mobility-by-region')
def chart_bar_green_mobility_by_region():
    """
    Génère un bar chart de la mobilité verte par région
    Les données proviennent de Commune_1001-13101_2.csv via load_mobility_data()
    """
    try:
        from app.routes.export import prepare_regions_data
        
        # Récupérer les filtres
        age_filter = request.args.get('age', '')
        
        regions_df = prepare_regions_data(age_filter)
        
        if regions_df.empty or 'green_mobility_index' not in regions_df.columns or 'Région' not in regions_df.columns:
            return "<p>Données non disponibles</p>", 404
        
        # Générer le bar chart en base64
        img_base64 = create_bar_chart(
            regions_df,
            'Région',
            'green_mobility_index',
            title="Indicateur de Mobilité Verte par Région",
            xlabel="Région",
            ylabel="Indicateur de Mobilité Verte",
            horizontal=True,
            return_base64=True
        )
        
        if img_base64:
            html = f'<img src="data:image/png;base64,{img_base64}" alt="Bar chart Mobilité Verte par Région" style="width: 100%;" />'
            return html
        else:
            return "<p>Erreur lors de la génération du graphique</p>", 500
    except Exception as e:
        logger.error(f"Erreur lors de la génération du bar chart: {e}", exc_info=True)
        return f"<p>Erreur: {str(e)}</p>", 500


@bp.route('/chart/bar/travel-time-by-region')
def chart_bar_travel_time_by_region():
    """
    Génère un bar chart du temps de trajet moyen par région
    Les données proviennent de Commune_1001-13101_2.csv via load_mobility_data()
    """
    try:
        from app.routes.export import prepare_regions_data
        
        # Récupérer les filtres
        age_filter = request.args.get('age', '')
        
        regions_df = prepare_regions_data(age_filter)
        
        if regions_df.empty or 'avg_commute_time' not in regions_df.columns or 'Région' not in regions_df.columns:
            return "<p>Données non disponibles</p>", 404
        
        # Générer le bar chart en base64
        img_base64 = create_bar_chart(
            regions_df,
            'Région',
            'avg_commute_time',
            title="Temps de Trajet Moyen par Région",
            xlabel="Région",
            ylabel="Temps (minutes)",
            horizontal=True,
            return_base64=True
        )
        
        if img_base64:
            html = f'<img src="data:image/png;base64,{img_base64}" alt="Bar chart Temps Trajet par Région" style="width: 100%;" />'
            return html
        else:
            return "<p>Erreur lors de la génération du graphique</p>", 500
    except Exception as e:
        logger.error(f"Erreur lors de la génération du bar chart: {e}", exc_info=True)
        return f"<p>Erreur: {str(e)}</p>", 500

