"""
Module de création de graphiques avec Matplotlib et Seaborn
"""

import matplotlib
matplotlib.use('Agg')  # Backend non-interactif pour Flask
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import logging
from typing import Optional, Dict, Any
from pathlib import Path
import io
import base64

logger = logging.getLogger(__name__)

# Configuration du style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'DejaVu Sans'


def create_histogram(
    df: pd.DataFrame,
    column: str,
    title: str = None,
    xlabel: str = None,
    ylabel: str = "Nombre de communes",
    bins: int = 30,
    return_base64: bool = False,
    output_path: Optional[str] = None
) -> Optional[str]:
    """
    Crée un histogramme pour visualiser la distribution d'une variable.
    
    Args:
        df: DataFrame avec les données
        column: Colonne à visualiser
        title: Titre du graphique
        xlabel: Label de l'axe X
        ylabel: Label de l'axe Y
        bins: Nombre de bins pour l'histogramme
        return_base64: Si True, retourne l'image en base64
        output_path: Chemin pour sauvegarder (optionnel)
    
    Returns:
        Chemin du fichier ou string base64 si return_base64=True
    """
    if column not in df.columns:
        logger.error(f"Colonne {column} non trouvée")
        return None
    
    # Filtrer les valeurs manquantes
    data = df[column].dropna()
    
    if len(data) == 0:
        logger.warning(f"Aucune donnée pour {column}")
        return None
    
    # Créer le graphique
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(data, bins=bins, edgecolor='black', alpha=0.7, color='steelblue')
    
    # Labels et titre
    ax.set_xlabel(xlabel or column, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(title or f"Distribution de {column}", fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    # Sauvegarder ou retourner
    if return_base64:
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        return image_base64
    
    if output_path:
        plt.savefig(output_path, dpi=100, bbox_inches='tight')
        plt.close()
        logger.info(f"Histogramme sauvegardé: {output_path}")
        return output_path
    
    plt.close()
    return None


def create_bar_chart(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    title: str = None,
    xlabel: str = None,
    ylabel: str = None,
    return_base64: bool = False,
    output_path: Optional[str] = None,
    max_items: int = 20,
    horizontal: bool = True
) -> Optional[str]:
    """
    Crée un bar chart pour comparer des valeurs.
    
    Args:
        df: DataFrame avec les données
        x_column: Colonne pour l'axe X (catégories)
        y_column: Colonne pour l'axe Y (valeurs)
        title: Titre du graphique
        xlabel: Label de l'axe X
        ylabel: Label de l'axe Y
        return_base64: Si True, retourne en base64
        output_path: Chemin pour sauvegarder
        max_items: Nombre maximum d'items à afficher
        horizontal: Si True, barres horizontales, sinon verticales
    
    Returns:
        Chemin du fichier ou string base64
    """
    if x_column not in df.columns or y_column not in df.columns:
        logger.error(f"Colonnes non trouvées: {x_column} ou {y_column}")
        return None
    
    # Agréger les données si nécessaire
    if len(df) > max_items:
        # Prendre les top N par valeur Y
        df_sorted = df.nlargest(max_items, y_column)
    else:
        df_sorted = df.copy()
    
    # Créer le graphique
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Trier par valeur décroissante
    df_sorted = df_sorted.sort_values(y_column, ascending=horizontal)
    
    if horizontal:
        bars = ax.barh(
            range(len(df_sorted)),
            df_sorted[y_column].values,
            color='steelblue',
            alpha=0.7,
            edgecolor='black'
        )
        # Labels
        ax.set_yticks(range(len(df_sorted)))
        ax.set_yticklabels(df_sorted[x_column].astype(str), fontsize=9)
        ax.set_xlabel(ylabel or y_column, fontsize=11)
        ax.set_ylabel(xlabel or x_column, fontsize=11)
    else:
        bars = ax.bar(
            range(len(df_sorted)),
            df_sorted[y_column].values,
            color='steelblue',
            alpha=0.7,
            edgecolor='black'
        )
        # Labels
        ax.set_xticks(range(len(df_sorted)))
        ax.set_xticklabels(df_sorted[x_column].astype(str), fontsize=9, rotation=45, ha='right')
        ax.set_xlabel(xlabel or x_column, fontsize=11)
        ax.set_ylabel(ylabel or y_column, fontsize=11)
    
    ax.set_title(title or f"{y_column} par {x_column}", fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x' if horizontal else 'y')
    
    plt.tight_layout()
    
    # Sauvegarder ou retourner
    if return_base64:
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        return image_base64
    
    if output_path:
        plt.savefig(output_path, dpi=100, bbox_inches='tight')
        plt.close()
        logger.info(f"Bar chart sauvegardé: {output_path}")
        return output_path
    
    plt.close()
    return None





