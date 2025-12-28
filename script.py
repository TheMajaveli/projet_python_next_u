import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def main():
    df_nom_commune = pd.read_csv("data/RP2021_mobpro/varmod_mobpro_2021.csv", sep=';')

    colonne_a_garder_commune = ['COD_VAR', 'COD_MOD', 'LIB_MOD']
    df_nom_commune_filtre = df_nom_commune[colonne_a_garder_commune]

    # Nettoyage et préparation des données

    # Suppression des enregistrements doublons

    presence_de_doublons = df_nom_commune_filtre.duplicated().sum()

    print(presence_de_doublons)
    if presence_de_doublons > 0:
        print("Suppression des doublons")
        df_nom_commune_filtre = df_nom_commune_filtre.drop_duplicates()
    else:
        print("Aucun doublon détecté")


    # Suppression des enregistrements ayant des valeurs manquantes par colonne
    nombre_de_valeurs_manquantes = df_nom_commune_filtre.isna().sum()

    print(nombre_de_valeurs_manquantes.sum())
    if nombre_de_valeurs_manquantes.sum() > 0:
        print("Suppression des enregistrements ayant des valeurs manquantes par colonne")
        df_nom_commune_filtre = df_nom_commune_filtre.dropna()
    else:
        print("Aucune valeur manquante détectée")

    print(df_nom_commune_filtre)

    df_mobilite_commune_1001_13101 = pd.read_csv("data/RP2021_mobpro/Commune_1001-13101.csv")

    # Nettoyage et préparation des données

    # Suppression des enregistrementsdoublons
    presence_de_doublons = df_mobilite_commune_1001_13101.duplicated().sum()

    if presence_de_doublons > 0:
        print("Suppression des doublons")
        df_mobilite_commune_1001_13101 = df_mobilite_commune_1001_13101.drop_duplicates()
    else:
        print("Aucun doublon détecté")

    # Suppression des enregistrements ayant des valeurs manquantes par colonne
    nombre_de_valeurs_manquantes = df_mobilite_commune_1001_13101.isna().sum()

    if nombre_de_valeurs_manquantes.sum() > 0:
        print("Suppression des enregistrements ayant des valeurs manquantes par colonne")
        df_mobilite_commune_1001_13101 = df_mobilite_commune_1001_13101.dropna()
    else:
        print("Aucune valeur manquante détectée")

    # Arrondi du poids de l'individu

    df_mobilite_commune_1001_13101['IPONDI'] = df_mobilite_commune_1001_13101['IPONDI'].round(2)

    df_mobilite_commune_1001_13101.loc[df_mobilite_commune_1001_13101['COMMUNE'].astype(str).str.len() == 4, 'COMMUNE'] = '0' + df_mobilite_commune_1001_13101['COMMUNE'].astype(str)

    df_mobilite_commune_1001_13101.loc[df_mobilite_commune_1001_13101['DCLT'].astype(str).str.len() == 4, 'DCLT'] = '0' + df_mobilite_commune_1001_13101['DCLT'].astype(str)

    df_nom_commune_filtre[df_nom_commune_filtre['COD_VAR'] == "TRANS"][df_nom_commune_filtre['COD_MOD'] == "5"]["LIB_MOD"]

    test = df_mobilite_commune_1001_13101.copy()
    test

    # test['COMMUNE'] = df_nom_commune_filtre[df_nom_commune_filtre['COD_VAR'] == "COMMUNE"][df_nom_commune_filtre['COD_MOD'] == "01001"]["LIB_MOD"]
    # test

    commune_mapping = df_nom_commune_filtre[df_nom_commune_filtre['COD_VAR'] == 'COMMUNE'].set_index('COD_MOD')['LIB_MOD']
    df_mobilite_commune_1001_13101['COMMUNE'] = df_mobilite_commune_1001_13101['COMMUNE'].astype(str).str.zfill(5).map(commune_mapping)

    DCLT_mapping = df_nom_commune_filtre[df_nom_commune_filtre['COD_VAR'] == 'DCLT'].set_index('COD_MOD')['LIB_MOD']
    df_mobilite_commune_1001_13101['DCLT'] = df_mobilite_commune_1001_13101['DCLT'].astype(str).str.zfill(5).map(DCLT_mapping)

    TRANS_mapping = df_nom_commune_filtre[df_nom_commune_filtre['COD_VAR'] == 'TRANS'].set_index('COD_MOD')['LIB_MOD']
    df_mobilite_commune_1001_13101['TRANS'] = df_mobilite_commune_1001_13101['TRANS'].astype(str).str.zfill(1).map(TRANS_mapping)

    AGEREVQ_mapping = df_nom_commune_filtre[df_nom_commune_filtre['COD_VAR'] == 'AGEREVQ'].set_index('COD_MOD')['LIB_MOD']
    df_mobilite_commune_1001_13101['AGEREVQ'] = df_mobilite_commune_1001_13101['AGEREVQ'].astype(str).str.zfill(3).map(AGEREVQ_mapping)

    ILTUU_mapping = df_nom_commune_filtre[df_nom_commune_filtre['COD_VAR'] == 'ILTUU'].set_index('COD_MOD')['LIB_MOD']
    df_mobilite_commune_1001_13101['ILTUU'] = df_mobilite_commune_1001_13101['ILTUU'].astype(str).str.zfill(1).map(ILTUU_mapping)

    df_mobilite_commune_1001_13101.to_csv("data/RP2021_mobpro/Commune_1001-13101_2.csv")

    # df_mobilite_commune_1001_13101

    # Pourcentage de population sans accès direct à un transport:

    # Calcul de la population global:
    population_total = df_mobilite_commune_1001_13101['IPONDI'].sum()
    population_total = round(population_total) 

    print(f"Population total: {population_total}")

    # Calcul de la population sans accès direct à un transport:
    population_sans_transport = df_mobilite_commune_1001_13101[df_mobilite_commune_1001_13101['TRANS'] == "Pas de transport"]['IPONDI'].sum()
    population_sans_transport = round(population_sans_transport)

    print(f"Population sans transport: {population_sans_transport}")

    # Calcul de la population sans accès direct à un transport, en pourcentage:
    pourcentage_population_sans_transport = (population_sans_transport / population_total) * 100
    pourcentage_population_sans_transport = round(pourcentage_population_sans_transport, 2)

    print(f"Pourcentage de population sans transport: {pourcentage_population_sans_transport}%")




    # Population sans transport par commune:

    df = df_mobilite_commune_1001_13101 
    df['sans_transport'] = df['IPONDI'].where(df['TRANS'] == 'Pas de transport', 0)

    df = df.groupby('COMMUNE').agg(
        total_hab=('IPONDI', 'sum'),
        sans_transport=('sans_transport', 'sum')
    ).reset_index()



    # Calcul de temps moyen domicle - travail:

    vitesses = {
        'Pas de transport': 0,
        'Marche à pied (ou rollers, patinette)': 5,
        'Vélo (y compris à assistance électrique)': 15,
        'Deux-roues motorisé': 40,
        'Voiture, camion, fourgonnette': 50,
        'Transports en commun': 30
    }

    # 1. Préparation des codes (en dehors de la boucle)
    # .str[1:-1] est souvent plus rapide qu'un regex si le format est fixe (01001)
    c_codes = df_mobilite_commune_1001_13101['COMMUNE'].astype(str).str.extract(r'\((\d+)\)')[0]
    d_codes = df_mobilite_commune_1001_13101['DCLT'].astype(str).str.extract(r'\((\d+)\)')[0]
    transports = df_mobilite_commune_1001_13101['TRANS']

    # 2. On crée une petite fonction optimisée
    def calcul_vitesse(row):
        c = str(row['c_code'])
        d = str(row['d_code'])
        t = row['TRANS']
        
        v = vitesses.get(t, 0) # .get évite les erreurs si le transport n'est pas dans le dico
        
        if c == d:
            return v
        elif c[:2] == d[:2]: # Même département
            return 1.5 * v
        else:
            return 2 * v

    # 3. On applique sur le dataframe d'un coup
    # On crée des colonnes temporaires pour le calcul
    temp_df = pd.DataFrame({
        'c_code': c_codes,
        'd_code': d_codes,
        'TRANS': transports
    })

    df_mobilite_commune_1001_13101['temps_estime'] = temp_df.apply(calcul_vitesse, axis=1)

    pourcentage_temps_moyen = df_mobilite_commune_1001_13101['temps_estime'].mean()
    pourcentage_temps_moyen = round(pourcentage_temps_moyen, 2)

    # print(pourcentage_temps_moyen)




    # Calculer le taux d'utilisation du vélo

    #Population globale:
    pop_total = df_mobilite_commune_1001_13101['IPONDI'].sum()

    # Population utilisant un vélo:
    pop_velo = df_mobilite_commune_1001_13101[df_mobilite_commune_1001_13101['TRANS'] == 'Vélo (y compris à assistance électrique)']['IPONDI'].sum()

    # Pourcentage de la population utilisant un vélo:
    taux_velo = (pop_velo / pop_total) * 100
    taux_velo = round(taux_velo, 2)

    # print(f"Le taux d'utilisation du vélo est de {taux_velo:.2f}%")


    # Calculer le taux d'utilisation des transports en commun

    # Population utilisant les transports en commun:
    pop_transport_commun = df_mobilite_commune_1001_13101[df_mobilite_commune_1001_13101['TRANS']== 'Transports en commun']['IPONDI'].sum()

    # Pourcentage de la population utilisant les transports en commun:
    taux_transport_commun = (pop_transport_commun / pop_total) * 100
    taux_transport_commun = round(taux_transport_commun, 2)

    # print(f"Le taux d'utilisation des transports en commun est de {taux_transport_commun:.2f}%")

    return {'pourcentage_sans_transport': pourcentage_population_sans_transport, 'pourcentage_temps_moyen': float(pourcentage_temps_moyen), 'pourcentage_velo': float(taux_velo), 'pourcentage_transport_commun': float(taux_transport_commun)}


test = main()
print(test)