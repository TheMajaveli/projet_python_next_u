#!/bin/bash

# Script de démarrage automatique pour le Dashboard Mobilité
# Gère l'environnement virtuel, les dépendances et le démarrage du serveur Flask

set -e

# Couleurs pour les messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages colorés
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Obtenir le répertoire du script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

print_info "🚀 Démarrage du Dashboard Mobilité"
echo ""

# 1. Vérifier Python
print_info "Vérification de Python..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
print_success "Python $PYTHON_VERSION détecté"
echo ""

# 2. Créer l'environnement virtuel si nécessaire
print_info "Vérification de l'environnement virtuel..."
if [ ! -d "venv" ]; then
    print_warning "Environnement virtuel non trouvé. Création en cours..."
    python3 -m venv venv
    print_success "Environnement virtuel créé"
else
    print_success "Environnement virtuel trouvé"
fi
echo ""

# 3. Activer l'environnement virtuel
print_info "Activation de l'environnement virtuel..."
source venv/bin/activate
print_success "Environnement virtuel activé"
echo ""

# 4. Mettre à jour pip
print_info "Mise à jour de pip..."
pip install --upgrade pip --quiet
print_success "pip mis à jour"
echo ""

# 5. Installer les dépendances
print_info "Installation des dépendances..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --quiet
    print_success "Dépendances installées"
else
    print_warning "Fichier requirements.txt non trouvé. Installation des dépendances de base..."
    pip install flask pandas folium matplotlib seaborn reportlab pydantic --quiet
    print_success "Dépendances de base installées"
fi
echo ""

# 6. Nettoyer le cache si nécessaire
print_info "Nettoyage du cache..."
if [ -d "data/processed" ]; then
    # Ne pas supprimer, juste informer
    print_info "Cache trouvé dans data/processed/"
fi
echo ""

# 7. Vérifier et trouver un port disponible
print_info "Vérification des ports disponibles..."
PORT=5000
FLASK_PID=$(lsof -ti:5000 2>/dev/null | head -1)

if [ -n "$FLASK_PID" ]; then
    PROCESS_NAME=$(ps -p $FLASK_PID -o comm= 2>/dev/null || echo "inconnu")
    if echo "$PROCESS_NAME" | grep -qi "flask\|python"; then
        print_warning "Processus Flask trouvé sur le port 5000 (PID: $FLASK_PID). Arrêt en cours..."
        kill -9 $FLASK_PID 2>/dev/null || true
        sleep 2
    else
        print_warning "Le port 5000 est occupé par un processus système ($PROCESS_NAME)."
        print_info "Recherche d'un port alternatif..."
        PORT=5001
        while lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; do
            PORT=$((PORT + 1))
            if [ $PORT -gt 5010 ]; then
                print_error "Aucun port disponible entre 5000-5010. Veuillez libérer un port manuellement."
                exit 1
            fi
        done
        print_success "Port $PORT disponible (port 5000 occupé par un processus système)"
    fi
fi

if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    print_warning "Le port $PORT est toujours occupé. Recherche d'un port alternatif..."
    PORT=5001
    while lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; do
        PORT=$((PORT + 1))
        if [ $PORT -gt 5010 ]; then
            print_error "Aucun port disponible entre 5000-5010."
            exit 1
        fi
    done
    print_success "Port $PORT disponible"
else
    print_success "Port $PORT disponible"
fi
echo ""

# 8. Configuration Flask
print_info "Configuration Flask..."
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=1

# Configuration des données (par défaut: données fictives)
if [ -z "$USE_DUMMY_DATA" ]; then
    export USE_DUMMY_DATA=true
    print_info "Utilisation des données fictives (par défaut)"
    print_info "Pour utiliser les données CSV: export USE_DUMMY_DATA=false"
else
    if [ "$USE_DUMMY_DATA" = "true" ]; then
        print_info "Utilisation des données fictives"
    else
        print_info "Utilisation des données CSV réelles"
    fi
fi
echo ""

# 9. Démarrer le serveur Flask
print_success "Démarrage du serveur Flask..."
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  🎉 Dashboard Mobilité - Serveur démarré${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}📍 Accès à l'application :${NC}"
echo -e "   ${GREEN}http://127.0.0.1:$PORT${NC}"
echo ""
echo -e "${BLUE}📊 Pages disponibles :${NC}"
echo -e "   • ${GREEN}/${NC}                    - Page d'accueil (KPIs, cartes, graphiques)"
echo -e "   • ${GREEN}/mobilite/communes${NC}    - Liste des communes"
echo -e "   • ${GREEN}/mobilite/regions${NC}      - Liste des régions"
echo -e "   • ${GREEN}/health${NC}               - Vérification de l'état"
echo ""
echo -e "${BLUE}💡 Astuce :${NC}"
echo -e "   Pour arrêter le serveur, utilisez ${YELLOW}Ctrl+C${NC} ou exécutez ${YELLOW}./stop.sh${NC}"
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Démarrer Flask
flask run --host=0.0.0.0 --port=$PORT

