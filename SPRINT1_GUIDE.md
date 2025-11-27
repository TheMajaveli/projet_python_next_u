# Guide Sprint 1 - Cartes 1 & 2
## Pour Dev 1 (Junior)

---

## 📋 Vue d'Ensemble

Ce guide explique **pourquoi** et **comment** nous allons configurer l'environnement de développement et la structure Git pour le projet.

---

## 🎯 CARTE 1 : Configuration Environnement Python/Flask

### Pourquoi cette approche ?

#### 1. **Environnement Virtuel Python**
**Pourquoi ?**
- **Isolation** : Chaque projet Python a ses propres dépendances. Sans environnement virtuel, tous les packages seraient installés globalement, créant des conflits entre projets.
- **Reproductibilité** : L'environnement virtuel garantit que tous les développeurs utilisent les mêmes versions de packages.
- **Sécurité** : Évite de polluer l'installation Python système.

**Comment ?**
- Nous utiliserons `venv` (intégré à Python 3.3+), la solution standard et simple.

#### 2. **Structure de Dossiers**
**Pourquoi cette structure ?**
```
projet_python_next_u/
├── app/              # Code source de l'application Flask
│   ├── __init__.py   # Fichier qui transforme app/ en package Python
│   └── main.py       # Point d'entrée de l'application
├── data/             # Données du projet
│   ├── raw/          # Données brutes (non modifiées)
│   └── processed/    # Données traitées
├── templates/        # Templates HTML (Jinja2)
├── static/           # Fichiers statiques (CSS, JS, images)
├── tests/            # Tests unitaires
├── docs/             # Documentation
├── venv/             # Environnement virtuel (ignoré par Git)
└── requirements.txt  # Liste des dépendances Python
```

**Pourquoi ?**
- **Séparation des responsabilités** : Chaque type de fichier a sa place
- **Convention Flask** : Structure standard reconnue par la communauté
- **Scalabilité** : Facile d'ajouter de nouvelles fonctionnalités
- **Organisation** : Facilite la navigation et la maintenance

#### 3. **requirements.txt**
**Pourquoi ?**
- **Reproductibilité** : Permet de réinstaller exactement les mêmes versions
- **Collaboration** : Baptiste peut installer les mêmes dépendances
- **Déploiement** : Facilite le déploiement en production

**Comment ?**
- Nous utiliserons `pip freeze > requirements.txt` après installation
- Versionner ce fichier dans Git

#### 4. **Fichiers __init__.py**
**Pourquoi ?**
- Transforme un dossier en **package Python**
- Permet d'importer des modules avec `from app import ...`
- Nécessaire pour la structure modulaire Flask

---

## 🎯 CARTE 2 : Structure Projet Git

### Pourquoi cette approche ?

#### 1. **Git Flow (Branches)**
**Pourquoi utiliser des branches ?**
- **Isolation** : Chaque fonctionnalité est développée séparément
- **Collaboration** : Dev 1 et Baptiste peuvent travailler en parallèle
- **Sécurité** : La branche `main` reste toujours fonctionnelle

**Structure de branches :**
```
main          → Code en production (stable)
develop       → Code en développement (intégration)
feature/*     → Nouvelles fonctionnalités
```

**Pourquoi `develop` ?**
- Branche d'intégration où toutes les features sont fusionnées
- Permet de tester l'intégration avant de merger dans `main`
- Standard dans Git Flow

**Pourquoi `feature/*` ?**
- Chaque nouvelle fonctionnalité = une branche
- Exemple : `feature/nettoyage-donnees`, `feature/cartes-folium`
- Facilite le code review et la gestion des tâches

#### 2. **.gitignore**
**Pourquoi ?**
- **Sécurité** : Évite de commiter des fichiers sensibles (mots de passe, clés API)
- **Performance** : Évite de versionner des fichiers générés (cache, logs)
- **Propreté** : Le dépôt Git reste propre et lisible

**Ce qu'on ignore :**
- `venv/` : Environnement virtuel (trop volumineux, spécifique à chaque machine)
- `__pycache__/` : Cache Python (généré automatiquement)
- `.env` : Variables d'environnement (peuvent contenir des secrets)
- `*.pyc` : Fichiers compilés Python
- `.DS_Store` : Fichiers système macOS

#### 3. **README.md**
**Pourquoi ?**
- **Première impression** : C'est le premier fichier qu'on lit
- **Documentation** : Explique rapidement le projet
- **Onboarding** : Aide les nouveaux développeurs à démarrer

**Contenu minimum :**
- Description du projet
- Instructions d'installation
- Structure du projet
- Comment démarrer

---

## 🔧 Processus d'Implémentation

### Étape 1 : Vérifier Python
```bash
python3 --version  # Doit être Python 3.8+
```

### Étape 2 : Créer l'environnement virtuel
```bash
python3 -m venv venv
```
**Explication** : Crée un dossier `venv/` avec un Python isolé

### Étape 3 : Activer l'environnement virtuel
```bash
source venv/bin/activate  # Sur macOS/Linux
```
**Explication** : Active l'environnement (le prompt change avec `(venv)`)

### Étape 4 : Installer Flask
```bash
pip install flask
pip install pandas folium matplotlib seaborn
```
**Explication** : Installe Flask et les dépendances du projet

### Étape 5 : Créer la structure de dossiers
```bash
mkdir -p app data/raw data/processed templates static tests docs
```
**Explication** : Crée tous les dossiers nécessaires

### Étape 6 : Créer les fichiers de base
- `app/__init__.py` : Initialise le package Flask
- `app/main.py` : Point d'entrée avec une route de test
- `requirements.txt` : Liste des dépendances

### Étape 7 : Tester Flask
```bash
flask run
```
**Explication** : Vérifie que tout fonctionne

### Étape 8 : Initialiser Git
```bash
git init
git checkout -b develop
```
**Explication** : Crée le dépôt et la branche develop

### Étape 9 : Créer .gitignore
Fichier avec les patterns à ignorer

### Étape 10 : Premier commit
```bash
git add .
git commit -m "Initial setup: Flask environment and project structure"
```

---

## 📚 Concepts Clés à Retenir

### 1. **Environnement Virtuel**
- **C'est quoi ?** : Un Python isolé pour ce projet uniquement
- **Pourquoi ?** : Évite les conflits de versions entre projets
- **Quand l'utiliser ?** : Toujours activer avant de travailler

### 2. **Package Python**
- **C'est quoi ?** : Un dossier avec `__init__.py`
- **Pourquoi ?** : Permet d'importer des modules facilement
- **Exemple** : `from app import routes`

### 3. **Branches Git**
- **main** : Code stable, prêt pour production
- **develop** : Code en développement, où on intègre les features
- **feature/*** : Branche temporaire pour une fonctionnalité

### 4. **Workflow Git**
1. Créer une branche `feature/nom-fonctionnalite`
2. Développer la fonctionnalité
3. Commit régulièrement
4. Merger dans `develop`
5. Tester sur `develop`
6. Merger `develop` dans `main` pour release

---

## ✅ Checklist de Validation

### Carte 1
- [ ] `venv/` existe et contient Python
- [ ] Environnement activé (prompt montre `(venv)`)
- [ ] Flask installé (`pip list | grep Flask`)
- [ ] Structure de dossiers créée
- [ ] `requirements.txt` contient Flask et dépendances
- [ ] `app/__init__.py` existe
- [ ] `app/main.py` existe avec une route de test
- [ ] `flask run` démarre sans erreur
- [ ] Page accessible sur http://127.0.0.1:5000

### Carte 2
- [ ] Dépôt Git initialisé (`.git/` existe)
- [ ] `.gitignore` existe et ignore `venv/`, `__pycache__/`, `.env`
- [ ] Branche `develop` créée et active
- [ ] `README.md` existe avec description du projet
- [ ] Premier commit effectué
- [ ] Structure visible dans `git log`

---

## 🚨 Erreurs Courantes et Solutions

### Erreur : "python3: command not found"
**Solution** : Installer Python 3 ou utiliser `python` au lieu de `python3`

### Erreur : "venv: No module named venv"
**Solution** : Installer `python3-venv` (Linux) ou mettre à jour Python

### Erreur : "flask: command not found"
**Solution** : Vérifier que l'environnement virtuel est activé

### Erreur : "ModuleNotFoundError: No module named 'flask'"
**Solution** : Réinstaller Flask dans l'environnement virtuel activé

### Erreur Git : "fatal: not a git repository"
**Solution** : Exécuter `git init` dans le dossier du projet

---

## 🎓 Ressources pour Aller Plus Loin

- **Flask Documentation** : https://flask.palletsprojects.com/
- **Python venv** : https://docs.python.org/3/library/venv.html
- **Git Flow** : https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow
- **PEP 8** (Style Python) : https://pep8.org/

---

## 📝 Notes Personnelles

**Points à retenir pour la suite :**
1. Toujours activer `venv` avant de travailler
2. Créer une branche `feature/` pour chaque nouvelle tâche
3. Commit régulièrement avec des messages clairs
4. Tester après chaque modification importante
5. Consulter la documentation Flask si besoin

---

**Prêt à implémenter ? Passons à l'action ! 🚀**

