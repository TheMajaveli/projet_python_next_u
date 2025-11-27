"""
Application Flask - Projet Mobilité
Tableau de bord d'analyse des inégalités de mobilité en France
"""

from flask import Flask

def create_app():
    """
    Factory function pour créer l'application Flask.
    Cette approche permet de créer plusieurs instances de l'app
    (utile pour les tests).
    """
    app = Flask(__name__)
    
    # Configuration de base
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    
    # Enregistrer les routes
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    return app

