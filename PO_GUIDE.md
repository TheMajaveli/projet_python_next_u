# Guide Product Owner - Projet Mobilité

## 1. Rôle du Product Owner (P.O.)

En tant que Product Owner, vos responsabilités principales sont :

### 1.1 Vision et Priorisation
- **Définir la vision produit** : S'assurer que l'équipe comprend l'objectif final (dashboard d'analyse des inégalités de mobilité)
- **Prioriser les fonctionnalités** : Déterminer l'ordre d'implémentation selon la valeur métier
- **Gérer le backlog** : Maintenir une liste ordonnée des tâches à réaliser

### 1.2 Communication et Coordination
- **Lien entre stakeholders et équipe** : Traduire les besoins métier en tâches techniques
- **Clarifier les exigences** : Répondre aux questions des développeurs sur les fonctionnalités
- **Valider les livrables** : S'assurer que chaque fonctionnalité répond aux besoins

### 1.3 Suivi et Reporting
- **Suivre l'avancement** : Vérifier régulièrement la progression dans Trello
- **Identifier les blocages** : Détecter et résoudre les obstacles rapidement
- **Ajuster le plan** : Réorganiser les priorités si nécessaire

### 1.4 Gestion de l'Équipe
- **Répartir les tâches** : Assigner les user stories selon les compétences
- **Faciliter les daily standups** : Organiser des points quotidiens (ou hebdomadaires)
- **Favoriser la collaboration** : Encourager la communication entre Dev 1 (Junior) et Dev 2 (Baptiste)

---

## 2. Structure Trello Recommandée

### 2.1 Colonnes du Board

```
📋 BACKLOG | 🔄 TO DO | ⚙️ IN PROGRESS | 👀 REVIEW | ✅ DONE
```

**BACKLOG** : Toutes les tâches identifiées, non priorisées
**TO DO** : Tâches priorisées et prêtes à être développées (Sprint actuel)
**IN PROGRESS** : Tâches en cours de développement
**REVIEW** : Tâches terminées, en attente de validation
**DONE** : Tâches validées et complètes

### 2.2 Labels Recommandés

- 🔴 **PRIORITÉ HAUTE** : Fonctionnalités critiques
- 🟡 **PRIORITÉ MOYENNE** : Fonctionnalités importantes
- 🟢 **PRIORITÉ BASSE** : Améliorations / Bonus
- 🐛 **BUG** : Corrections de bugs
- 📊 **DATA** : Tâches liées aux données
- 🎨 **UI/UX** : Interface utilisateur
- 🔧 **TECH** : Tâches techniques/infrastructure
- 📝 **DOC** : Documentation

### 2.3 Checklist par Carte

Chaque carte doit contenir :
- [ ] Description claire de la tâche
- [ ] Critères d'acceptation
- [ ] Fichiers/endpoints concernés
- [ ] Dépendances (si applicable)
- [ ] Estimation (en points ou heures)

---

## 3. Répartition des Tâches par Développeur

### Stratégie de Répartition

**Dev 1 (Junior)** - Tâches d'apprentissage et de base :
- Configuration initiale du projet
- Nettoyage de données (Pandas)
- Création de fonctions de calcul simples
- Tests unitaires
- Documentation de base

**Dev 2 (Baptiste)** - Tâches plus complexes :
- Architecture Flask
- Intégration des visualisations
- Export PDF
- Optimisations
- Code review pour Dev 1

**Tâches Collaboratives** :
- Définition des structures de données
- Tests d'intégration
- Revue de code mutuelle

---

## 4. Planification par Sprints

### Sprint 1 : Setup & Données (Semaine 1)
**Objectif** : Mise en place de l'environnement et préparation des données

**Tâches** :
- [ ] Configuration environnement Python/Flask
- [ ] Récupération des données sources (Open Data France, INSEE)
- [ ] Nettoyage initial des données
- [ ] Structure du projet Git

**Assignation** :
- Dev 1 : Setup environnement, récupération données
- Dev 2 : Structure projet, configuration Git

### Sprint 2 : Analyse de Données (Semaine 2)
**Objectif** : Créer les fonctions d'analyse et calculer les indicateurs

**Tâches** :
- [ ] Scripts de nettoyage (valeurs manquantes, formats)
- [ ] Fusion des tables (démographie + transport + géolocalisation)
- [ ] Fonctions d'agrégation (département, type transport, âge)
- [ ] Calcul des indicateurs clés

**Assignation** :
- Dev 1 : Nettoyage et fusion de données
- Dev 2 : Calcul des indicateurs complexes

### Sprint 3 : Visualisations (Semaine 3)
**Objectif** : Créer les graphiques et cartes interactives

**Tâches** :
- [ ] Cartes interactives Folium (zones mal desservies)
- [ ] Graphiques Matplotlib/Seaborn (histogrammes, bar charts)
- [ ] Intégration des visualisations dans Flask

**Assignation** :
- Dev 1 : Graphiques simples (bar charts, histogrammes)
- Dev 2 : Cartes Folium, intégration Flask

### Sprint 4 : Dashboard Web (Semaine 4)
**Objectif** : Créer l'interface web avec filtres

**Tâches** :
- [ ] Templates HTML/Jinja2
- [ ] Pages d'affichage des indicateurs
- [ ] Système de filtres (zone, transport, âge)
- [ ] Design responsive (Bootstrap)

**Assignation** :
- Dev 1 : Templates de base, pages simples
- Dev 2 : Système de filtres, intégration complète

### Sprint 5 : Exports & Bonus (Semaine 5)
**Objectif** : Fonctionnalités d'export et améliorations

**Tâches** :
- [ ] Export CSV
- [ ] Export PDF (FPDF/ReportLab)
- [ ] Rapport PDF personnalisé (bonus)
- [ ] Tests finaux et corrections

**Assignation** :
- Dev 1 : Export CSV, tests
- Dev 2 : Export PDF, rapport personnalisé

### Sprint 6 : Documentation & Finalisation (Semaine 6)
**Objectif** : Finaliser la documentation et préparer la présentation

**Tâches** :
- [ ] Guide d'installation
- [ ] Documentation des indicateurs
- [ ] Préparation présentation orale
- [ ] Revue finale du code

**Assignation** :
- Dev 1 : Guide d'installation, documentation indicateurs
- Dev 2 : Revue code, préparation présentation

---

## 5. Critères d'Acceptation par Fonctionnalité

### 5.1 Nettoyage de Données
- ✅ Toutes les valeurs manquantes sont identifiées et traitées
- ✅ Formats de données cohérents (dates, nombres)
- ✅ Doublons supprimés
- ✅ Script réutilisable et documenté

### 5.2 Calcul d'Indicateurs
- ✅ Indicateurs calculés correctement selon la formule
- ✅ Résultats validés sur un échantillon
- ✅ Fonctions testées unitairement
- ✅ Documentation de chaque indicateur

### 5.3 Visualisations
- ✅ Cartes affichent correctement les zones
- ✅ Graphiques sont lisibles et pertinents
- ✅ Légendes et labels clairs
- ✅ Performance acceptable (< 3s de chargement)

### 5.4 Dashboard Web
- ✅ Interface responsive (mobile + desktop)
- ✅ Filtres fonctionnent correctement
- ✅ Navigation intuitive
- ✅ Pas d'erreurs console

### 5.5 Exports
- ✅ CSV contient toutes les données demandées
- ✅ PDF est bien formaté et lisible
- ✅ Exports fonctionnent pour tous les filtres

---

## 6. Points de Contrôle (Checkpoints)

### Checkpoint Hebdomadaire
- **Quand** : Chaque vendredi
- **Durée** : 30 minutes
- **Ordre du jour** :
  1. Récap des tâches terminées
  2. Blocages identifiés
  3. Ajustement des priorités
  4. Planification semaine suivante

### Daily Standup (Optionnel mais recommandé)
- **Quand** : Chaque matin (10-15 min)
- **Questions** :
  - Qu'as-tu fait hier ?
  - Que vas-tu faire aujourd'hui ?
  - Y a-t-il des blocages ?

---

## 7. Gestion des Risques

### Risques Identifiés

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Données incomplètes | Moyenne | Élevé | Tester avec échantillon dès Sprint 1 |
| Complexité Folium | Faible | Moyen | Formation rapide, documentation |
| Délais dépassés | Moyenne | Élevé | Prioriser fonctionnalités core, bonus optionnel |
| Conflits Git | Faible | Moyen | Bonnes pratiques Git, code review |

---

## 8. Métriques de Succès

- ✅ **Vélocité** : Nombre de cartes complétées par sprint
- ✅ **Qualité** : Nombre de bugs détectés en review
- ✅ **Couverture** : Pourcentage de code testé
- ✅ **Satisfaction** : Feedback des développeurs sur la clarté des tâches

---

## 9. Communication

### Canaux Recommandés
- **Trello** : Suivi des tâches et commentaires
- **GitHub** : Code et issues techniques
- **Réunions** : Checkpoints hebdomadaires
- **Slack/Email** : Communication quotidienne si besoin

### Règles de Communication
- ✅ Mettre à jour Trello quotidiennement
- ✅ Commenter les cartes en cas de question
- ✅ Taguer le PO dans les décisions importantes
- ✅ Documenter les décisions techniques

---

## 10. Template de User Story

```
**Titre** : [Action] [Résultat]

**Description** :
En tant que [utilisateur],
Je veux [action],
Afin de [bénéfice].

**Critères d'acceptation** :
- [ ] Critère 1
- [ ] Critère 2
- [ ] Critère 3

**Dépendances** :
- [Carte X] doit être terminée avant

**Fichiers concernés** :
- `path/to/file.py`

**Estimation** : [X] points / heures

**Assigné à** : [Dev 1 / Dev 2]
```

---

## 11. Actions Immédiates pour le PO

1. ✅ **Créer le board Trello** avec la structure proposée
2. ✅ **Créer les cartes pour le Sprint 1** avec les détails
3. ✅ **Organiser une réunion de kickoff** avec l'équipe
4. ✅ **Définir les rôles** et responsabilités de chacun
5. ✅ **Mettre en place les checkpoints** hebdomadaires
6. ✅ **Partager ce document** avec l'équipe

---

**Bon courage avec le projet ! 🚀**

