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
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    # Configuration de base
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    
    # Enregistrer les routes
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    # Enregistrer les routes mobilité
    from app.routes.mobilite import bp as mobilite_bp
    app.register_blueprint(mobilite_bp)
    
    # Enregistrer les routes d'export
    from app.routes.export import bp as export_bp
    app.register_blueprint(export_bp)
    
    # Enregistrer les routes de visualisation
    from app.routes.visualizations import bp as visualizations_bp
    app.register_blueprint(visualizations_bp)
    
    return app

