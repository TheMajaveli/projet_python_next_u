# Tableau de bord d'analyse des inégalités de mobilité en France

## 📋 Description du Projet

Cette application web est un **tableau de bord interactif** permettant d'analyser les inégalités de mobilité entre les communes françaises. Elle permet aux collectivités et aux chercheurs de :

- **Comparer les conditions de mobilité** entre communes (urbaines vs rurales)
- **Identifier les zones mal desservies** en transport
- **Analyser les modes de transport** utilisés par tranche d'âge
- **Produire des indicateurs** pour appuyer des décisions (infrastructures, communication, open data)
- **Exporter les données** filtrées en CSV ou PDF

---

## 🎯 Comment l'Application Fonctionne

### Architecture Générale

L'application suit une architecture **Flask** classique avec séparation des responsabilités :

```
┌─────────────────┐
│   Utilisateur   │
│   (Navigateur)  │
└────────┬────────┘
         │ Requêtes HTTP
         ▼
┌─────────────────┐
│   Flask App     │  ← app.py (point d'entrée)
│   (Routes)      │
└────────┬────────┘
         │
    ┌────┴────┬──────────────┬──────────────┐
    ▼         ▼              ▼              ▼
┌────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ Pages  │ │  API     │ │ Export   │ │  Maps    │
│ HTML   │ │  JSON    │ │ CSV/PDF  │ │  Charts  │
└────────┘ └──────────┘ └──────────┘ └──────────┘
    │         │              │              │
    └─────────┴──────────────┴──────────────┘
                    │
                    ▼
         ┌──────────────────┐
         │  Data Loader     │  ← Charge les CSV
         │  (avec Cache)    │
         └─────────┬────────┘
                   │
                   ▼
         ┌──────────────────┐
         │  Fichiers CSV    │
         │  - Communes      │
         │  - Mobilité      │
         │  - Régions       │
         └──────────────────┘
```

### Flux de Données

1. **Chargement Initial** :
   - L'application charge les données depuis les fichiers CSV dans `data/`
   - Un système de **cache en mémoire** évite de recharger les fichiers à chaque requête
   - Le cache se met à jour automatiquement si les fichiers CSV sont modifiés

2. **Traitement des Données** :
   - Les données de mobilité (`Commune_1001-13101_2.csv`) contiennent ~670 000 lignes
   - Chaque ligne représente un individu avec son mode de transport, sa tranche d'âge, sa commune
   - L'application **groupe par commune** et calcule des pourcentages pour chaque type de transport

3. **Calcul des Indicateurs** :
   - **Pourcentages par type de transport** : vélo, voiture, transports en commun, marche, etc.
   - **Indice de mobilité verte** : combinaison du taux de vélo et de transports en commun
   - **Temps de trajet moyen** : estimation basée sur le type de transport utilisé
   - **Filtrage par tranche d'âge** : permet d'analyser les comportements par génération

4. **Affichage dans l'Interface** :
   - Les données sont envoyées au navigateur via des **API JSON** (pas de rechargement complet de page)
   - Le frontend utilise **JavaScript** pour charger dynamiquement les tableaux
   - Les filtres (région, département, âge) sont appliqués côté serveur avant l'envoi

---

## 🚀 Installation et Démarrage

### Prérequis

- **Python 3.8 ou supérieur** (testé avec Python 3.11)
- **pip** (gestionnaire de packages Python)
- **Git** (pour cloner le dépôt)

### Étapes d'Installation

#### 1. Cloner le dépôt

```bash
git clone <url-du-depot>
cd projet_python_next_u
```

#### 2. Créer l'environnement virtuel

L'environnement virtuel isole les dépendances du projet :

```bash
python3 -m venv venv
```

#### 3. Activer l'environnement virtuel

**Sur macOS/Linux :**
```bash
source venv/bin/activate
```

**Sur Windows :**
```bash
venv\Scripts\activate
```

Vous devriez voir `(venv)` apparaître dans votre terminal.

#### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

Cette commande installe toutes les bibliothèques nécessaires :
- **Flask** : framework web
- **Pandas** : manipulation de données
- **Folium** : génération de cartes interactives
- **Matplotlib/Seaborn** : création de graphiques
- **ReportLab** : génération de PDF

#### 5. Vérifier les données

Assurez-vous que les fichiers CSV sont présents :
- `data/RP2021_mobpro/Commune_1001-13101_2.csv` (données de mobilité)
- `ensemble/donnees_communes.csv` (données démographiques)
- `ensemble/donnees_regions.csv` (données régionales)

### Démarrage de l'Application

#### Option 1 : Utiliser le script de démarrage

```bash
./start.sh
```

#### Option 2 : Démarrer manuellement

```bash
# Activer l'environnement virtuel (si pas déjà fait)
source venv/bin/activate

# Démarrer Flask
export FLASK_APP=app.py
flask run
```

Ou directement :
```bash
python app.py
```

#### Accéder à l'application

- Ouvrir un navigateur à l'adresse : **http://127.0.0.1:5000**
- Vérifier l'état de l'application : **http://127.0.0.1:5000/health**

---

## 📖 Guide d'Utilisation

### Page d'Accueil (`/`)

La page d'accueil affiche :
- **Statistiques globales** : pourcentages moyens de chaque mode de transport
- **Top 5 Communes** : communes les plus peuplées avec leur indice de mobilité verte
- **Top 5 Régions** : régions les plus peuplées avec leurs indicateurs
- **Cartes interactives** : visualisation géographique des données
- **Graphiques statistiques** : distribution des temps de trajet, usage des transports

### Page Communes (`/mobilite/communes`)

Cette page permet d'analyser les données par commune avec :

#### Filtres Disponibles

1. **Région** : Filtrer par région française (ex: Île-de-France, Auvergne-Rhône-Alpes)
2. **Département** : Filtrer par département (apparaît après sélection d'une région)
3. **Tranche d'Âge** : Filtrer par groupe d'âge
   - 0-18 ans
   - 19-35 ans
   - 36-50 ans
   - 51-65 ans
   - 65+ ans

#### Tableau des Indicateurs

Pour chaque commune, le tableau affiche :
- **Nom de la commune**
- **Population** (ajustée selon la tranche d'âge si filtre actif)
- **Pourcentages par type de transport** :
  - 🚴 Vélo
  - 🚗 Voiture
  - 🚌 Transports en commun
  - 🚶 Marche à pied
  - 🏍️ Deux-roues motorisé
  - ❌ Pas de transport
- **Indice de mobilité verte** : score combinant vélo + transports en commun
- **Temps de trajet moyen** : en minutes

#### Fonctionnalités

- **Pagination** : 10 communes par page (configurable)
- **Détails** : Cliquer sur une commune ouvre une modale avec les détails complets
- **Export CSV** : Télécharger les données filtrées en CSV
- **Export PDF** : Générer un rapport PDF avec les données filtrées

### Page Régions (`/mobilite/regions`)

Similaire à la page Communes, mais agrégée au niveau régional :

- **Filtre par tranche d'âge** uniquement
- **Indicateurs agrégés** pour chaque région
- **Export CSV/PDF** des données régionales

---

## 🛠️ Structure Technique du Projet

### Organisation des Fichiers

```
projet_python_next_u/
├── app/                          # Code source de l'application
│   ├── __init__.py               # Factory Flask (création de l'app)
│   ├── main.py                   # Routes principales (page d'accueil)
│   ├── routes/                   # Routes organisées par fonctionnalité
│   │   ├── mobilite.py          # Routes communes/régions + API JSON
│   │   ├── export.py            # Routes export CSV/PDF
│   │   └── visualizations.py    # Routes cartes et graphiques
│   ├── utils/                   # Utilitaires
│   │   ├── data_loader.py       # Chargement CSV avec cache
│   │   └── cache.py             # Cache des statistiques globales
│   └── visualizations/          # Génération de visualisations
│       ├── maps.py              # Cartes Folium interactives
│       └── charts.py            # Graphiques Matplotlib/Seaborn
├── templates/                    # Templates HTML (Jinja2)
│   ├── base/                    # Templates de base
│   ├── pages/                   # Pages principales
│   │   └── home.html           # Page d'accueil
│   └── mobilite/                # Pages mobilité
│       ├── communes.html       # Page communes
│       └── regions.html        # Page régions
├── static/                      # Fichiers statiques
│   ├── css/                    # Styles CSS
│   ├── js/                     # JavaScript
│   ├── images/                 # Images
│   └── map_*.html              # Cartes statiques pré-générées
├── data/                        # Données CSV
│   ├── RP2021_mobpro/          # Données de mobilité INSEE
│   └── processed/              # Données traitées (optionnel)
├── ensemble/                   # Données géographiques INSEE
│   ├── donnees_communes.csv    # Liste des communes
│   ├── donnees_regions.csv     # Liste des régions
│   └── ...
├── scripts/                     # Scripts utilitaires
│   ├── extract_age_ranges.py   # Extraction des tranches d'âge
│   └── generate_maps_with_tooltips.py  # Génération de cartes
├── docs/                        # Documentation
├── app.py                       # Point d'entrée Flask
├── script.py                   # Script de calcul des statistiques
├── requirements.txt            # Dépendances Python
└── README.md                   # Ce fichier
```

### Technologies Utilisées

#### Backend
- **Python 3.11** : Langage de programmation
- **Flask 3.1.2** : Framework web léger et flexible
- **Pandas 2.3.3** : Manipulation et analyse de données
- **NumPy 2.3.5** : Calculs numériques

#### Visualisations
- **Folium 0.20.0** : Cartes interactives basées sur Leaflet
- **Matplotlib 3.10.7** : Création de graphiques
- **Seaborn 0.13.2** : Graphiques statistiques avancés

#### Frontend
- **HTML5** : Structure des pages
- **Bootstrap 5** : Framework CSS (via CDN)
- **JavaScript** : Interactivité (chargement AJAX, modales)
- **Jinja2** : Moteur de templates Flask

#### Export
- **ReportLab 4.2.5** : Génération de PDF
- **Pandas** : Export CSV natif

---

## 🔍 Fonctionnement Détaillé

### 1. Chargement des Données

Le fichier `app/utils/data_loader.py` gère le chargement des CSV avec un système de cache :

```python
# Exemple simplifié
def load_mobility_data(self, use_cache=True):
    # Vérifier le cache
    if cache_existe_et_fichier_non_modifié:
        return cache
    
    # Charger depuis le fichier CSV
    df = pd.read_csv('data/RP2021_mobpro/Commune_1001-13101_2.csv',
                     usecols=['COMMUNE', 'TRANS', 'AGEREVQ', 'IPONDI'])
    
    # Mettre en cache
    cache = df.copy()
    return df
```

**Pourquoi un cache ?**
- Le fichier CSV fait ~670 000 lignes
- Sans cache, chaque requête rechargerait le fichier (lent)
- Le cache vérifie si le fichier a été modifié avant de le recharger

### 2. Calcul des Indicateurs

Dans `app/routes/mobilite.py`, l'API `/api/communes` :

1. **Charge les données** de mobilité et de communes
2. **Applique les filtres** (région, département, âge)
3. **Groupe par commune** et calcule les pourcentages :
   ```python
   # Exemple : Pourcentage de vélo par commune
   grouped = df.groupby(['COMMUNE_CODE', 'TRANS']).sum()
   total_by_commune = grouped.groupby('COMMUNE_CODE').sum()
   velo_percentage = (velo_count / total_by_commune) * 100
   ```
4. **Retourne en JSON** pour le frontend

### 3. Affichage Dynamique

Le fichier `templates/mobilite/communes.html` contient du JavaScript qui :

1. **Appelle l'API** quand les filtres changent :
   ```javascript
   function loadCommunes() {
       fetch('/mobilite/api/communes?region=' + region + '&age=' + age)
           .then(response => response.json())
           .then(data => {
               // Construire le tableau HTML
               buildTable(data.communes);
           });
   }
   ```

2. **Construit le tableau** dynamiquement (sans recharger la page)
3. **Gère la pagination** côté client
4. **Ouvre les modales** de détails au clic

### 4. Export des Données

Le fichier `app/routes/export.py` :

- **CSV** : Utilise `pandas.to_csv()` avec les données filtrées
- **PDF** : Utilise `reportlab` pour créer un document structuré avec :
  - En-tête avec filtres appliqués
  - Tableau formaté
  - Statistiques résumées

---

## 📊 Sources de Données

### Données Démographiques

- **Fichier** : `ensemble/donnees_communes.csv`
- **Source** : INSEE (Institut National de la Statistique)
- **Contenu** :
  - Codes INSEE des communes (COM, CODCOM)
  - Noms des communes
  - Codes région (REG) et département (DEP)
  - Population totale (PTOT)

### Données de Mobilité

- **Fichier** : `data/RP2021_mobpro/Commune_1001-13101_2.csv`
- **Source** : INSEE - Recensement de la Population 2021
- **Contenu** : ~670 000 lignes avec :
  - **COMMUNE** : Nom et code de la commune
  - **TRANS** : Type de transport utilisé
  - **AGEREVQ** : Tranche d'âge de l'individu
  - **IPONDI** : Poids statistique (pour les calculs)

### Types de Transport

Les valeurs possibles pour `TRANS` :
- "Voiture, camion, fourgonnette"
- "Vélo (y compris à assistance électrique)"
- "Transports en commun"
- "Marche à pied (ou rollers, patinette)"
- "Deux-roues motorisé"
- "Pas de transport"

---

## 🎓 Points Pédagogiques

### Concepts Informatiques Illustrés

1. **Architecture Web** :
   - Séparation client/serveur
   - API REST (endpoints JSON)
   - Templates côté serveur (Jinja2)

2. **Traitement de Données** :
   - Manipulation de gros volumes (670k lignes)
   - Agrégation et groupement (Pandas)
   - Calculs statistiques (pourcentages, moyennes)

3. **Optimisation** :
   - Cache en mémoire pour éviter les rechargements
   - Chargement sélectif de colonnes (`usecols`)
   - Pagination pour limiter les données affichées

4. **Interactivité** :
   - AJAX pour charger les données sans recharger la page
   - Filtres dynamiques
   - Modales pour les détails

5. **Visualisation** :
   - Cartes interactives (Folium/Leaflet)
   - Graphiques statistiques (Matplotlib/Seaborn)
   - Export de données (CSV, PDF)

---

## 👥 Équipe

- **Dev 1** : Junior
- **Dev 2** : Baptiste
