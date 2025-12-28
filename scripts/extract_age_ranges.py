#!/usr/bin/env python3
"""
Script pour extraire les tranches d'âge réelles du fichier CSV
"""

import pandas as pd
import sys
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

def extract_age_ranges():
    """Extrait toutes les tranches d'âge uniques du fichier CSV"""
    csv_path = Path(__file__).parent.parent / 'data' / 'RP2021_mobpro' / 'Commune_1001-13101_2.csv'
    
    if not csv_path.exists():
        print(f"Fichier non trouvé: {csv_path}")
        return
    
    print(f"Chargement du fichier: {csv_path}")
    print("Taille du fichier:", csv_path.stat().st_size / (1024*1024), "MB")
    
    # Charger seulement la colonne AGEREVQ pour économiser la mémoire
    print("\nChargement de la colonne AGEREVQ...")
    df = pd.read_csv(csv_path, usecols=['AGEREVQ'])
    
    print(f"Nombre total de lignes: {len(df):,}")
    
    # Extraire les valeurs uniques
    age_ranges = df['AGEREVQ'].dropna().unique()
    
    print(f"\n=== TRANCHES D'ÂGE UNIQUES ({len(age_ranges)} trouvées) ===\n")
    
    # Trier et afficher avec le nombre d'occurrences
    age_counts = df['AGEREVQ'].value_counts().sort_index()
    
    for age_range, count in age_counts.items():
        print(f"  {age_range}: {count:,} occurrences")
    
    # Créer un mapping vers les filtres du dropdown
    print("\n=== MAPPING VERS FILTRES DROPDOWN ===\n")
    
    age_mapping = {}
    for age_range in sorted(age_ranges):
        age_str = str(age_range).strip()
        
        # Extraire les nombres de la tranche d'âge
        import re
        numbers = re.findall(r'\d+', age_str)
        
        if numbers:
            min_age = int(numbers[0])
            max_age = int(numbers[-1]) if len(numbers) > 1 else min_age
            
            # Mapper vers les catégories du dropdown
            if min_age < 19:
                category = '0-18'
            elif min_age < 36:
                category = '19-35'
            elif min_age < 51:
                category = '36-50'
            elif min_age < 66:
                category = '51-65'
            else:
                category = '65+'
            
            if category not in age_mapping:
                age_mapping[category] = []
            age_mapping[category].append(age_str)
    
    for category, ages in sorted(age_mapping.items()):
        print(f"\n{category}:")
        for age in ages:
            print(f"  - {age}")
    
    return age_ranges, age_mapping

if __name__ == '__main__':
    extract_age_ranges()


