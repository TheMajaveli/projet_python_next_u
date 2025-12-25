#!/bin/bash

# Script d'arrêt pour le Dashboard Mobilité
# Arrête tous les processus Flask en cours d'exécution

set -e

# Couleurs pour les messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info "🛑 Arrêt du Dashboard Mobilité"
echo ""

# Arrêter les processus Flask
print_info "Recherche des processus Flask..."
FLASK_PIDS=$(pgrep -f "flask run" || true)
PYTHON_PIDS=$(pgrep -f "python.*app.py" || true)

STOPPED_ANY=false

if [ ! -z "$FLASK_PIDS" ]; then
    print_info "Arrêt des processus Flask (PID: $FLASK_PIDS)..."
    pkill -f "flask run" || true
    STOPPED_ANY=true
fi

if [ ! -z "$PYTHON_PIDS" ]; then
    print_info "Arrêt des processus Python app.py (PID: $PYTHON_PIDS)..."
    pkill -f "python.*app.py" || true
    STOPPED_ANY=true
fi

if [ "$STOPPED_ANY" = true ]; then
    sleep 2
fi

# Vérifier et libérer les ports Flask (5000-5010)
print_info "Vérification des ports Flask (5000-5010)..."
PORTS_FREED=0
for PORT in {5000..5010}; do
    PID=$(lsof -ti:$PORT 2>/dev/null | head -1)
    if [ -n "$PID" ]; then
        PROCESS_NAME=$(ps -p $PID -o comm= 2>/dev/null || echo "inconnu")
        if echo "$PROCESS_NAME" | grep -qi "flask\|python"; then
            print_info "Arrêt du processus Flask sur le port $PORT (PID: $PID)..."
            kill -9 $PID 2>/dev/null && PORTS_FREED=$((PORTS_FREED + 1)) || true
        fi
    fi
done

if [ $PORTS_FREED -gt 0 ]; then
    sleep 1
    print_success "$PORTS_FREED port(s) Flask libéré(s)"
elif [ "$STOPPED_ANY" = false ]; then
    print_warning "Aucun processus Flask trouvé"
fi

print_success "Arrêt terminé"
echo ""

