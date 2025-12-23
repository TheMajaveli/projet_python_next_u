"""
Routes principales de l'application Flask
"""

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from script import main
from flask import Blueprint, render_template

# Créer un Blueprint pour organiser les routes
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """
    Page d'accueil du dashboard
    """
    return render_template('pages/home.html', stats=main(), test="test")

@bp.route('/health')
def health():
    """
    Route de santé pour vérifier que l'application fonctionne
    """
    return {'status': 'ok', 'message': 'Application Flask fonctionnelle'}, 200

