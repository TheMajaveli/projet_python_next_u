"""
Routes principales de l'application Flask
"""

from flask import Blueprint, render_template

# Créer un Blueprint pour organiser les routes
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """
    Page d'accueil du dashboard
    """
    return render_template('index.html', 
                         title='Dashboard Mobilité',
                         message='Bienvenue sur le tableau de bord d\'analyse des inégalités de mobilité')

@bp.route('/health')
def health():
    """
    Route de santé pour vérifier que l'application fonctionne
    """
    return {'status': 'ok', 'message': 'Application Flask fonctionnelle'}, 200

