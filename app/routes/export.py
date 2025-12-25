"""
Routes pour l'export des données (CSV et PDF)
"""

from flask import Blueprint, send_file, request, jsonify
import pandas as pd
import io
import logging
from app.utils.data_loader import DataLoader
from app.utils.cache import get_cached_stats
from script import main
from datetime import datetime

logger = logging.getLogger(__name__)

# Import reportlab avec gestion d'erreur
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    logger.warning("reportlab n'est pas installé. Les exports PDF ne seront pas disponibles.")

bp = Blueprint('export', __name__, url_prefix='/export')
data_loader = DataLoader()


def prepare_communes_data(region_filter='', department_filter='', age_filter=''):
    """Prépare les données des communes avec indicateurs et filtres"""
    try:
        import re
        import pandas as pd
        
        # Charger les statistiques globales (avec cache)
        stats = get_cached_stats(main)
        
        # Charger les communes
        communes_df = data_loader.load_communes_data()
        
        if communes_df.empty:
            return pd.DataFrame()
        
        # Appliquer les filtres géographiques
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
        
        # Créer COMMUNE_CODE dès maintenant pour qu'il soit toujours disponible
        if 'COMMUNE_CODE' not in communes_df.columns:
            if 'COM' in communes_df.columns:
                communes_df['COMMUNE_CODE'] = communes_df['COM'].astype(str).str.zfill(5)
            elif 'CODCOM' in communes_df.columns:
                communes_df['COMMUNE_CODE'] = communes_df['CODCOM'].astype(str).str.zfill(5)
        
        # Charger les données de mobilité
        mobility_df = data_loader.load_mobility_data()
        
        if mobility_df.empty:
            # Si pas de données de mobilité, retourner avec valeurs par défaut mais garder COMMUNE_CODE
            cols_to_return = []
            if 'Commune' in communes_df.columns:
                cols_to_return.append('Commune')
            if 'PTOT' in communes_df.columns:
                cols_to_return.append('PTOT')
            if 'COMMUNE_CODE' in communes_df.columns:
                cols_to_return.append('COMMUNE_CODE')
            if 'LIBGEO' in communes_df.columns:
                cols_to_return.append('LIBGEO')
            return communes_df[cols_to_return].copy() if cols_to_return else pd.DataFrame()
        
        # Extraire le code commune depuis la colonne COMMUNE
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
            
            # Calculer les pourcentages avec protection contre division par zéro
            for transport_type in transport_categories.keys():
                pop_col = f'{transport_type}_pop'
                if pop_col in result_df.columns:
                    # Utiliser replace(0, 1) pour éviter division par zéro, puis remplacer les résultats invalides
                    result_df[f'{transport_type}_percentage'] = (
                        (result_df[pop_col] / result_df['total_pop'].replace(0, pd.NA) * 100)
                        .fillna(0)
                        .round(1)
                    )
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
        
        # Calculer les indicateurs généraux
        if len(communes_df) > 0:
            communes_df = communes_df.copy()
            
            # Ajuster la population selon la tranche d'âge
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
            
            # Calculer l'indice de mobilité verte
            velo_pct = communes_df['velo_percentage'] if 'velo_percentage' in communes_df.columns else pd.Series([0.0] * len(communes_df), index=communes_df.index)
            tc_pct = communes_df['transport_commun_percentage'] if 'transport_commun_percentage' in communes_df.columns else pd.Series([0.0] * len(communes_df), index=communes_df.index)
            communes_df['green_mobility_index'] = (velo_pct + tc_pct * 0.8).round(1)
            
            # Calculer le temps de trajet moyen
            base_avg_commute = stats.get('pourcentage_temps_moyen', 30)
            population_max = communes_df['PTOT'].max() if 'PTOT' in communes_df.columns else 1
            population_factor = (communes_df['PTOT'] / population_max) if population_max > 0 else 0
            communes_df['avg_commute_time'] = (base_avg_commute + (population_factor * 5)).round(1)
        
        # S'assurer que toutes les colonnes de transport sont présentes
        transport_cols = ['velo_percentage', 'voiture_percentage', 'transport_commun_percentage', 
                          'marche_percentage', 'deux_roues_percentage', 'pas_transport_percentage']
        for col in transport_cols:
            if col not in communes_df.columns:
                communes_df[col] = 0.0
        
        # Sélectionner les colonnes nécessaires
        base_cols = ['Commune', 'PTOT', 'green_mobility_index', 'avg_commute_time']
        # Ajouter les colonnes de code commune pour les cartes
        code_cols = []
        if 'COMMUNE_CODE' in communes_df.columns:
            code_cols.append('COMMUNE_CODE')
        if 'COM' in communes_df.columns:
            code_cols.append('COM')
        if 'CODCOM' in communes_df.columns:
            code_cols.append('CODCOM')
        if 'LIBGEO' in communes_df.columns:
            code_cols.append('LIBGEO')
        
        display_cols = base_cols + transport_cols + code_cols
        available_cols = [col for col in display_cols if col in communes_df.columns]
        return communes_df[available_cols].copy()
    except Exception as e:
        logger.error(f"Erreur lors de la préparation des données communes: {e}", exc_info=True)
        return pd.DataFrame()


def prepare_regions_data(age_filter=''):
    """Prépare les données des régions avec indicateurs et filtres"""
    try:
        import pandas as pd
        
        # Charger les statistiques globales (avec cache)
        stats = get_cached_stats(main)
        
        # Charger les régions
        regions_df = data_loader.load_regions_data()
        
        if regions_df.empty:
            return pd.DataFrame()
        
        # Charger les communes pour obtenir les codes communes par région
        communes_df = data_loader.load_communes_data()
        
        # Charger les données de mobilité
        mobility_df = data_loader.load_mobility_data()
        
        if mobility_df.empty:
            return pd.DataFrame()
        
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
            communes_df_copy = communes_df.copy()
            communes_df_copy['REG_STR'] = communes_df_copy['REG'].astype(str)
            
            if 'COM' in communes_df_copy.columns:
                communes_df_copy['COMMUNE_CODE'] = communes_df_copy['COM'].astype(str).str.zfill(5)
            elif 'CODCOM' in communes_df_copy.columns:
                communes_df_copy['COMMUNE_CODE'] = communes_df_copy['CODCOM'].astype(str).str.zfill(5)
            
            if 'COMMUNE_CODE' in communes_df_copy.columns:
                region_commune_map = communes_df_copy.groupby('REG_STR')['COMMUNE_CODE'].apply(set).to_dict()
        
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
                transport_percentages = {f'{t}_percentage': 0.0 for t in transport_categories.keys()}
                total_pop = 0
            else:
                # Filtrer les données de mobilité pour cette région
                commune_codes_list = list(commune_codes) if isinstance(commune_codes, set) else commune_codes
                region_mobility = mobility_df[mobility_df['COMMUNE_CODE'].isin(commune_codes_list)]
                
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
                'Région': region_name,
                'REG': region_code,
                'NBCOM': int(region_row.get('NBCOM', 0)),
                'PTOT': adjusted_population,
                'green_mobility_index': green_mobility_index,
                'avg_commute_time': avg_commute_time,
                **transport_percentages
            })
        
        # Convertir en DataFrame
        return pd.DataFrame(regions_list)
    except Exception as e:
        logger.error(f"Erreur lors de la préparation des données régions: {e}", exc_info=True)
        return pd.DataFrame()


@bp.route('/csv/communes')
def export_csv_communes():
    """Export des données communes en CSV avec filtres"""
    try:
        # Récupérer les filtres depuis les paramètres URL
        region_filter = request.args.get('region', '')
        department_filter = request.args.get('department', '')
        age_filter = request.args.get('age', '')
        
        df = prepare_communes_data(region_filter, department_filter, age_filter)
        
        if df.empty:
            return jsonify({'error': 'Aucune donnée disponible'}), 404
        
        # Renommer les colonnes pour l'export
        df = df.rename(columns={
            'Commune': 'Commune',
            'PTOT': 'Population',
            'green_mobility_index': 'Mobilité Verte (%)',
            'avg_commute_time': 'Temps Trajet (min)',
            'velo_percentage': '% Vélo',
            'voiture_percentage': '% Voiture',
            'transport_commun_percentage': '% Transport en Commun',
            'marche_percentage': '% Marche',
            'deux_roues_percentage': '% Deux-roues',
            'pas_transport_percentage': '% Sans Transport'
        })
        
        # Créer un buffer en mémoire
        output = io.StringIO()
        df.to_csv(output, index=False, sep=';', encoding='utf-8-sig')
        output.seek(0)
        
        # Créer un fichier en mémoire
        mem = io.BytesIO()
        mem.write(output.getvalue().encode('utf-8-sig'))
        mem.seek(0)
        
        return send_file(
            mem,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'communes_mobilite_{datetime.now().strftime("%Y%m%d")}.csv'
        )
    except Exception as e:
        logger.error(f"Erreur lors de l'export CSV communes: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@bp.route('/csv/regions')
def export_csv_regions():
    """Export des données régions en CSV avec filtres"""
    try:
        # Récupérer les filtres depuis les paramètres URL
        age_filter = request.args.get('age', '')
        
        df = prepare_regions_data(age_filter)
        
        if df.empty:
            return jsonify({'error': 'Aucune donnée disponible'}), 404
        
        # Renommer les colonnes pour l'export
        df = df.rename(columns={
            'Région': 'Région',
            'NBCOM': 'Nombre Communes',
            'PTOT': 'Population',
            'green_mobility_index': 'Mobilité Verte (%)',
            'avg_commute_time': 'Temps Trajet (min)',
            'velo_percentage': '% Vélo',
            'voiture_percentage': '% Voiture',
            'transport_commun_percentage': '% Transport en Commun',
            'marche_percentage': '% Marche',
            'deux_roues_percentage': '% Deux-roues',
            'pas_transport_percentage': '% Sans Transport'
        })
        
        # Créer un buffer en mémoire
        output = io.StringIO()
        df.to_csv(output, index=False, sep=';', encoding='utf-8-sig')
        output.seek(0)
        
        # Créer un fichier en mémoire
        mem = io.BytesIO()
        mem.write(output.getvalue().encode('utf-8-sig'))
        mem.seek(0)
        
        return send_file(
            mem,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'regions_mobilite_{datetime.now().strftime("%Y%m%d")}.csv'
        )
    except Exception as e:
        logger.error(f"Erreur lors de l'export CSV régions: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@bp.route('/pdf/communes')
def export_pdf_communes():
    """Export des données communes en PDF avec filtres"""
    if not REPORTLAB_AVAILABLE:
        return jsonify({'error': 'reportlab n\'est pas installé. Installez-le avec: pip install reportlab'}), 503
    try:
        # Récupérer les filtres depuis les paramètres URL
        region_filter = request.args.get('region', '')
        department_filter = request.args.get('department', '')
        age_filter = request.args.get('age', '')
        
        df = prepare_communes_data(region_filter, department_filter, age_filter)
        
        if df.empty:
            return jsonify({'error': 'Aucune donnée disponible'}), 404
        
        # Créer un buffer en mémoire pour le PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30
        )
        
        # Titre
        elements.append(Paragraph("Rapport - Indicateurs de Mobilité par Commune", title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Informations générales avec filtres
        stats = main()
        filter_info = []
        if region_filter:
            filter_info.append(f"Région: {region_filter}")
        if department_filter:
            filter_info.append(f"Département: {department_filter}")
        if age_filter:
            filter_info.append(f"Tranche d'âge: {age_filter}")
        
        info_text = f"""
        <b>Date du rapport:</b> {datetime.now().strftime("%d/%m/%Y %H:%M")}<br/>
        <b>Nombre de communes:</b> {len(df)}<br/>
        """
        if filter_info:
            info_text += f"<b>Filtres appliqués:</b> {', '.join(filter_info)}<br/>"
        info_text += f"""
        <b>Taux moyen d'utilisation du vélo:</b> {stats.get('pourcentage_velo', 0):.2f}%<br/>
        <b>Taux moyen d'utilisation des transports en commun:</b> {stats.get('pourcentage_transport_commun', 0):.2f}%
        """
        elements.append(Paragraph(info_text, styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Préparer les données pour le tableau (limiter à 50 lignes)
        df_display = df.head(50).copy()
        df_display = df_display.rename(columns={
            'Commune': 'Commune',
            'PTOT': 'Population',
            'green_mobility_index': 'Mobilité Verte',
            'avg_commute_time': 'Temps Trajet',
            'velo_percentage': '% Vélo',
            'voiture_percentage': '% Voiture',
            'transport_commun_percentage': '% TC',
            'marche_percentage': '% Marche',
            'deux_roues_percentage': '% 2-roues',
            'pas_transport_percentage': '% Sans Transport'
        })
        
        # Créer le tableau
        data = [df_display.columns.tolist()]
        for _, row in df_display.iterrows():
            data.append([
                str(row.get('Commune', 'N/A'))[:30],  # Limiter la longueur
                str(int(row.get('Population', 0))) if pd.notna(row.get('Population')) else 'N/A',
                f"{row.get('Mobilité Verte', 0):.1f}" if pd.notna(row.get('Mobilité Verte')) else 'N/A',
                f"{row.get('Temps Trajet', 0):.1f}" if pd.notna(row.get('Temps Trajet')) else 'N/A',
                f"{row.get('% Vélo', 0):.1f}%" if pd.notna(row.get('% Vélo')) else 'N/A',
                f"{row.get('% Voiture', 0):.1f}%" if pd.notna(row.get('% Voiture')) else 'N/A',
                f"{row.get('% TC', 0):.1f}%" if pd.notna(row.get('% TC')) else 'N/A',
                f"{row.get('% Marche', 0):.1f}%" if pd.notna(row.get('% Marche')) else 'N/A',
                f"{row.get('% 2-roues', 0):.1f}%" if pd.notna(row.get('% 2-roues')) else 'N/A',
                f"{row.get('% Sans Transport', 0):.1f}%" if pd.notna(row.get('% Sans Transport')) else 'N/A'
            ])
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
        ]))
        
        elements.append(table)
        
        if len(df) > 50:
            elements.append(Spacer(1, 0.2*inch))
            elements.append(Paragraph(f"<i>Note: Seules les 50 premières communes sont affichées. Total: {len(df)} communes.</i>", styles['Normal']))
        
        # Construire le PDF
        doc.build(elements)
        buffer.seek(0)
        
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'rapport_communes_mobilite_{datetime.now().strftime("%Y%m%d")}.pdf'
        )
    except Exception as e:
        logger.error(f"Erreur lors de l'export PDF communes: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@bp.route('/pdf/regions')
def export_pdf_regions():
    """Export des données régions en PDF avec filtres"""
    if not REPORTLAB_AVAILABLE:
        return jsonify({'error': 'reportlab n\'est pas installé. Installez-le avec: pip install reportlab'}), 503
    try:
        # Récupérer les filtres depuis les paramètres URL
        age_filter = request.args.get('age', '')
        
        df = prepare_regions_data(age_filter)
        
        if df.empty:
            return jsonify({'error': 'Aucune donnée disponible'}), 404
        
        # Créer un buffer en mémoire pour le PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30
        )
        
        # Titre
        elements.append(Paragraph("Rapport - Indicateurs de Mobilité par Région", title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Informations générales avec filtres
        stats = main()
        filter_info = []
        if age_filter:
            filter_info.append(f"Tranche d'âge: {age_filter}")
        
        info_text = f"""
        <b>Date du rapport:</b> {datetime.now().strftime("%d/%m/%Y %H:%M")}<br/>
        <b>Nombre de régions:</b> {len(df)}<br/>
        """
        if filter_info:
            info_text += f"<b>Filtres appliqués:</b> {', '.join(filter_info)}<br/>"
        info_text += f"""
        <b>Taux moyen d'utilisation du vélo:</b> {stats.get('pourcentage_velo', 0):.2f}%<br/>
        <b>Taux moyen d'utilisation des transports en commun:</b> {stats.get('pourcentage_transport_commun', 0):.2f}%
        """
        elements.append(Paragraph(info_text, styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Préparer les données pour le tableau
        df_display = df.copy()
        df_display = df_display.rename(columns={
            'Région': 'Région',
            'NBCOM': 'Nb Communes',
            'PTOT': 'Population',
            'green_mobility_index': 'Mobilité Verte',
            'avg_commute_time': 'Temps Trajet',
            'velo_percentage': '% Vélo',
            'voiture_percentage': '% Voiture',
            'transport_commun_percentage': '% TC',
            'marche_percentage': '% Marche',
            'deux_roues_percentage': '% 2-roues',
            'pas_transport_percentage': '% Sans Transport'
        })
        
        # Créer le tableau
        data = [df_display.columns.tolist()]
        for _, row in df_display.iterrows():
            data.append([
                str(row.get('Région', 'N/A'))[:25],
                str(int(row.get('Nb Communes', 0))) if pd.notna(row.get('Nb Communes')) else 'N/A',
                str(int(row.get('Population', 0))) if pd.notna(row.get('Population')) else 'N/A',
                f"{row.get('Mobilité Verte', 0):.1f}" if pd.notna(row.get('Mobilité Verte')) else 'N/A',
                f"{row.get('Temps Trajet', 0):.1f}" if pd.notna(row.get('Temps Trajet')) else 'N/A',
                f"{row.get('% Vélo', 0):.1f}%" if pd.notna(row.get('% Vélo')) else 'N/A',
                f"{row.get('% Voiture', 0):.1f}%" if pd.notna(row.get('% Voiture')) else 'N/A',
                f"{row.get('% TC', 0):.1f}%" if pd.notna(row.get('% TC')) else 'N/A',
                f"{row.get('% Marche', 0):.1f}%" if pd.notna(row.get('% Marche')) else 'N/A',
                f"{row.get('% 2-roues', 0):.1f}%" if pd.notna(row.get('% 2-roues')) else 'N/A',
                f"{row.get('% Sans Transport', 0):.1f}%" if pd.notna(row.get('% Sans Transport')) else 'N/A'
            ])
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
        ]))
        
        elements.append(table)
        
        # Construire le PDF
        doc.build(elements)
        buffer.seek(0)
        
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'rapport_regions_mobilite_{datetime.now().strftime("%Y%m%d")}.pdf'
        )
    except Exception as e:
        logger.error(f"Erreur lors de l'export PDF régions: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500
