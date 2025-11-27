# Tableau de bord d'analyse des inégalités de mobilité en France

## 📋 Description du Projet

Application web (dashboard) permettant à une collectivité de :
- Comparer les conditions de mobilité entre communes / zones (urbaines vs rurales)
- Identifier les zones mal desservies
- Produire des indicateurs pour appuyer des décisions (infrastructures, communication interne, open data)

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de packages Python)

### Étapes d'installation

1. **Cloner le dépôt** (si applicable)
   ```bash
   git clone <url-du-depot>
   cd projet_python_next_u
   ```

2. **Créer l'environnement virtuel**
   ```bash
   python3 -m venv venv
   ```

3. **Activer l'environnement virtuel**
   ```bash
   # Sur macOS/Linux
   source venv/bin/activate
   
   # Sur Windows
   venv\Scripts\activate
   ```

4. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

## 🏃 Démarrage

1. **Activer l'environnement virtuel** (si pas déjà fait)
   ```bash
   source venv/bin/activate
   ```

2. **Démarrer l'application Flask**
   ```bash
   export FLASK_APP=app.py
   flask run
   ```
   
   Ou directement :
   ```bash
   python app.py
   ```

3. **Accéder à l'application**
   - Ouvrir un navigateur à l'adresse : http://127.0.0.1:5000
   - Vérifier l'état : http://127.0.0.1:5000/health

## 📁 Structure du Projet

```
projet_python_next_u/
├── app/                    # Code source de l'application Flask
│   ├── __init__.py         # Initialisation de l'application
│   └── main.py             # Routes principales
├── data/                   # Données du projet
│   ├── raw/                # Données brutes (non modifiées)
│   └── processed/          # Données traitées
├── templates/              # Templates HTML (Jinja2)
├── static/                 # Fichiers statiques (CSS, JS, images)
├── tests/                  # Tests unitaires
├── docs/                   # Documentation
├── venv/                   # Environnement virtuel (ignoré par Git)
├── app.py                  # Point d'entrée de l'application
├── requirements.txt        # Dépendances Python
└── README.md              # Ce fichier
```

## 🛠️ Technologies Utilisées

- **Backend** : Python 3.11 + Flask
- **Données** : Pandas
- **Visualisations** : Folium (cartes), Matplotlib, Seaborn (graphiques)
- **Frontend** : HTML5 + Bootstrap + Jinja2

## 👥 Équipe

- **Dev 1** : Junior
- **Dev 2** : Baptiste
- **Product Owner** : [Votre nom]

## 📝 Workflow Git

- **main** : Branche principale (code stable)
- **develop** : Branche de développement (intégration)
- **feature/*** : Branches pour nouvelles fonctionnalités

### Structure des branches

```bash
# Voir toutes les branches
git branch -a

# Branches principales
develop          # Branche de développement (active par défaut)
feature/*         # Branches pour nouvelles fonctionnalités
```

### Créer une nouvelle fonctionnalité
```bash
# 1. S'assurer d'être sur develop et à jour
git checkout develop
git pull origin develop  # Si dépôt distant existe

# 2. Créer une nouvelle branche feature
git checkout -b feature/nom-fonctionnalite

# 3. Développer la fonctionnalité
# ... faire vos modifications ...

# 4. Commiter les changements
git add .
git commit -m "Description claire de la fonctionnalité"

# 5. Pousser la branche (si dépôt distant existe)
git push origin feature/nom-fonctionnalite

# 6. Après validation, merger dans develop
git checkout develop
git merge feature/nom-fonctionnalite
git branch -d feature/nom-fonctionnalite  # Supprimer la branche locale
```

### Exemples de noms de branches feature
- `feature/nettoyage-donnees`
- `feature/cartes-folium`
- `feature/export-pdf`
- `feature/filtres-geographiques`

## 📚 Documentation

- Guide Sprint 1 : `SPRINT1_GUIDE.md`
- Guide Product Owner : `PO_GUIDE.md`
- Cartes Trello : `TRELLO_CARDS.md`

## 🐛 Dépannage

### Erreur : "flask: command not found"
**Solution** : Vérifier que l'environnement virtuel est activé (`source venv/bin/activate`)

### Erreur : "ModuleNotFoundError: No module named 'flask'"
**Solution** : Réinstaller les dépendances (`pip install -r requirements.txt`)

### Erreur : "Address already in use"
**Solution** : Changer le port (`flask run --port=5001`)

## 📄 Licence

[À définir]

---

**Dernière mise à jour** : Sprint 1 - Configuration initiale

