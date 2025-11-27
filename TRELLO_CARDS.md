# Structure Trello - Projet Mobilité

## 📋 Instructions d'Import

1. Créer un nouveau board Trello : "Projet Mobilité - Dashboard"
2. Créer les colonnes : `BACKLOG`, `TO DO`, `IN PROGRESS`, `REVIEW`, `DONE`
3. Créer les labels : 🔴 Priorité Haute, 🟡 Priorité Moyenne, 🟢 Priorité Basse, 🐛 Bug, 📊 Data, 🎨 UI/UX, 🔧 Tech, 📝 Doc
4. Créer les membres : Dev 1 (Junior), Dev 2 (Baptiste)
5. Créer les cartes ci-dessous dans l'ordre

---

## 🚀 SPRINT 1 : Setup & Données

### Carte 1 : Configuration Environnement Python/Flask
**Labels** : 🔴 Priorité Haute, 🔧 Tech  
**Assigné à** : Dev 1 (Junior)  
**Colonne** : TO DO

**Description** :
Mettre en place l'environnement de développement pour le projet Flask.

**Checklist** :
- [ ] Créer environnement virtuel Python 3
- [ ] Installer Flask et dépendances de base
- [ ] Créer structure de dossiers (app/, data/, templates/, static/)
- [ ] Configurer requirements.txt
- [ ] Tester que Flask démarre correctement

**Critères d'acceptation** :
- ✅ Environnement virtuel fonctionnel
- ✅ Flask accessible via `flask run`
- ✅ Structure de projet claire et documentée

**Fichiers concernés** :
- `requirements.txt`
- `app/__init__.py`
- `app/main.py`

---

### Carte 2 : Structure Projet Git
**Labels** : 🔴 Priorité Haute, 🔧 Tech  
**Assigné à** : Dev 2 (Baptiste)  
**Colonne** : TO DO

**Description** :
Initialiser le dépôt Git et mettre en place la structure de branches.

**Checklist** :
- [ ] Initialiser dépôt Git
- [ ] Créer .gitignore approprié pour Python/Flask
- [ ] Créer branche `develop`
- [ ] Créer branche `feature/*` pour nouvelles fonctionnalités
- [ ] Configurer README.md de base
- [ ] Premier commit avec structure

**Critères d'acceptation** :
- ✅ Dépôt Git accessible
- ✅ .gitignore exclut venv/, __pycache__, .env
- ✅ README avec instructions de base

**Fichiers concernés** :
- `.gitignore`
- `README.md`

---

### Carte 3 : Récupération Données Sources
**Labels** : 🔴 Priorité Haute, 📊 Data  
**Assigné à** : Dev 1 (Junior)  
**Colonne** : TO DO

**Description** :
Télécharger et organiser les données sources nécessaires au projet.

**Checklist** :
- [ ] Identifier les URLs des données Open Data France
- [ ] Télécharger données transport
- [ ] Télécharger données INSEE (population, zones IRIS)
- [ ] Télécharger données géographiques (coordonnées GPS communes)
- [ ] Organiser les fichiers dans `data/raw/`
- [ ] Documenter les sources dans `data/README.md`

**Critères d'acceptation** :
- ✅ Toutes les sources identifiées et téléchargées
- ✅ Fichiers organisés dans `data/raw/`
- ✅ Documentation des sources disponible

**Fichiers concernés** :
- `data/raw/`
- `data/README.md`

---

### Carte 4 : Analyse Structure Données
**Labels** : 🟡 Priorité Moyenne, 📊 Data  
**Assigné à** : Dev 2 (Baptiste)  
**Colonne** : TO DO

**Description** :
Analyser la structure des données récupérées pour planifier le nettoyage.

**Checklist** :
- [ ] Examiner les colonnes de chaque fichier
- [ ] Identifier les formats de données (dates, nombres, textes)
- [ ] Repérer les valeurs manquantes potentielles
- [ ] Identifier les clés de jointure possibles
- [ ] Créer un document de mapping des données

**Critères d'acceptation** :
- ✅ Document de structure des données créé
- ✅ Clés de jointure identifiées
- ✅ Problèmes potentiels listés

**Fichiers concernés** :
- `docs/DATA_STRUCTURE.md`

---

## 📊 SPRINT 2 : Analyse de Données

### Carte 5 : Script Nettoyage Données - Valeurs Manquantes
**Labels** : 🔴 Priorité Haute, 📊 Data  
**Assigné à** : Dev 1 (Junior)  
**Colonne** : BACKLOG

**Description** :
Créer un script pour nettoyer les valeurs manquantes dans les datasets.

**Checklist** :
- [ ] Identifier les colonnes avec valeurs manquantes
- [ ] Décider de la stratégie (suppression, imputation, moyenne)
- [ ] Implémenter la fonction de nettoyage
- [ ] Tester sur un échantillon
- [ ] Documenter les décisions prises

**Critères d'acceptation** :
- ✅ Fonction `clean_missing_values()` créée
- ✅ Traitement cohérent pour chaque type de données
- ✅ Tests unitaires passent

**Fichiers concernés** :
- `app/data_processing/cleaner.py`
- `tests/test_cleaner.py`

**Dépendances** : Carte 4

---

### Carte 6 : Script Nettoyage Données - Formats
**Labels** : 🔴 Priorité Haute, 📊 Data  
**Assigné à** : Dev 1 (Junior)  
**Colonne** : BACKLOG

**Description** :
Standardiser les formats de données (dates, nombres, textes).

**Checklist** :
- [ ] Convertir les dates au format standard
- [ ] Standardiser les nombres (décimales, séparateurs)
- [ ] Normaliser les textes (majuscules, accents)
- [ ] Créer fonction `standardize_formats()`
- [ ] Tests unitaires

**Critères d'acceptation** :
- ✅ Toutes les dates au format YYYY-MM-DD
- ✅ Nombres au format numérique Python
- ✅ Textes normalisés

**Fichiers concernés** :
- `app/data_processing/cleaner.py`

**Dépendances** : Carte 5

---

### Carte 7 : Script Nettoyage Données - Doublons
**Labels** : 🟡 Priorité Moyenne, 📊 Data  
**Assigné à** : Dev 1 (Junior)  
**Colonne** : BACKLOG

**Description** :
Détecter et supprimer les doublons dans les datasets.

**Checklist** :
- [ ] Identifier les clés uniques pour chaque dataset
- [ ] Détecter les doublons
- [ ] Décider de la stratégie (garder premier, dernier, moyenne)
- [ ] Implémenter `remove_duplicates()`
- [ ] Tests unitaires

**Critères d'acceptation** :
- ✅ Fonction détecte et supprime les doublons
- ✅ Log des doublons supprimés disponible
- ✅ Tests passent

**Fichiers concernés** :
- `app/data_processing/cleaner.py`

**Dépendances** : Carte 6

---

### Carte 8 : Fusion Tables - Démographie + Transport + Géolocalisation
**Labels** : 🔴 Priorité Haute, 📊 Data  
**Assigné à** : Dev 2 (Baptiste)  
**Colonne** : BACKLOG

**Description** :
Créer une fonction pour fusionner les différentes sources de données.

**Checklist** :
- [ ] Identifier les clés de jointure (code commune, code IRIS)
- [ ] Implémenter la fusion avec pandas.merge()
- [ ] Gérer les cas de données manquantes après fusion
- [ ] Créer fonction `merge_datasets()`
- [ ] Sauvegarder le dataset fusionné
- [ ] Tests unitaires

**Critères d'acceptation** :
- ✅ Dataset fusionné créé avec toutes les colonnes nécessaires
- ✅ Pas de perte de données critiques
- ✅ Performance acceptable (< 30s pour fusion complète)

**Fichiers concernés** :
- `app/data_processing/merger.py`
- `data/processed/merged_data.csv`

**Dépendances** : Carte 7

---

### Carte 9 : Fonctions Agrégation - Par Département
**Labels** : 🔴 Priorité Haute, 📊 Data  
**Assigné à** : Dev 1 (Junior)  
**Colonne** : BACKLOG

**Description** :
Créer des fonctions pour agréger les données par département.

**Checklist** :
- [ ] Fonction `aggregate_by_department()`
- [ ] Calculer statistiques (moyenne, médiane, min, max)
- [ ] Grouper par code département
- [ ] Tests unitaires

**Critères d'acceptation** :
- ✅ Agrégation correcte par département
- ✅ Statistiques calculées correctement
- ✅ Tests passent

**Fichiers concernés** :
- `app/data_processing/aggregator.py`

**Dépendances** : Carte 8

---

### Carte 10 : Fonctions Agrégation - Par Type Transport
**Labels** : 🔴 Priorité Haute, 📊 Data  
**Assigné à** : Dev 1 (Junior)  
**Colonne** : BACKLOG

**Description** :
Agréger les données selon le type de transport utilisé.

**Checklist** :
- [ ] Fonction `aggregate_by_transport_type()`
- [ ] Grouper par type (train, bus, voiture, vélo, etc.)
- [ ] Calculer statistiques par type
- [ ] Tests unitaires

**Critères d'acceptation** :
- ✅ Agrégation correcte par type de transport
- ✅ Tous les types de transport identifiés
- ✅ Tests passent

**Fichiers concernés** :
- `app/data_processing/aggregator.py`

**Dépendances** : Carte 8

---

### Carte 11 : Fonctions Agrégation - Par Classe d'Âge
**Labels** : 🟡 Priorité Moyenne, 📊 Data  
**Assigné à** : Dev 1 (Junior)  
**Colonne** : BACKLOG

**Description** :
Agréger les données selon les classes d'âge.

**Checklist** :
- [ ] Définir les classes d'âge (ex: 0-18, 19-35, 36-50, 51-65, 65+)
- [ ] Fonction `aggregate_by_age_group()`
- [ ] Calculer statistiques par classe
- [ ] Tests unitaires

**Critères d'acceptation** :
- ✅ Classes d'âge définies et cohérentes
- ✅ Agrégation correcte
- ✅ Tests passent

**Fichiers concernés** :
- `app/data_processing/aggregator.py`

**Dépendances** : Carte 8

---

### Carte 12 : Calcul Indicateur - Population Sans Accès Transport
**Labels** : 🔴 Priorité Haute, 📊 Data  
**Assigné à** : Dev 2 (Baptiste)  
**Colonne** : BACKLOG

**Description** :
Calculer le pourcentage de population sans accès direct à un transport.

**Checklist** :
- [ ] Définir critère "sans accès direct" (distance, temps)
- [ ] Fonction `calculate_no_transport_access()`
- [ ] Calculer pour chaque commune
- [ ] Valider sur échantillon connu
- [ ] Tests unitaires

**Critères d'acceptation** :
- ✅ Indicateur calculé correctement
- ✅ Résultats validés
- ✅ Documentation de la formule

**Fichiers concernés** :
- `app/indicators/accessibility.py`
- `docs/INDICATORS.md`

**Dépendances** : Carte 8

---

### Carte 13 : Calcul Indicateur - Temps Moyen Domicile-Travail
**Labels** : 🔴 Priorité Haute, 📊 Data  
**Assigné à** : Dev 2 (Baptiste)  
**Colonne** : BACKLOG

**Description** :
Calculer le temps moyen de trajet domicile-travail.

**Checklist** :
- [ ] Fonction `calculate_avg_commute_time()`
- [ ] Calculer par commune, département, région
- [ ] Gérer les valeurs manquantes
- [ ] Valider les résultats
- [ ] Tests unitaires

**Critères d'acceptation** :
- ✅ Temps moyen calculé correctement
- ✅ Disponible à différents niveaux géographiques
- ✅ Tests passent

**Fichiers concernés** :
- `app/indicators/commute.py`

**Dépendances** : Carte 8

---

### Carte 14 : Calcul Indicateur - Taux Utilisation Vélo
**Labels** : 🟡 Priorité Moyenne, 📊 Data  
**Assigné à** : Dev 1 (Junior)  
**Colonne** : BACKLOG

**Description** :
Calculer le taux d'utilisation du vélo.

**Checklist** :
- [ ] Fonction `calculate_bike_usage_rate()`
- [ ] Calculer pourcentage d'utilisateurs vélo
- [ ] Calculer par zone géographique
- [ ] Tests unitaires

**Critères d'acceptation** :
- ✅ Taux calculé correctement (0-100%)
- ✅ Disponible par commune/département
- ✅ Tests passent

**Fichiers concernés** :
- `app/indicators/transport_modes.py`

**Dépendances** : Carte 8

---

### Carte 15 : Calcul Indicateur - Taux Utilisation Transports Communs
**Labels** : 🟡 Priorité Moyenne, 📊 Data  
**Assigné à** : Dev 1 (Junior)  
**Colonne** : BACKLOG

**Description** :
Calculer le taux d'utilisation des transports en commun.

**Checklist** :
- [ ] Fonction `calculate_public_transport_rate()`
- [ ] Inclure train, bus, métro, tram
- [ ] Calculer par zone géographique
- [ ] Tests unitaires

**Critères d'acceptation** :
- ✅ Taux calculé correctement
- ✅ Tous les modes de transport inclus
- ✅ Tests passent

**Fichiers concernés** :
- `app/indicators/transport_modes.py`

**Dépendances** : Carte 8

---

## 🗺️ SPRINT 3 : Visualisations

### Carte 16 : Carte Folium - Localisation Communes
**Labels** : 🔴 Priorité Haute, 🎨 UI/UX  
**Assigné à** : Dev 2 (Baptiste)  
**Colonne** : BACKLOG

**Description** :
Créer une carte interactive Folium affichant la localisation des communes.

**Checklist** :
- [ ] Créer carte Folium de base (France)
- [ ] Ajouter marqueurs pour chaque commune
- [ ] Ajouter popup avec nom commune
- [ ] Fonction `create_communes_map()`
- [ ] Tester avec échantillon de communes

**Critères d'acceptation** :
- ✅ Carte affiche toutes les communes
- ✅ Popups fonctionnent
- ✅ Performance acceptable (< 5s chargement)

**Fichiers concernés** :
- `app/visualizations/maps.py`

**Dépendances** : Carte 8

---

### Carte 17 : Carte Folium - Zones Mal Desservies
**Labels** : 🔴 Priorité Haute, 🎨 UI/UX  
**Assigné à** : Dev 2 (Baptiste)  
**Colonne** : BACKLOG

**Description** :
Mettre en évidence les zones mal desservies sur la carte (marqueurs/cercles rouges).

**Checklist** :
- [ ] Identifier critère "mal desservie" (basé sur indicateurs)
- [ ] Ajouter cercles/marqueurs rouges pour zones mal desservies
- [ ] Légende claire
- [ ] Fonction `highlight_underserved_areas()`
- [ ] Tests visuels

**Critères d'acceptation** :
- ✅ Zones mal desservies clairement identifiées
- ✅ Légende explicative
- ✅ Performance acceptable

**Fichiers concernés** :
- `app/visualizations/maps.py`

**Dépendances** : Carte 12, Carte 16

---

### Carte 18 : Carte Folium - Indicateur Mobilité Verte
**Labels** : 🟡 Priorité Moyenne, 🎨 UI/UX  
**Assigné à** : Dev 2 (Baptiste)  
**Colonne** : BACKLOG

**Description** :
Colorer les communes selon un indicateur de "mobilité verte" (vélo + transports communs).

**Checklist** :
- [ ] Calculer indicateur mobilité verte (vélo + TC)
- [ ] Créer échelle de couleurs (vert = élevé, rouge = faible)
- [ ] Appliquer couleurs aux communes
- [ ] Légende avec échelle
- [ ] Fonction `create_green_mobility_map()`

**Critères d'acceptation** :
- ✅ Carte colorée selon indicateur
- ✅ Légende claire
- ✅ Performance acceptable

**Fichiers concernés** :
- `app/visualizations/maps.py`

**Dépendances** : Carte 14, Carte 15, Carte 16

---

### Carte 19 : Graphiques - Histogrammes
**Labels** : 🟡 Priorité Moyenne, 🎨 UI/UX  
**Assigné à** : Dev 1 (Junior)  
**Colonne** : BACKLOG

**Description** :
Créer des histogrammes pour visualiser la distribution des indicateurs.

**Checklist** :
- [ ] Fonction `create_histogram()` générique
- [ ] Histogramme temps moyen domicile-travail
- [ ] Histogramme taux utilisation vélo
- [ ] Histogramme taux utilisation TC
- [ ] Sauvegarder en PNG/SVG

**Critères d'acceptation** :
- ✅ Histogrammes lisibles et pertinents
- ✅ Axes et labels clairs
- ✅ Fonction réutilisable

**Fichiers concernés** :
- `app/visualizations/charts.py`

**Dépendances** : Carte 13, Carte 14, Carte 15

---

### Carte 20 : Graphiques - Bar Charts
**Labels** : 🟡 Priorité Moyenne, 🎨 UI/UX  
**Assigné à** : Dev 1 (Junior)  
**Colonne** : BACKLOG

**Description** :
Créer des bar charts pour comparer les indicateurs entre zones.

**Checklist** :
- [ ] Fonction `create_bar_chart()` générique
- [ ] Bar chart par département
- [ ] Bar chart par type de transport
- [ ] Bar chart par classe d'âge
- [ ] Sauvegarder en PNG/SVG

**Critères d'acceptation** :
- ✅ Bar charts lisibles
- ✅ Comparaisons claires
- ✅ Fonction réutilisable

**Fichiers concernés** :
- `app/visualizations/charts.py`

**Dépendances** : Carte 9, Carte 10, Carte 11

---

### Carte 21 : Graphiques - Courbes d'Évolution
**Labels** : 🟢 Priorité Basse, 🎨 UI/UX  
**Assigné à** : Dev 1 (Junior)  
**Colonne** : BACKLOG

**Description** :
Créer des courbes d'évolution pour montrer les tendances (si données temporelles disponibles).

**Checklist** :
- [ ] Vérifier disponibilité données temporelles
- [ ] Fonction `create_evolution_curve()`
- [ ] Courbe évolution temps moyen
- [ ] Courbe évolution taux vélo/TC
- [ ] Sauvegarder en PNG/SVG

**Critères d'acceptation** :
- ✅ Courbes lisibles si données disponibles
- ✅ Tendances clairement visibles
- ✅ Sinon, marquer comme non applicable

**Fichiers concernés** :
- `app/visualizations/charts.py`

**Dépendances** : Carte 8 (vérifier données temporelles)

---

## 🌐 SPRINT 4 : Dashboard Web

### Carte 22 : Templates HTML/Jinja2 - Structure Base
**Labels** : 🔴 Priorité Haute, 🎨 UI/UX  
**Assigné à** : Dev 1 (Junior)  
**Colonne** : BACKLOG

**Description** :
Créer la structure de base des templates HTML avec Jinja2.

**Checklist** :
- [ ] Template base.html avec Bootstrap
- [ ] Template layout responsive
- [ ] Navigation principale
- [ ] Footer
- [ ] Intégration Jinja2

**Critères d'acceptation** :
- ✅ Structure HTML valide
- ✅ Responsive sur mobile et desktop
- ✅ Navigation fonctionnelle

**Fichiers concernés** :
- `app/templates/base.html`
- `app/templates/layout.html`

**Dépendances** : Carte 1

---

### Carte 23 : Page Accueil Dashboard
**Labels** : 🔴 Priorité Haute, 🎨 UI/UX  
**Assigné à** : Dev 1 (Junior)  
**Colonne** : BACKLOG

**Description** :
Créer la page d'accueil du dashboard avec vue d'ensemble.

**Checklist** :
- [ ] Template index.html
- [ ] Afficher indicateurs clés (KPIs)
- [ ] Lien vers cartes et graphiques
- [ ] Design attractif

**Critères d'acceptation** :
- ✅ Page d'accueil claire et informative
- ✅ KPIs affichés correctement
- ✅ Navigation vers autres pages

**Fichiers concernés** :
- `app/templates/index.html`
- `app/routes/main.py`

**Dépendances** : Carte 22

---

### Carte 24 : Page Affichage Indicateurs par Commune
**Labels** : 🔴 Priorité Haute, 🎨 UI/UX  
**Assigné à** : Dev 2 (Baptiste)  
**Colonne** : BACKLOG

**Description** :
Créer une page pour afficher les indicateurs d'une commune sélectionnée.

**Checklist** :
- [ ] Template commune.html
- [ ] Route Flask `/commune/<code>`
- [ ] Afficher tous les indicateurs de la commune
- [ ] Intégrer carte Folium de la commune
- [ ] Design clair

**Critères d'acceptation** :
- ✅ Page affiche tous les indicateurs
- ✅ Carte intégrée correctement
- ✅ Navigation fonctionne

**Fichiers concernés** :
- `app/templates/commune.html`
- `app/routes/commune.py`

**Dépendances** : Carte 22, Carte 16

---

### Carte 25 : Page Affichage Indicateurs par Région
**Labels** : 🟡 Priorité Moyenne, 🎨 UI/UX  
**Assigné à** : Dev 2 (Baptiste)  
**Colonne** : BACKLOG

**Description** :
Créer une page pour afficher les indicateurs agrégés par région.

**Checklist** :
- [ ] Template region.html
- [ ] Route Flask `/region/<code>`
- [ ] Afficher indicateurs agrégés
- [ ] Liste des communes de la région
- [ ] Graphiques comparatifs

**Critères d'acceptation** :
- ✅ Indicateurs régionaux affichés
- ✅ Comparaisons claires
- ✅ Navigation fonctionne

**Fichiers concernés** :
- `app/templates/region.html`
- `app/routes/region.py`

**Dépendances** : Carte 22, Carte 9

---

### Carte 26 : Système de Filtres - Zone Géographique
**Labels** : 🔴 Priorité Haute, 🔧 Tech  
**Assigné à** : Dev 2 (Baptiste)  
**Colonne** : BACKLOG

**Description** :
Implémenter un système de filtres par zone géographique (département, région, commune).

**Checklist** :
- [ ] Formulaire de filtres dans template
- [ ] Route Flask pour traitement filtres
- [ ] Filtre par département
- [ ] Filtre par région
- [ ] Filtre par commune
- [ ] Mise à jour dynamique des résultats

**Critères d'acceptation** :
- ✅ Filtres fonctionnent correctement
- ✅ Résultats mis à jour après sélection
- ✅ Interface intuitive

**Fichiers concernés** :
- `app/templates/filters.html`
- `app/routes/filters.py`

**Dépendances** : Carte 22

---

### Carte 27 : Système de Filtres - Type de Transport
**Labels** : 🟡 Priorité Moyenne, 🔧 Tech  
**Assigné à** : Dev 2 (Baptiste)  
**Colonne** : BACKLOG

**Description** :
Implémenter un filtre pour sélectionner le type de transport.

**Checklist** :
- [ ] Checkbox/multiselect pour types de transport
- [ ] Route Flask pour traitement
- [ ] Filtrage des données selon sélection
- [ ] Mise à jour graphiques/cartes

**Critères d'acceptation** :
- ✅ Filtre fonctionne
- ✅ Graphiques mis à jour
- ✅ Interface claire

**Fichiers concernés** :
- `app/routes/filters.py`

**Dépendances** : Carte 26

---

### Carte 28 : Système de Filtres - Tranche d'Âge
**Labels** : 🟡 Priorité Moyenne, 🔧 Tech  
**Assigné à** : Dev 1 (Junior)  
**Colonne** : BACKLOG

**Description** :
Implémenter un filtre pour sélectionner la tranche d'âge.

**Checklist** :
- [ ] Select pour tranches d'âge
- [ ] Route Flask pour traitement
- [ ] Filtrage des données
- [ ] Mise à jour graphiques

**Critères d'acceptation** :
- ✅ Filtre fonctionne
- ✅ Données filtrées correctement
- ✅ Interface claire

**Fichiers concernés** :
- `app/routes/filters.py`

**Dépendances** : Carte 26

---

### Carte 29 : Intégration Visualisations dans Flask
**Labels** : 🔴 Priorité Haute, 🔧 Tech  
**Assigné à** : Dev 2 (Baptiste)  
**Colonne** : BACKLOG

**Description** :
Intégrer les cartes Folium et graphiques dans les pages Flask.

**Checklist** :
- [ ] Route pour générer cartes Folium
- [ ] Route pour générer graphiques
- [ ] Intégration dans templates
- [ ] Cache des visualisations (si nécessaire)
- [ ] Tests d'intégration

**Critères d'acceptation** :
- ✅ Cartes s'affichent dans pages
- ✅ Graphiques s'affichent correctement
- ✅ Performance acceptable

**Fichiers concernés** :
- `app/routes/visualizations.py`
- Templates concernés

**Dépendances** : Carte 16, Carte 19, Carte 20

---

## 📤 SPRINT 5 : Exports & Bonus

### Carte 30 : Export CSV
**Labels** : 🔴 Priorité Haute, 🔧 Tech  
**Assigné à** : Dev 1 (Junior)  
**Colonne** : BACKLOG

**Description** :
Implémenter l'export des données filtrées en CSV.

**Checklist** :
- [ ] Route Flask `/export/csv`
- [ ] Fonction `export_to_csv()`
- [ ] Respecter les filtres appliqués
- [ ] Téléchargement fichier
- [ ] Tests

**Critères d'acceptation** :
- ✅ CSV généré correctement
- ✅ Contient toutes les données demandées
- ✅ Téléchargement fonctionne

**Fichiers concernés** :
- `app/routes/export.py`
- `app/utils/csv_exporter.py`

**Dépendances** : Carte 26

---

### Carte 31 : Export PDF - Base
**Labels** : 🔴 Priorité Haute, 🔧 Tech  
**Assigné à** : Dev 2 (Baptiste)  
**Colonne** : BACKLOG

**Description** :
Implémenter l'export de base en PDF (tableau de données).

**Checklist** :
- [ ] Installer FPDF ou ReportLab
- [ ] Route Flask `/export/pdf`
- [ ] Fonction `export_to_pdf()`
- [ ] Générer PDF avec données
- [ ] Téléchargement fichier
- [ ] Tests

**Critères d'acceptation** :
- ✅ PDF généré correctement
- ✅ Format lisible
- ✅ Téléchargement fonctionne

**Fichiers concernés** :
- `app/routes/export.py`
- `app/utils/pdf_exporter.py`

**Dépendances** : Carte 30

---

### Carte 32 : Export PDF - Rapport Personnalisé (BONUS)
**Labels** : 🟢 Priorité Basse, 🔧 Tech  
**Assigné à** : Dev 2 (Baptiste)  
**Colonne** : BACKLOG

**Description** :
Créer un rapport PDF personnalisé avec sélection de zone, indicateurs et graphiques.

**Checklist** :
- [ ] Formulaire de sélection zone
- [ ] Sélection indicateurs à inclure
- [ ] Génération PDF avec graphiques intégrés
- [ ] Mise en page professionnelle
- [ ] Résumé des indicateurs

**Critères d'acceptation** :
- ✅ Rapport PDF complet et lisible
- ✅ Graphiques intégrés
- ✅ Mise en page soignée

**Fichiers concernés** :
- `app/routes/export.py`
- `app/utils/pdf_report_generator.py`

**Dépendances** : Carte 31, Carte 19, Carte 20

---

### Carte 33 : Tests Finaux et Corrections
**Labels** : 🔴 Priorité Haute, 🐛 Bug  
**Assigné à** : Dev 1 + Dev 2  
**Colonne** : BACKLOG

**Description** :
Effectuer des tests finaux et corriger les bugs identifiés.

**Checklist** :
- [ ] Tests de toutes les fonctionnalités
- [ ] Tests sur différents navigateurs
- [ ] Tests responsive
- [ ] Correction des bugs identifiés
- [ ] Optimisation performance

**Critères d'acceptation** :
- ✅ Tous les tests passent
- ✅ Pas de bugs critiques
- ✅ Performance acceptable

**Fichiers concernés** :
- Tous les fichiers

**Dépendances** : Toutes les cartes précédentes

---

## 📝 SPRINT 6 : Documentation & Finalisation

### Carte 34 : Guide d'Installation
**Labels** : 🔴 Priorité Haute, 📝 Doc  
**Assigné à** : Dev 1 (Junior)  
**Colonne** : BACKLOG

**Description** :
Créer un guide d'installation complet pour le projet.

**Checklist** :
- [ ] Prérequis (Python, versions)
- [ ] Installation dépendances
- [ ] Configuration environnement
- [ ] Instructions démarrage
- [ ] Dépannage (troubleshooting)

**Critères d'acceptation** :
- ✅ Guide complet et clair
- ✅ Instructions testées
- ✅ Accessible aux nouveaux utilisateurs

**Fichiers concernés** :
- `README.md`
- `docs/INSTALLATION.md`

---

### Carte 35 : Documentation Indicateurs
**Labels** : 🔴 Priorité Haute, 📝 Doc  
**Assigné à** : Dev 1 (Junior)  
**Colonne** : BACKLOG

**Description** :
Documenter tous les indicateurs calculés (formules, signification).

**Checklist** :
- [ ] Liste tous les indicateurs
- [ ] Formule de calcul pour chacun
- [ ] Signification métier
- [ ] Exemples de valeurs
- [ ] Unités utilisées

**Critères d'acceptation** :
- ✅ Documentation complète
- ✅ Formules correctes
- ✅ Exemples clairs

**Fichiers concernés** :
- `docs/INDICATORS.md`

---

### Carte 36 : Documentation Données
**Labels** : 🟡 Priorité Moyenne, 📝 Doc  
**Assigné à** : Dev 2 (Baptiste)  
**Colonne** : BACKLOG

**Description** :
Documenter les sources de données et leur structure.

**Checklist** :
- [ ] Sources de données (URLs, dates)
- [ ] Structure de chaque fichier
- [ ] Clés de jointure
- [ ] Fréquence de mise à jour
- [ ] Licences

**Critères d'acceptation** :
- ✅ Documentation complète des sources
- ✅ Structure claire
- ✅ Informations de licence

**Fichiers concernés** :
- `docs/DATA_SOURCES.md`

---

### Carte 37 : Revue Code Finale
**Labels** : 🔴 Priorité Haute, 🔧 Tech  
**Assigné à** : Dev 2 (Baptiste)  
**Colonne** : BACKLOG

**Description** :
Effectuer une revue complète du code pour qualité et cohérence.

**Checklist** :
- [ ] Vérifier style de code (PEP 8)
- [ ] Vérifier commentaires
- [ ] Vérifier gestion erreurs
- [ ] Vérifier sécurité (injections, etc.)
- [ ] Optimisations finales

**Critères d'acceptation** :
- ✅ Code propre et commenté
- ✅ Pas de vulnérabilités évidentes
- ✅ Performance optimisée

**Fichiers concernés** :
- Tous les fichiers Python

---

### Carte 38 : Préparation Présentation Orale
**Labels** : 🔴 Priorité Haute, 📝 Doc  
**Assigné à** : Dev 1 + Dev 2  
**Colonne** : BACKLOG

**Description** :
Préparer la présentation orale de 10 minutes du projet.

**Checklist** :
- [ ] Slides de présentation
- [ ] Démo du dashboard
- [ ] Résultats clés à présenter
- [ ] Répartition temps de parole
- [ ] Répétition

**Critères d'acceptation** :
- ✅ Présentation prête (10 min)
- ✅ Démo fonctionnelle
- ✅ Points clés identifiés

**Fichiers concernés** :
- `docs/PRESENTATION.md`
- Slides (PowerPoint/PDF)

---

## 📊 Statistiques du Board

- **Total cartes** : 38
- **Sprint 1** : 4 cartes
- **Sprint 2** : 11 cartes
- **Sprint 3** : 6 cartes
- **Sprint 4** : 8 cartes
- **Sprint 5** : 4 cartes
- **Sprint 6** : 5 cartes

---

## 🎯 Actions Immédiates

1. Créer le board Trello avec cette structure
2. Déplacer les cartes du Sprint 1 dans "TO DO"
3. Assigner les développeurs selon les cartes
4. Définir les dates de début/fin de chaque sprint
5. Organiser la réunion de kickoff

---

**Bonne chance avec le projet ! 🚀**

